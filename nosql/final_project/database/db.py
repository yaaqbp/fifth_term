from .magic_store.kv_idea.store import Store
import json
import xmltodict

class Database:
    def __init__(self, username, password):
        self.username = username
        self.store = Store()
        self.store.createNamespace(username)
        self.store.createUser('user', username, password)
        #self.store.login(username, password)
        #print(self.store._users)
        #print(self.store.users)

    
    def saveDoc(self, filepath, tags = []):
        """
        Put document to database. You can add gpx, txt or pdf file.
        """

        filetype = filepath.split('.')[-1]
        if filetype not in ['gpx', 'txt', 'pdf']:
            print('Incorrect file type')
            return 0
        elif filetype == 'gpx':
            with open(filepath) as xml_file:
                file = json.dumps(xmltodict.parse(xml_file.read()))
        elif filetype == 'txt':
            with open(filepath) as txt_file:
                file = txt_file.read()
        elif filetype == 'pdf':
            print('working on it')
            return 0
        filename = filepath.split('/')[-1]
        try:
            self.store.put(filename, file, tags = tags)
        except:
            print('Something went wrong')
            return 0
        print('file saved')

    def getDoc(self, tag: str):
        message = self.store.searchByTag(tag, namespace = self.username)
        keys = list(message['value'].keys())
        docs = []
        for key in keys:
            doc = self.store.get(key=key, namespace = self.username)['value']
            docs.append(doc)
        return docs

    def addTag(self, key, tag):
        try: 
            self.store.addTag(tag = tag, key = key, namespace = self.username)
            print('tag added')
        except:
            print('Something went wrong')
            return 0

    def removeTag(self, key, tag):
        try:
            self.store.removeTag(tag = tag, key = key, namespace = self.username)
            print('tag removed')
        except:
            print('Something went wrong')
            return 0



