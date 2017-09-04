import binascii
import crcmod.predefined
from dbmongo import *
import datetime


class PacoteMXT:

    def __init__(self, pacote_bruto):
        self.pacote_bruto = binascii.hexlify(pacote_bruto)
        self.pacote_data = ''       #Pacote Sem Byte Stuffing e CRC
        self.crc_received = ''
        self.crc_calculated = ''

        self.gtw_datetime = datetime.datetime.now()
        self.MXT_dd = ''  # 1 byte
        self.MXT_mt = ''  # 1 byte
        self.MXT_id_bin = ''
        self.MXT_id_int = ''  # 4 bytes
        self.MXT_data   = ''  # x bytes (resto do pacote_data)

        self.MXT_protocol   = '' # 1 byte
        self.MXT_info_group = '' # 1 byte
        self.MXT_position   = 0 # 2 bytes
        self.MXT_datetime   = 0 # 4 bytes
        self.MXT_latitude   = 0 # 4 bytes
        self.MXT_longitude  = 0 # 4 bytes

        # Flags
        self.MXT_flags      = 0 # 4 bytes
        self.MXT_flag_ignition = 0  # 1 bit
        self.MXT_flag_gprsfix = 0   # 1 bit
        self.MXT_flag_gpsfix = 0    # 1 bit

        self.MXT_speed      = 0 # 1 byte
        self.MXT_GPSinfo    = 0 # 8 bytes

        self.MXT_odometer = 0 # 4 bytes
        self.MXT_event    = 0 # 4 bytes
        self.pacote_ack = ''

        self.MXT_ND_qty  = 0
        self.MXT_ND_type = 0

        self.list_points_reconstruct = []

        self.remove_byteStuf()
        self.crc_calculated = self.calcula_CRC(self.pacote_data)
        if self.quebra_pacote():
            self.exibir_infos()
            self.save_position_mongo()
        self.envia_ack()


    def quebra_pacote(self):
        self.MXT_dd = self.pacote_data[0:2]
        self.MXT_mt = self.pacote_data[2:4]
        if self.MXT_mt == '31':
            self.MXT_id_bin = self.pacote_data[4:12]
            self.MXT_id_int = int(self.inverte_bytes(self.MXT_id_bin),16)
            self.MXT_protocol = self.pacote_data[12:14]
            self.MXT_info_group = self.pacote_data[14:16]
            self.MXT_position = int(self.inverte_bytes(self.pacote_data[16:20]),16)
            self.MXT_datetime  = self.inverte_bytes(self.pacote_data[20:28])
            self.MXT_datetime = self.converte_datetime(self.MXT_datetime)

            # self.MXT_latitude  = self.inverte_bytes(self.pacote_data[28:36])
            self.MXT_latitude  = self.converte_two_complement(self.pacote_data[28:36], 32)

            # self.MXT_longitude = self.inverte_bytes(self.pacote_data[36:44])
            self.MXT_longitude = self.converte_two_complement(self.pacote_data[36:44], 32)

            self.MXT_flags = self.inverte_bytes(self.pacote_data[44:52])
            self.MXT_flag_ignition = self.retorna_flag(self.MXT_flags, 0)
            self.MXT_flag_gprsfix  = self.retorna_flag(self.MXT_flags, 13)
            self.MXT_flag_gpsfix   = self.retorna_flag(self.MXT_flags, 15)

            self.MXT_speed = int(self.pacote_data[52:54],16)
            # input mask[54:56];
            index_info_group = 56
            self.MXT_GPSinfo = self.inverte_bytes(self.pacote_data[index_info_group : index_info_group + 16])
            self.MXT_odometer= int(self.inverte_bytes(self.pacote_data[index_info_group + 16 : index_info_group + 24]),16)
            self.MXT_event   = int(self.inverte_bytes(self.pacote_data[index_info_group + 24 : index_info_group + 32]),16)

            # NEW DATA (pg 169 do protocolo)
            index_new_data = index_info_group + 32
            if self.MXT_protocol == '18':
                self.MXT_ND_qty  =  int(self.pacote_data[index_new_data + 0 : index_new_data + 2],16)
                pointer = index_new_data + 2
                for x in range(0,self.MXT_ND_qty):
                    MXT_ND_type =                                self.pacote_data[pointer     : pointer + 2]
                    MXT_ND_size =         int(self.inverte_bytes(self.pacote_data[pointer + 2 : pointer + 6]),16)
                    self.quebra_newdata(MXT_ND_type, MXT_ND_size,self.pacote_data[pointer + 6 : pointer + 6 + (MXT_ND_size*2)])
                    pointer += 6 + (MXT_ND_size*2)
            return True
        else:
            return False

    def quebra_newdata(self, type, size, newdata):
        # print "***************************************************************************************  Quebra New Data"
        print type
        print size
        print newdata
        if type == '12':
            # initial_lat  = self.inverte_bytes(newdata[ 0:8 ])
            initial_lat  = self.converte_two_complement(newdata[ 0:8 ], 32)
            initial_long = self.converte_two_complement(newdata[ 8:16], 32)

            initial_date = self.inverte_bytes(newdata[16:24])
            initial_date = self.converte_datetime(initial_date)
            initial_speed= int(newdata[24:26],16)
            num_sections = int(newdata[26:28],16)
            # print initial_lat
            # print initial_long
            # print initial_date
            # print num_sections
            tmp_point   = Route_Reconstruct( (initial_lat), (initial_long), initial_date, initial_speed)
	    first_point = Route_Reconstruct( (initial_lat), (initial_long), initial_date, initial_speed)
            self.list_points_reconstruct.append(first_point.__dict__)

            # Calcula todos pontos de reconstrucao
            ptr = 28
            last_point = tmp_point
            for x in range(0, num_sections):
                section = newdata[ptr:ptr+10]
                # print "Sec " + str(x) + " - " + section
                #point = Route_Reconstruct()
                tmp_lat = self.converte_two_complement(section[0:2], 8)
                tmp_lng = self.converte_two_complement(section[2:4], 8)
                tmp_speed = int(section[ 4:6 ],16)
                tmp_date  = int(self.inverte_bytes(section[ 6:10]),16)

                last_point.lat   = tmp_point.lat   + (tmp_lat*10)
                last_point.long  = tmp_point.long  + (tmp_lng*10)
                last_point.speed = tmp_speed
                last_point.date  = tmp_point.date + datetime.timedelta(seconds=tmp_date)

                point = Route_Reconstruct(last_point.lat, last_point.long, last_point.date, last_point.speed)
                self.list_points_reconstruct.append(point.__dict__)
                ptr += 10

    def save_position_mongo(self):
        print "Grava no Mongo"
        obj = Dados_uteis(self.pacote_bruto,
                          self.gtw_datetime,
                          self.MXT_datetime,
                          self.MXT_position,
                          self.MXT_id_int,
                          self.MXT_latitude,
                          self.MXT_longitude,
                          self.MXT_speed,
                          self.MXT_flag_ignition,
                          self.MXT_flag_gpsfix,
                          self.MXT_flag_gprsfix,
                          self.MXT_odometer,
                          self.MXT_event,
                          self.list_points_reconstruct)
        obj.to_mongo()

    def envia_ack(self):
        pacote_ack = self.MXT_dd + '02' + self.MXT_id_bin + self.crc_received
        crc_ack = self.calcula_CRC(pacote_ack)
        pacote_ack = '01' + pacote_ack + crc_ack + '04'
        self.pacote_ack = binascii.unhexlify(pacote_ack.lower())
        # print "- ACK: " + self.pacote_ack

    def exibir_infos(self):

        print "Date Gateway: " + str(self.gtw_datetime)
        print "Date Pacote : " + str(self.MXT_datetime)
        # print "Pacote Bruto: " + self.pacote_bruto
        # print "Pacote Data : " + self.pacote_data
        # print "CRC recv    : " + self.crc_received
        # print "CRC calc    : " + self.crc_calculated
        #
        # print "dd :  " + self.MXT_dd
        # print "mt :  " + self.MXT_mt
        print "protocol:     " + self.MXT_protocol
        # print "info group: " + self.MXT_info_group

        print "id :  " + str(self.MXT_id_int)
        print "pos:  " + str(self.MXT_position)

        print "lat:  " + str(self.MXT_latitude)
        print "long: " + str(self.MXT_longitude)

        print "ign:      " + str(self.MXT_flag_ignition)
        # print "gprs fix: " + str(self.MXT_flag_gprsfix)
        # print "gps fix:  " + str(self.MXT_flag_gpsfix)

        # print "speed:    " + str(self.MXT_speed)
        # print "flags " + str(self.MXT_flags)

        # print "gps info: " + str(self.MXT_GPSinfo)
        # print "odom:     " + str(self.MXT_odometer)
        print "evento:   " + str(self.MXT_event)

        for x in self.list_points_reconstruct:
            print "Section "
            print "Lat:  " + str(x["lat"])
            print "Long: " + str(x["long"])
            print "Speed:" + str(x["speed"])
            print "Date: " + str(x["date"])

    def retorna_flag(self, bitmap, position):
        temp = int(bitmap,16)
        temp = temp >> position
        temp = temp & 0x01
        if temp == 0x1:
            return True
        else:
            return False

    def converte_two_complement(self, latlong_bin, bits):
        latlong_bin = self.inverte_bytes(latlong_bin)

        temp = bin(int(latlong_bin,16)).replace('0b','').zfill(bits)
        temp2 = ''
        if(temp[0] == '1'):
            for x in temp:
                if x == '0':
                    temp2 = temp2 + '1'
                else:
                    temp2 = temp2 + '0'
            temp = (int(temp2,2) + 1 )*(-1)
        else:
            temp = int(temp,2)
        return temp

    def converte_datetime(self, date_to_convert):
        dataRef = datetime.datetime(year=2000, month=1, day=1)
        temp = int(date_to_convert,16)
        temp2= bin(temp).replace('0b','').zfill(32)
        dias    = int(temp2[0:15],2)
        horas   = int(temp2[15:20], 2)
        minutos = int(temp2[20:26], 2)
        segundos= int(temp2[26:32], 2)
        date_to_convert = dataRef + datetime.timedelta(days=dias, hours=horas, minutes=minutos, seconds=segundos)
        return date_to_convert

    # CRC_CCITT
    def calcula_CRC(self, dados):
        pacote = binascii.unhexlify(dados)
        crc16 = crcmod.predefined.Crc('xmodem')
        crc16.update(pacote)
        inverteCRC = crc16.hexdigest()
        i = 4
        CRC = ''
        while (i > 0):
            CRC = CRC + inverteCRC[i - 2:i]
            i = i - 2
        return CRC

    def remove_byteStuf(self):
        # pacote = binascii.hexlify(self.pacote_bruto)
        pacote = self.pacote_bruto[2: len(self.pacote_bruto) - 2]

        iteration = iter(range(0, pacote.__len__(), 2))
        for x in iteration:
            if (pacote[x:(x + 2)]) == '10':
                if (pacote[x + 2:(x + 4)]) == '21':
                    self.pacote_data = self.pacote_data + '01'

                elif (pacote[x + 2:(x + 4)]) == '24':
                    self.pacote_data = self.pacote_data + '04'

                elif (pacote[x + 2:(x + 4)]) == '30':
                    self.pacote_data = self.pacote_data + '10'

                elif (pacote[x + 2:(x + 4)]) == '31':
                    self.pacote_data = self.pacote_data + '11'

                elif (pacote[x + 2:(x + 4)]) == '33':
                    self.pacote_data = self.pacote_data + '13'
                next(iteration)
            else:
                self.pacote_data = self.pacote_data + pacote[x:(x + 2)]
        self.crc_received = self.pacote_data [self.pacote_data .__len__()-4:].upper()
        self.pacote_data = self.pacote_data [0:self.pacote_data .__len__()-4]
        return

    def inverte_bytes(self, bytes):
        temp = ''
        for x in range(bytes.__len__(), 0, -2):
            temp = temp + bytes[x-2:x]
        return temp


class Route_Reconstruct:
    def __init__(self, lat, long, date, speed):
        self.lat = lat
        self.long = long
        self.speed = speed
        self.date = date

class Dados_uteis:
    def __init__(self, pacote_bruto, date_gtw, date_dev, pos, dev_id, lat, long, speed, ign, gpsfix, gprsfix, odometer, event, route_reconstruct):
        self.pacote_bruto = pacote_bruto
        self.date_gtw = date_gtw
        self.date_dev = date_dev
        self.dev_id   = dev_id
        self.pos      = pos
        self.lat      = lat
        self.long     = long
        self.speed    = speed
        self.ign      = ign
        self.gpsfix   = gpsfix
        self.gprsfix  = gprsfix
        self.odometer = odometer
        self.event    = event
        self.route_rec= route_reconstruct

    def to_mongo(self):
        print "Salvando no Banco"

        Database().add2(self.__dict__,"Pontos")
