from bson import json_util
from datetime import datetime

__author__ = 'felipepereira'

from pymongo import MongoClient
import json
from pprint import pprint

class Database:
    conn = None

    def __init__(self):
        if self.conn is None:
            self.conn = MongoClient('localhost:27017')

    def add2(self, data, col):
        self.__init__()
        # r_json = json.dumps(data.__dict__, default=json_util.default)
        r_json = json.dumps(data, default=json_util.default)
        r_json = json.loads(r_json, object_hook=json_util.object_hook)
        #pprint (r_json)
        database   = self.conn["MyTracker"]
        collection = database[col]
        collection.insert(r_json)

    def addInfoMTC(self, data, col):
        self.__init__()
        info = Information()
        info.prot = data['protocol']
        info.devDate = datetime.strptime(data['setup_record_date'], '%Y-%m-%d %H:%M:%S')
        info.serial = data['serial']
        info.vApp = data['firmware_version']

        r_json = json.dumps(info.__dict__, default=json_util.default)
        r_json = json.loads(r_json, object_hook=json_util.object_hook)
        database   = self.conn["LogAnalyzer"]
        collection = database[col]
        collection.insert(r_json)

    def addInfoMXT(self, data, col):
        self.__init__()
        info = Information()

        info.prot = data['header']['protocol']
        info.devDate = datetime.strptime(data['header']['timestamp'], '%Y-%m-%d %H:%M:%S')
        info.serial = data['header']['serial']
        info.vApp = data['application_version']
        info.vMod = data['modem_version']

        r_json = json.dumps(info.__dict__, default=json_util.default)
        r_json = json.loads(r_json, object_hook=json_util.object_hook)
        database   = self.conn["LogAnalyzer"]
        collection = database[col]
        collection.insert(r_json)

    def getdata(self, query, sortby, collection):
        self.client = MongoClient('localhost:27017')
        self.db = self.client["LogAnalyzer"]
        self.pesquisa = self.db["LinhaMXT"]
        self.pesquisa = self.db[collection]
        if sortby != 0:
            return self.pesquisa.find(query).sort(sortby)
        else:
            return self.pesquisa.find(query)

    def getLimiteddata(self,limite, query, sortby, collection):
        self.__init__()
        self.pesquisa = self.db[collection]
        if sortby != 0:
            return self.pesquisa.find(query).sort(sortby).limit(limite)
        else:
            return self.pesquisa.find(query)

class Information:
        def __init__(self):
            self.prot = 0
            self.serial = 0
            self.vApp = ""
            self.vMod = ""
            self.devDate = 0

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            print obj.isoformat()
            return obj.isoformat()
            # return obj.strftime("ISODate(%Y-%m-%d %H:%M:%S)")
            # return obj.strftime('%Y-%m-%d %H:%M:%S')
        # elif isinstance(obj, date):
        #     return obj.isoformat()
            # return obj.strftime('%Y-%m-%d')
        # Let the base class default method raise the TypeError
        return json_util.default