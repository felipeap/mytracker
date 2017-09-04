from dbmongo import Database
import json
import pymongo

class Compareclass:
	
	def __init__(self):
		None
	
	def leitura(self):
		print "blaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
		json_query = {}
		sortby =[['proprietario', pymongo.ASCENDING]]
		cursor = Database().getdata(json_query, sortby, collection="Rastreadores")
		print cursor.count()
		listaProdutos = list(cursor)
		return listaProdutos