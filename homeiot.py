import os
import glob
import time
import json
import urllib
from bluetooth import *
from firebase import firebase

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

CURRENT_USER = ''
FIREBASE_REF = 'https://homeiot.firebaseio.com/' + CURRENT_USER + '/'
firebase = firebase.FirebaseApplication(FIREBASE_REF, None)

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "AquaPiServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
def init():
    with open('config.json') as json_file:
        user_data = json.load(json_file)
        CURRENT_USER = user_data['username']
        print 'Logging in as ' + CURRENT_USER + '...'
    return;

def new_unlock(unlocker):
    return;

def sync_lock_history():
    with open('lock/history.json') as json_file:
        history_data = json.load(json_file)
    #try:
    return;

def sync_lock_guests():
    return;

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
'''
while True:
    check_mobile()
'''
