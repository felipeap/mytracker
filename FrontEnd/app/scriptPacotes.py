from datetime import datetime, timedelta
import pymongo

from Utils import Utils
from dbmongo import Database
from geopy.distance import great_circle

class Pacote_Data:
    def __init__(self, deviceID=0, seqNumber=0, reason=0, datetime=0, gtwDate=0, ignition=0, gpsFix = 0, gprsFix = 0, lat=0, lng=0, moving=0, speed=0, csq=0, extPower=0, battery=0, batteryState=0, uptime=0, hdop=0, snr=0, svn=0):
        self.deviceID = deviceID
        self.seqNumber = seqNumber
        self.reason = reason
        self.datetime = datetime
        self.unixTime = 0
        self.gtwDate = gtwDate
        self.ignition = ignition
        self.gpsFix = gpsFix
        self.gprsFix = gprsFix
        self.lat = lat
        self.long = lng
        self.moving = moving
        self.speed = speed
        self.csq = csq
        self.extPower = extPower
        self.battery = battery
        self.batteryState = batteryState
        self.uptime = uptime
        self.hdop = hdop
        self.snr = snr
        self.svn = svn


class n1_PacotesclassMaxPB:
    def __init__(self, serial=0,  dtsup=datetime(2099,1,1,1,1,1) ,dtinf=datetime(2010,1,1,1,1,1)):
        self.serial = serial
        self.dtinf  = dtinf
        self.dtsup  = dtsup

    def leitura(self):
        StartDateInt = int(Utils().set_DatetimeToInt(self.dtinf))
        EndDateInt = int(Utils().set_DatetimeToInt(self.dtsup))

        json_query = {'deviceID': int(self.serial),'dateTime': {'$gte': StartDateInt, '$lte': EndDateInt}}
        sortby =[['dateTime', pymongo.DESCENDING]]
        cursor = Database().getdata(json_query, sortby, collection="DataMaxPB")

        print cursor.count()
        lines = []
        if cursor.count() > 0:
            for doc in cursor:
                pacoteData = Pacote_Data()

                pacoteData.deviceID = int(self.serial)
                pacoteData.seqNumber = Utils().get_memoryindex(doc)
                pacoteData.reason = Utils().get_event(doc)
                pacoteData.datetime = Utils().get_devdate(doc)
                pacoteData.unixTime = doc["dateTime"]
                pacoteData.gtwDate = Utils().get_gtwdate(doc)
                pacoteData.ignition = Utils().get_ignition(doc)
                pacoteData.gpsFix = Utils().get_gpsfix(doc)
                pacoteData.gprsFix = Utils().get_gprsfix(doc)
                pacoteData.lat = float(float(doc["positionInfo"][0]["latitude"])/10000000)
                pacoteData.long = float(float(doc["positionInfo"][0]["longitude"])/10000000)
                pacoteData.moving = Utils().get_gsensor(doc)
                pacoteData.speed = Utils().get_speed(doc)
                pacoteData.csq = Utils().get_csq(doc)
                pacoteData.extPower = Utils().get_extpower(doc)
                pacoteData.battery = Utils().get_battery(doc)
                pacoteData.batteryState = Utils().get_batteryState(doc)
                pacoteData.uptime = Utils().get_uptime(doc)
                pacoteData.hdop = Utils().get_hdop(doc)
                pacoteData.snr = Utils().get_snr(doc)
                pacoteData.svn = Utils().get_svn(doc)
                lines.append(pacoteData.__dict__)

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
    def calculaDistancia(self, lat, long):
        latref  = -19.984357 #Latlong da Denox
        longref = -43.947501
        referencia = (longref, latref)
        ponto = (long, lat)
        distance = int(great_circle(referencia, ponto).meters)
        return distance