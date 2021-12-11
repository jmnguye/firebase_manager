import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(
    "/home/mxp/DEVELOP/Python/firebase/jenkins-web-cv-firebase-adminsdk-ay7vj-5afd2a8970.json")
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
    'tag_docker': tag_docker
}

my_value2 = {
    'commit': '1a2c32',
    'release_chart': chart,
    'status': status,
    'tag_docker': tag_docker
}

my_value3 = {
    'commit': '1a2c33',
    'release_chart': chart,
    'status': status,
    'tag_docker': tag_docker
}

ref.push(my_value)
ref.push(my_value2)
ref.push(my_value3)

print(ref.get())


def update():
    pass


def add():
    pass


def delete():
    pass

# print(ref.)
