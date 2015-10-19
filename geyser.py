import time
import requests
import json
from firebase import firebase

username = ''
FIREBASE_REF = 'https://homeiot.firebaseio.com/'
firebase = firebase.FirebaseApplication(FIREBASE_REF, None)

def init():
    global username
    with open('user/config.json') as json_file:
        user_data = json.load(json_file)
        username = user_data['username']
        print 'Logging in as ' + username + '...'
    return;

def get_time():
    from datetime import datetime
    now = datetime.now()
    d = now.strftime('%Y%m%d%H%M%S')
    return d;

def new_geyser_time():
    payload = {'username':'furqan', 'time':get_time()} 
    r = requests.post('https://homeiot.herokuapp.com/api/geyser/new-time', data=payload)
    print r.text
    return;

def update_history():
    history_path = username + '/geyser' + '/history'
    history = firebase.get(history_path, None)
    with open('user/geyser/history.json', 'w') as json_file:
        json.dump(history, json_file)
    return;

init()
new_geyser_time()
update_history()

