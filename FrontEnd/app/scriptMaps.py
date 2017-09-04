from datetime import datetime, timedelta
import pymongo

from Utils import Utils
from dbmongo import Database
from geopy.distance import great_circle

class Map_Data:
	def __init__(self, type=0, lat=0, lng=0, text=""):
		self.type = type
		self.lat = lat
		self.lng = lng
		self.text = text

class n1_MapaclassMaxPB:
    def __init__(self, serial=0,  dtsup=datetime(2099,1,1,1,1,1) ,dtinf=datetime(2010,1,1,1,1,1)):
        self.serial = serial
        self.dtinf  = dtinf
        self.dtsup  = dtsup
        self.gateways = []

    def leitura(self):
        StartDateInt = int(Utils().set_DatetimeToInt(self.dtinf))
        EndDateInt = int(Utils().set_DatetimeToInt(self.dtsup))

        json_query = {'dev_id': int(self.serial),'date_dev': {'$gte': self.dtinf, '$lte': self.dtsup}}
        sortby =[['date_dev', pymongo.ASCENDING]]
        print "pre db"
        cursor = Database().getdata(json_query, sortby, collection="Pontos")
        print cursor.count()
        lines = []
	first = True
        if cursor.count() > 0:
            for doc in cursor:
                gprs = Utils().get_gprsfix(doc)
                ignition = Utils().get_ignition(doc)
                evento = Utils().get_event(doc)
		pos = Utils().get_memoryindex(doc)

		if first or lastPos != pos:
			first = False
			lastPos = pos
                
	                speed = Utils().get_speed(doc)
	                gps  = Utils().get_gpsfix(doc)
	                date = Utils().get_devdate(doc)
	                # extPwr = Utils().get_extpower(doc)
	                # battery = Utils().get_battery(doc)
	                latitude = float(float(doc["lat"])/1000000)
	                longitude = float(float(doc["long"])/1000000)
	                stringInfo = "<b>Position</b>: " + str(pos) \
	                           + "<br><b>Event:</b> "    + str(evento)  \
	                           + "<br><b>Date:</b> "     + str(date) \
	                           + "<br><b>Ignition: </b> "  + str(ignition) \
	                           + "<br><b>Speed:</b> "  + str(speed) \
	                           + "<br><b>GPS Fix:</b> "  + str(gps) \
	                           + "<br><b>GPRS Fix:</b> "  + str(gprs)
	                           # + "<br><b>Battery:</b> "  + str(battery) \
	                           # + "<br><b>Ext Power:</b> "  + str(extPwr)
	                type = self.getType(doc)
	                mapdata = Map_Data(type, latitude, longitude, stringInfo)
	
	                route_reconstruct = doc["route_rec"]
	                if route_reconstruct.__len__() > 0:
	                    for rec_cursor in route_reconstruct:
	                        lat_rec   = float(float(rec_cursor["lat"])/1000000)
	                        long_rec  = float(float(rec_cursor["long"])/1000000)
	                        string_info_rec = "<b>Position : </b> "  + str(pos) \
	                                        + "<br><b>Date : </b> "  + str(rec_cursor["date"]) \
	                                        + "<br><b>Speed: </b> "  + str(rec_cursor["speed"])
	                        point_reconstruct = Map_Data(0, lat_rec, long_rec, string_info_rec)
	                        lines.append(point_reconstruct)
	                lines.append(mapdata.__dict__)

        return lines

    def getType(self, doc):
        gps = Utils().get_gpsfix(doc)
        gprs = Utils().get_gprsfix(doc)
        if Utils().isAccelerometerEvent(doc) == False:
            if gps == False and gprs == False:
                type = 1
            elif gps == False and gprs == True:
                type = 2
            elif gps == True and gprs == False:
                type = 3
            elif gps == True and gprs == True:
                type = 4
        else:
            if gps == False and gprs == False:
                type = 5
            elif gps == False and gprs == True:
                type = 6
            elif gps == True and gprs == False:
                type = 7
            elif gps == True and gprs == True:
                type = 8
        return type
    def isAccelerometerEvent(self, doc):
        return False


