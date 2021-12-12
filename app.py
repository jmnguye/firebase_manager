import firebase_admin
import os
import json
import argparse
from firebase_admin import credentials
from firebase_admin import db

DB_SIZE = 10

parser = argparse.ArgumentParser(description='CRUD Manage data on firebase')
parser.add_argument('--action')

app_path = os.getcwd()
cred = credentials.Certificate(
    f"{app_path}/jenkins-web-cv-firebase-adminsdk-ay7vj-5afd2a8970.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jenkins-web-cv-default-rtdb.europe-west1.firebasedatabase.app/'
})


chart = '0.0.1'
status = 'started'
tag_docker = '0.0.1'

my_value = {
    'commit': '1a2c31',
    'release_chart': chart,
    'status': status,
    'tag_docker': tag_docker,
    'timestamp': {'.sv': 'timestamp'}
}

my_value2 = {
    'commit': '1a2c32',
    'release_chart': chart,
    'status': status,
    'tag_docker': tag_docker,
    'timestamp': {'.sv': 'timestamp'}
}

my_value3 = {
    'commit': '1a2c33',
    'release_chart': chart,
    'status': status,
    'tag_docker': tag_docker,
    'timestamp': {'.sv': 'timestamp'}
}

# ref.push(my_value)
# ref.push(my_value2)
#ref.push(my_value3)

def get_ref():
    return db.reference('/commits')

def update():
    pass

def add(value):
    ref = get_ref()
    ref.push(value)

def delete():
    pass

'''
i want to limit entries up to let's say 2 for the moment
in case there are more, remove the oldest one
data are filled like a queue
get the size of ref
'''
def get_ref_shallow():
    ref = db.reference('/commits')
    return ref.get(shallow=True)

def get_nodes_sorted():
    shallowed = get_ref_shallow() # get only keys
    json_sorted = json.dumps(shallowed, sort_keys=True) # this trick help me sort key
    return json.loads(json_sorted) # build python objects from json output sorted
#print(type(nodes_sorted))
#print(db.reference(f'/commits/{list(nodes_sorted.keys())[0]}').get())

def restrict_db_size():
    while len(get_ref_shallow()) > DB_SIZE:
        top_node = list(get_nodes_sorted().keys())[0]
        node = db.reference(f'/commits/{top_node}')
        print(node.get())
        node.delete()

restrict_db_size()
