import firebase_admin
import os
import json
from firebase_admin import credentials
from firebase_admin import db

app_path = os.getcwd()
cred = credentials.Certificate(
    f"{app_path}/jenkins-web-cv-firebase-adminsdk-ay7vj-5afd2a8970.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jenkins-web-cv-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference('/commits')

chart = '0.0.1'
status = 'started'
tag_docker = '0.0.1'

# print(ref.get())
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

#print(json.dumps(ref.get(), indent=4, sort_keys=True))


def update():
    pass


def add():
    pass


def delete():
    pass


'''
i want to limit entries up to let's say 2 for the moment
in case there are more, remove the oldest one
data are filled like a queue
get the size of ref
'''
shallowed = ref.get(shallow=True) # get only keys
json_sorted = json.dumps(shallowed, sort_keys=True) # this trick help me sort key
nodes_sorted = json.loads(json_sorted) # build python objects from json output sorted
#print(type(nodes_sorted))
#print(db.reference(f'/commits/{list(nodes_sorted.keys())[0]}').get())
while len(shallowed) > 10:
    top_node = list(nodes_sorted.keys())[0]
    node = db.reference(f'/commits/{top_node}')
    print(node.get())
    node.delete()
    shallowed = ref.get(shallow=True)
    

#for node in nodes_sorted:
#        node_ref = db.reference(f'/commits/{node}')
#        print(node_ref.get())


print(len(shallowed))
