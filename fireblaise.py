import firebase_admin
import os
import json
import argparse
import re
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import exceptions
from firebase_admin.exceptions import FirebaseError

DB_SIZE = 100

parser = argparse.ArgumentParser(description='CRUD Manage data on firebase', usage='fireblaise.py [-h] [--post COMMIT] [--get COMMIT] [--delete COMMIT] [--patch COMMIT VALUE:STRING] [--put COMMIT VALUE:STRING]')
group_parser = parser.add_mutually_exclusive_group()
group_parser.add_argument('--post', help='add commit entry')
group_parser.add_argument('--get', help='retrieve data from commit')
group_parser.add_argument('--delete', help='delete data by commit')
group_parser.add_argument('--patch', nargs='+', help='update commit entry with list argument')
group_parser.add_argument('--put', nargs='+', help='replace commit entry with list argument')
args = parser.parse_args()

app_path = os.getcwd()
cred = credentials.Certificate(
    f"{app_path}/jenkins-web-cv-firebase-adminsdk-ay7vj-5afd2a8970.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jenkins-web-cv-default-rtdb.europe-west1.firebasedatabase.app/'
})

class CommitNotFound(Exception):
    pass

class CommitSyntaxError(Exception):
    pass

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

def get_ref_commits():
    return db.reference('/commits')

def find_ref_commit_in_db(commit):
    if check_commit(commit):
        for ref in ref_commits.get():
            ref_commit = db.reference(f'/commits/{ref}')
            ref_commit_get = ref_commit.get()
            if commit == ref_commit_get['commit']:
                return ref_commit
        return None

def patch(values):
    try:
        commit = values.pop(0)
        ref_commit = find_ref_commit_in_db(commit)
        if ref_commit is not None:
            for value in values:
                try:
                    list_value = value.split(':')
                    param = {list_value[0]: list_value[1]}
                    ref_commit.update(param) 
                except exceptions as e:
                    print(e)
        else:
            raise CommitNotFound
    except exceptions as e:
        print(e)

def post(commit):
    ref_commit = find_ref_commit_in_db(commit)
    if ref_commit is None:
        try:
            ref_commits.push({'commit': commit})
        except FirebaseError as e:
            print(e)
        except ValueError as e:
            print(e)
    else:
        raise CommitNotFound

def get(commit):
    ref_commit = find_ref_commit_in_db(commit)
    if ref_commit is not None:
        print(ref_commit.get())
    else:
        raise CommitNotFound

def delete(commit):
    ref_commit = find_ref_commit_in_db(commit)
    if ref_commit:
        ref_commit.delete()
    else:
        raise CommitNotFound

def put(values):
    try:
        commit = values.pop(0)
        delete(commit)
        post(commit)
        values.insert(0,commit)
        patch(values)
    except exceptions as e:
        print(e)

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
        node.delete()

def check_commit(commit):
    if re.fullmatch(r'[0-9a-z]{7}', commit):
        return True
    else:
        raise CommitSyntaxError

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
    values = args.patch
    patch(values)

elif args.put:
    values = args.put
    put(values)

restrict_db_size()
