import firebase_admin
import os
import json
import argparse
import re
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin.exceptions import FirebaseError

DB_SIZE = 10

parser = argparse.ArgumentParser(description='CRUD Manage data on firebase',
                                 usage='app.py [-h] [--post COMMIT] [--get COMMIT] [--delete COMMIT] [--patch COMMIT]')
group_parser = parser.add_mutually_exclusive_group()
group_parser.add_argument('--post', help='add commit entry')
group_parser.add_argument('--get', help='retrieve data from commit')
group_parser.add_argument('--delete', help='delete data by commit')
group_parser.add_argument('--patch', help='update commit entry')
args = parser.parse_args()

app_path = os.getcwd()
cred = credentials.Certificate(
    f"{app_path}/jenkins-web-cv-firebase-adminsdk-ay7vj-5afd2a8970.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jenkins-web-cv-default-rtdb.europe-west1.firebasedatabase.app/'
})


chart = '0.0.1'
status = 'started'
tag_docker = '0.0.1'

empty_value = {
    'commit': '',
    'release_char': '',
    'status': '',
    'tag_docker': '',
    'timestamp': ''
}

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

def get_ref_commits():
    return db.reference('/commits')

def patch(value):
    pass

def find_ref_commit_in_db(commit):
    if check_commit(commit):
        for ref in ref_commits.get():
            ref_commit = db.reference(f'/commits/{ref}')
            ref_commit_get = ref_commit.get()
            if commit == ref_commit_get['commit']:
                return ref_commit
        return None

def post(commit):
    ref_commit = find_ref_commit_in_db(commit)
    if check_commit(commit):
        if ref_commit is None:
            try:
                ref_commits.push({'commit': commit})
                print(f'Commit {commit} successfully added')
            except FirebaseError as e:
                print(e)
            except ValueError as e:
                print(e)
        else:
            print(f'Nothing done, commit {commit} already exist in db')

def get(commit):
    ref_commit = find_ref_commit_in_db(commit)
    if ref_commit:
        print(ref_commit.get())
    else:
        print(f'{commit} not found')

def delete(commit):
    ref_commit = find_ref_commit_in_db(commit)
    if ref_commit:
        ref_commit.delete()
        print(f'{commit} deleted')
    else:
        print(f'{commit} not found')

def get_ref_commits_shallow():
    return ref_commits.get(shallow=True)

def get_nodes_sorted():
    shallowed = get_ref_commits_shallow()  # get only keys
    # this trick help me sort key
    json_sorted = json.dumps(shallowed, sort_keys=True)
    # build python objects from json output sorted
    return json.loads(json_sorted)

def restrict_db_size():
    while len(get_ref_commits_shallow()) > DB_SIZE:
        top_node = list(get_nodes_sorted().keys())[0]
        node = db.reference(f'/commits/{top_node}')
#        print(node.get())
        node.delete()

def check_commit(commit):
    if re.fullmatch(r'[0-9a-z]{7}', commit):
        return True
    else:
        print('invalid commit syntax')
        return False

ref_commits = get_ref_commits()

if args.post:
    commit = args.post
    post(commit)

elif args.get:
    commit = args.get
    get(commit)

elif args.delete:
    commit = args.delete
    delete(commit)

elif args.patch:
    pass

restrict_db_size()
