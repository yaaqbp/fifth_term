import json
import uuid
from datetime import datetime
from ..constants import MESSAGES, EVENTS

class Store:
    def _createEvent(self, event_type, message = None):
        if event_type in EVENTS.TYPES:
            now = datetime.now().isoformat()
            if message is None:
                self._events.update({now:event_type})
            else:
                self._events.update({now:event_type+'-'+message})

    def __init__(self):
        self._store = {"__default__": {}}
        self._currentNamespace = None
        self._events = {}
        self._createEvent('init')

    def createNamespace(self, namespace):
        if namespace == "__default__":
            message = MESSAGES.INCORRECT_NAMESPACE
            self._createEvent('createNamespace', message=message['description'])
            return message

        self._store[namespace] = {}
        message = MESSAGES.OK
        self._createEvent('createNamespace', message=message['description'])
        return message


    def put(self, key, value, *, namespace = None, guard = None):
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
        message = MESSAGES.OK
        self._createEvent('put', message=message['description'])
        return message


    def get(self, key, *, namespace = None):
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

        return MESSAGES.ok(
            value,
            self._store[namespace][key]["guard"]
        )


    def delete(self, key, *, namespace = None, guard = None):
        namespace = self._checkNamespace(namespace)

        if namespace == None:
            return MESSAGES.INCORRECT_NAMESPACE

        if not(isinstance(key, str) and len(key)>0):
            return MESSAGES.INCORRECT_TYPE

        if not (namespace in self._store):
            return MESSAGES.INCORRECT_NAMESPACE

        if key in self._store[namespace]:
            v = self._store[namespace][key]

            if v["guard"] == guard:
                del self._store[namespace][key]
                return MESSAGES.OK
            else:
                return MESSAGES.INCORRECT_GUARD
        else:
            return MESSAGES.INCORRECT_KEY


    def save(self):
        file = open("db.json","w")
        json.dump(self._store, file)
        file.close()
        return MESSAGES.OK


    def load(self):
        file = open("db.json","r")
        self._store = json.load(file)
        file.close()
        return MESSAGES.OK


    def _checkNamespace(self, namespace):

        if namespace == "__default__":
            return None
        elif namespace == None:
            if not self._currentNamespace == None:
                return self._currentNamespace
            else:
                return "__default__"

        return namespace

    def _guardKVArgs(self, key, value):
        if isinstance(key, str) and len(key)>0:
            return True
        else:
            return False