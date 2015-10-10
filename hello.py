import time
import json
import requests
import serial
from firebase import firebase

CURRENT_USER = 'furqan'
FIREBASE_REF = 'https://homeiot.firebaseio.com/' + CURRENT_USER + '/'
firebase = firebase.FirebaseApplication(FIREBASE_REF, None)
security_delay = 5
    
def new_unlock(unlocker_name):
    lockhistory_url = 'lock/history'
    current_time = time.strftime('%Y%m%d%H%M%S')
    data = { 'person': unlocker_name, 'time': current_time }
    result = firebase.post(lockhistory_url, data)
    print "Record inserted: " + str(result)
    time.sleep(security_delay)
    return;

def sync_guests(new_data):
    with open('/tmp/lock_data.json', 'w') as jsonfile_w:
        json.dump(new_data, jsonfile_w)
        print 'guest data updated'
    return;

def guest_routine():
    blSerial = serial.Serial("/dev/rfcomm1",baudrate=9600)
    print 'guest routine check'
    with open('/tmp/lock_data.json') as jsonfile:
        local_data = json.load(jsonfile)
    lockguests_url = 'lock/guests'
    response = firebase.get(lockguests_url, None)
    
    if ( local_data != response ):
        sync_guests(response)
        blSerial.write('{"guests": ' + str(json.dumps(response)) +'}')
        print 'broadcasting new data over bluetooth...'
        time.sleep(security_delay)
        print 'broadcast end'
    else:
        blSerial.write('{"guests": "no updates"}')
    return;

def unlock_routine():
    blSerial = serial.Serial("/dev/rfcomm1",baudrate=9600)
    print 'unlock routine check'
    try:
        j = json.loads(str(blSerial.readline()))
        if ( j['unlocker'] != 'nil' ):
            new_unlock(j['unlocker'])
    except:
        print '! bluetooth not connected'
    return;

# MAIN LOOPING CODE
while 1:
    guest_routine()
    unlock_routine()
    time.sleep(3)
