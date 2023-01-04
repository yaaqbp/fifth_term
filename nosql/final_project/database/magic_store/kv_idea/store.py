import json
import uuid
from datetime import datetime
from ..constants import MESSAGES, EVENTS, USERS

class Store:
    def _checkPermission(self, event_type):
        if event_type in USERS.PERMISSIONS.get(self.currentUserType):
            return True
        return False


    def _createEvent(self, event_type, message = None):
        if event_type in EVENTS.TYPES:
            now = datetime.now().isoformat()
            if message is None:
                self._events.update({now:event_type})
            else:
                self._events.update({now:event_type+'-'+message})


    def createUser(self, usertype: str, username: str, password: str):
        if not self._checkPermission('createUser'):
            message = MESSAGES.INCORRECT_PERMISSION
            self._createEvent('createUser', message=message['description'])
            return message
        if usertype in USERS.PERMISSIONS.keys() and usertype != 'admin':
            if username not in self._users.keys():
                self._users.update({username:password})
                self.users.update({username:usertype})
                message = MESSAGES.OK
                self._createEvent('createUser', message=message['description'])
                return message
            else:
                message = MESSAGES.INCORRECT_USERNAME
                self._createEvent('createUser', message=message['description'])
                return message
        else:
            message = MESSAGES.INCORRECT_USERTYPE
            self._createEvent('createUser', message=message['description'])
            return message


    def login(self, username: str, password: str):
        if username in self._users.keys():
            if self._users.get(username) == password:
                self.currentUser = username
                self.currentUserType = self.users.get(username)
                message = MESSAGES.OK
                self._createEvent('login', message=message['description'])
                return message
            else:
                message = MESSAGES.INCORRECT_PASSWORD
                self._createEvent('login', message=message['description'])
                return message
        else:
            message = MESSAGES.INCORRECT_USERNAME
            self._createEvent('login', message=message['description'])
            return message


    def __init__(self):
        self._store = {"__tags__": {}}
        self._currentNamespace = None
        self._events = {}
        self._createEvent('init')
        #here will be dict username:password
        self._users = {'admin':'admin'}
        #here will be dict username:usertype
        self.users = {'admin':'admin'}
        self.currentUser = 'admin'  
        self.currentUserType = 'admin'


    def createNamespace(self, namespace: str):
        if not self._checkPermission('createNamespace'):
            message = MESSAGES.INCORRECT_PERMISSION
            self._createEvent('createNamespace', message=message['description'])
            return message
        if namespace == "__tags__":
            message = MESSAGES.INCORRECT_NAMESPACE
            self._createEvent('createNamespace', message=message['description'])
            return message

        self._store[namespace] = {}
        self._currentNamespace = namespace
        message = MESSAGES.OK
        self._createEvent('createNamespace', message=message['description'])
        return message

        
    def _createTag(self, tag):
        self._store['__tags__'][tag] = {}


    def put(self, key: str, value: str, namespace = None, guard = None, tags = []):
        if not self._checkPermission('put'):
            message = MESSAGES.INCORRECT_PERMISSION
            self._createEvent('put', message=message['description'])
            return message
        namespace = self._checkNamespace(namespace)
        if namespace == None:
            message = MESSAGES.INCORRECT_NAMESPACE
            self._createEvent('put', message=message['description'])
            return message

        if not self._guardKVArgs(key, value):
            message = MESSAGES.INCORRECT_TYPE
            self._createEvent('put', message=message['description'])
            return message

        if not (namespace in self._store):
            self.createNamespace(namespace)
            #self._currentNamespace = namespace

        if key in self._store[namespace]:
            v = self._store[namespace][key]

            if v["guard"] == guard:
                v["guard"] = uuid.uuid4().hex
                v["value"] = value
            else:
                message = MESSAGES.INCORRECT_GUARD
                self._createEvent('put', message=message['description'])
                return message
        else:
            self._store[namespace][key] = {"guard": uuid.uuid4().hex, "value": value}
        for tag in tags:
            if not tag in self._store['__tags__']:
                self._createTag(tag)
            if namespace not in self._store['__tags__'][tag]:
                self._store['__tags__'][tag][namespace] = {key:True}
            else:
                self._store['__tags__'][tag][namespace][key] = True
        message = MESSAGES.OK
        self._createEvent('put', message=message['description'])
        return message


    def get(self, key: str, *, namespace = None):
        if not self._checkPermission('get'):
            message = MESSAGES.INCORRECT_PERMISSION
            self._createEvent('get', message=message['description'])
            return message
        namespace = self._checkNamespace(namespace)

        if namespace == None:
            message = MESSAGES.INCORRECT_NAMESPACE
            self._createEvent('get', message=message['description'])
            return message

        if not(isinstance(key, str) and len(key)>0):
            message = MESSAGES.INCORRECT_TYPE
            self._createEvent('get', message=message['description'])
            return message

        if not (namespace in self._store):
            message = MESSAGES.INCORRECT_NAMESPACE
            self._createEvent('get', message=message['description'])
            return message

        if not (key in self._store[namespace]):
            message = MESSAGES.INCORRECT_KEY
            self._createEvent('get', message=message['description'])
            return message

        value = None
        if isinstance(self._store[namespace][key]["value"], dict) or \
           isinstance(self._store[namespace][key]["value"], list):
            value = self._store[namespace][key]["value"].copy()
        else:
            value = self._store[namespace][key]["value"]

        message = MESSAGES.ok(
            value,
            self._store[namespace][key]["guard"]
        )
        self._createEvent('get', message=message['description'])
        return message


    def delete(self, key: str, *, namespace = None, guard = None):
        if not self._checkPermission('delete'):
            message = MESSAGES.INCORRECT_PERMISSION
            self._createEvent('delete', message=message['description'])
            return message
        namespace = self._checkNamespace(namespace)
        if namespace == None:
            message = MESSAGES.INCORRECT_NAMESPACE
            self._createEvent('delete', message=message['description'])
            return message

        if not(isinstance(key, str) and len(key)>0):
            message = MESSAGES.INCORRECT_TYPE
            self._createEvent('delete', message=message['description'])
            return message

        if not (namespace in self._store):
            message = MESSAGES.INCORRECT_NAMESPACE
            self._createEvent('delete', message=message['description'])
            return message

        if key in self._store[namespace]:
            v = self._store[namespace][key]
            if v["guard"] == guard:
                del self._store[namespace][key]
                message = MESSAGES.OK
                self._createEvent('delete', message=message['description'])
                return message
            else:
                message = MESSAGES.INCORRECT_GUARD
                self._createEvent('delete', message=message['description'])
                return message
        else:
            message = MESSAGES.INCORRECT_KEY
            self._createEvent('delete', message=message['description'])
            return message



    def searchByTag(self, tag: str, namespace=None):
        """if not self._checkPermission('searchByTag'):
            message = MESSAGES.INCORRECT_PERMISSION
            self._createEvent('searchByTag', message=message['description'])
            return message"""
        namespace = self._checkNamespace(namespace)
        if namespace == None or namespace == '__tags__' or not (namespace in self._store):
            message = MESSAGES.INCORRECT_NAMESPACE
            self._createEvent('searchByTag', message=message['description'])
            return message

        if not(isinstance(tag, str) and len(tag)>0):
            message = MESSAGES.INCORRECT_TYPE
            self._createEvent('searchByTag', message=message['description'])
            return message

        if not (tag in self._store['__tags__']):
            message = MESSAGES.INCORRECT_TAG
            self._createEvent('searchByTag', message=message['description'])
            return message

        dct = {key:True for key in self._store['__tags__'][tag][namespace].keys()}
        message = MESSAGES.ok(dct)
        self._createEvent('searchByTag', message=message['description'])
        return message


    def save(self):
        if not self._checkPermission('save'):
            message = MESSAGES.INCORRECT_PERMISSION
            self._createEvent('save', message=message['description'])
            return message
        file = open("db.json","w")
        json.dump(self._store, file)
        file.close()
        message = MESSAGES.OK
        self._createEvent('save', message=message['description'])
        return message


    def load(self):
        if not self._checkPermission('load'):
            message = MESSAGES.INCORRECT_PERMISSION
            self._createEvent('load', message=message['description'])
            return message
        file = open("db.json","r")
        self._store = json.load(file)
        file.close()
        message = MESSAGES.OK
        self._createEvent('load', message=message['description'])
        return message


    def saveEvents(self):
        if not self._checkPermission('saveEvents'):
            message = MESSAGES.INCORRECT_PERMISSION
            self._createEvent('saveEvents', message=message['description'])
            return message
        message = MESSAGES.OK
        self._createEvent('saveEvents', message=message['description'])
        with open('events.log','w') as f:
            for k, v in self._events.items():
                f.write(f'{k} {v}\n')
        return message


    def _checkNamespace(self, namespace):
        if namespace == "__tags__":
            return None
        elif namespace == None:
            if not self._currentNamespace == None:
                return self._currentNamespace
            else:
                return "__tags__"
        return namespace


    def _guardKVArgs(self, key, value):
        if isinstance(key, str) and len(key)>0:
            return True
        else:
            return False
"""
    def showPermissons(self):
        return USERS.PERMISSIONS[self.currentUser]
    """