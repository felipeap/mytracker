import json
__author__ = 'felipepereira'

from pymongo import MongoClient
import pymongo
import json
from pprint import pprint

class Database:
	client = None
	db = None
	pesquisa = None

	def __init__(self):
		if self.client is None:
			self.client = MongoClient('localhost:27017')
			self.db = self.client["MyTracker"]
			self.pesquisa = self.db["LinhaMXT"]
			#self.pesquisa = self.db[collection]

	def getdata(self, query, sortby, collection):
		self.__init__()
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

	def update(self, query, field, newValue, collection):
		self.pesquisa = self.db[collection]
		for p in self.pesquisa.find(query):
			for k,v in p.iteritems():
				value=v[field]
				v[field]=newValue