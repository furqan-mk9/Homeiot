import os
import glob
import time
import json
from bluetooth import *
from firebase import firebase

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

# used json.dumps to get pretty json
# used json.loads to load json from a string
# used json.load to load json from json object
# used ntplib to download time from a remote server

port = server_sock.getsockname()[1]

username = ''
FIREBASE_REF = 'https://homeiot.firebaseio.com/'
firebase = firebase.FirebaseApplication(FIREBASE_REF, None)

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "AquaPiServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
def init():
    global username
    with open('user/config.json') as json_file:
        user_data = json.load(json_file)
        username = user_data['username']
        print 'Logging in as ' + username + '...'
    return;

def get_utc_time():
    import ntplib, datetime
    from time import ctime
    client = ntplib.NTPClient()
    response = client.request('pool.ntp.org')
    d = datetime.datetime.strptime(ctime(response.tx_time), '%a %b %d %H:%M:%S %Y')
    timestamp = d.strftime('%Y%m%d%H%M%S')
    return timestamp;

def new_unlock(unlocker):
    return;

def sync_lock_history():
    #try:
        global username
        history_path = username + '/lock' + '/history'
        with open('user/lock/history.json') as json_file:
            history_local = json.load(json_file)
            print username
            history_remote = firebase.get(history_path, None)
            print json.dumps(history_remote)
            
            if history_local != history_remote:
                for key in history_remote:
                    print json.dumps(history_remote[key])
            #test_unlock = {'username': 'shehzad', 'time': get_utc_time()}
            #firebase.post(history_path, test_unlock)  
        return;
    #except:
    #    print 'Error encountered'
    #   try:
    

def search_mobile():         
    print "Waiting for connection on RFCOMM channel %d" % port
    client_sock, client_info = server_sock.accept()
    print "Accepted connection from ", client_info
    try:
        data = client_sock.recv(1024)
        if len(data) == 0: return;
	print "received [%s]" % data
                
    except IOError:
	pass

    except KeyboardInterrupt:
	print "disconnected"
	client_sock.close()
	server_sock.close()
	print "all done"
	return;

init()
sync_lock_history()
'''
sync_lock_history()

while True:
    check_mobile()
'''
