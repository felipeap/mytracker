from datetime import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import *
from geopy.distance import great_circle
import pymongo


styles = getSampleStyleSheet()
style = TableStyle([   ('ALIGN',(0,0),(-1,-1),'CENTER'),
                               ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ('INNERGRID', (0,0),(-1,-1), 0.25, colors.black),
                               ('FONT',(0,0),(0,-1),'Helvetica-Bold'),
                               ('FONT',(0,0),(-1,0),'Helvetica-Bold'),
                               ('FONTSIZE', (0,0), (-1, -1), 8),
                               ('BACKGROUND',(0,0),(0,-1),colors.lightgrey),
                               ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                               ('FONTSIZE',(0,0),(0,-1),9),
                               ('FONTSIZE',(0,0),(-1,0),9),
                               ])
stylepeq = TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                               ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ('INNERGRID', (0,0),(-1,-1), 0.25, colors.black),
                               ('BACKGROUND',(0,0),(0,-1),colors.lightgrey),
                               ('FONT',(0,0),(0,-1),'Helvetica-Bold'),
                               ])
heading = styles["Heading1"]
heading.wordWrap = 'CJK'
normal = styles["Normal"]
class Utils:
    def __init__(self):
        None

    def NumProtocol_to_product(self, protocol):
        if protocol == 1:
            return "MTC"
        elif protocol == 166 or protocol == 167 or protocol == 172 or protocol == 168:
            return "MXT"
        elif protocol == 173:
            return "MaxPB"

    def protocol_to_product(self, doc):
        try:
            a = doc["deviceID"]
            return "MaxPB"
        except:
            protocol = self.get_protocol(doc)
            if protocol == 1:
                return "MTC"
            elif protocol == 166 or protocol == 167 or protocol == 172 or protocol == 168:
                return "MXT"
            else:
                return "Error"

    def numprotocol_to_product(self, protocol):
        if protocol == 1:
            return "MTC"
        elif protocol == 166 or protocol == 167 or protocol == 172 or protocol == 168:
            return "MXT"
        else:
            return "MaxPB"

    def get_event(self, doc):
        return doc["event"]

    def isAccelerometerEvent(self, doc):
        protocol= self.get_protocol(doc)
        product = self.protocol_to_product(doc)
        if product == "MXT" :
            event = self.get_event(doc)
            if event == 100:
                return True
            else:
                return False
        elif product == "MTC":
            try:
                x = int(doc["accelerometer_data"]["data"]["flag_value"])
                if x > 0:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

    def existsCANdata(self, doc):
        protocol= self.get_protocol(doc)
        product = self.protocol_to_product(doc)
        if product == "MXT" :
            try:
                a = doc["additional_data"]["position_information"]
                return True
            except:
                return False
        elif product == "MTC":
                return False

    def CANdataInfo(self, doc):
        stringCAN =  "<br><br><b>CAN DATA: </b>"
        protocol= self.get_protocol(doc)
        product = self.protocol_to_product(doc)
        # ANALOG DATA
        speedCAN = self.get_speedCAN(doc)
        RPM = self.get_rpm(doc)
        odometerCAN = self.get_odometer(doc)
        airtemperature = self.get_air_temperature(doc)
        fuelconsumption = self.get_fuel_consumption(doc)
        fuelLevel1 = self.get_fuel_level1(doc)
        fuelLevel2 = self.get_fuel_level2(doc)
        engineTemperature = self.get_engine_temperature(doc)
        windowWipers = self.get_windshield_wipers(doc)
        engineFuelRate = self.get_engine_fuel_rate(doc)
        intakeAirTemp = self.get_intake_air_temp(doc)
        intakeAirFlow = self.get_intake_air_flow(doc)
        throttlePosition = self.get_throttle_position(doc)
        barometricPressure = self.get_barometric_pressure(doc)
        controlModuleVoltage = self.get_control_module_voltage(doc)
        fuelType = self.get_fuel_type(doc)
        ethanolRatio = self.get_ethanol_ratio(doc)
        oilTemperature = self.get_oil_temperature(doc)
        engineRefTorque = self.get_engine_ref_torque(doc)
        currentGear = self.get_current_gear(doc)

        # DIGITAL DATA
        clutchDigital = self.get_clutch(doc)
        brakeDigital = self.get_brake(doc)
        parkingBrakeDigital = self.get_parking_brake(doc)
        motorBrakeDigital = self.get_motor_brake(doc)
        doorClosedDigital = self.get_door_closed(doc)
        doorLockedDigital = self.get_door_locked(doc)
        numDTCavailable = self.get_num_dtc_available(doc)
        numDTCpacket = self.get_num_dtc_packet(doc)

        if product == "MXT" :
            if airtemperature != -1 :
                stringCAN = stringCAN + "<br<b>Air Temperature: </b> " + str(airtemperature)

            if fuelconsumption != -1 :
                stringCAN = stringCAN + "<br><b>Fuel Consumption: </b> " + str(fuelconsumption)

            if fuelLevel1 != -1 :
                stringCAN = stringCAN + "<br<b>Fuel Level 1: </b> " + str(fuelLevel1)

            if fuelLevel2 != -1 :
                stringCAN = stringCAN + "<br><b>Fuel Level 2: </b> " + str(fuelLevel2)

            if engineTemperature != -1 :
                stringCAN = stringCAN + "<br<b>Air Temperature: </b> " + str(engineTemperature)

            if windowWipers != -1 :
                stringCAN = stringCAN + "<br><b>Windshield Wipers: </b> " + str(windowWipers)

            if engineFuelRate != -1 :
                stringCAN = stringCAN + "<br<b>Air Temperature: </b> " + str(engineFuelRate)

            if intakeAirTemp != -1 :
                stringCAN = stringCAN + "<br><b>Fuel Consumption: </b> " + str(intakeAirTemp)

            if intakeAirFlow != -1 :
                stringCAN = stringCAN + "<br<b>Air Temperature: </b> " + str(intakeAirFlow)

            if throttlePosition != -1 :
                stringCAN = stringCAN + "<br><b>Fuel Consumption: </b> " + str(throttlePosition)

            if barometricPressure != -1 :
                stringCAN = stringCAN + "<br<b>Air Temperature: </b> " + str(barometricPressure)

            if controlModuleVoltage != -1 :
                stringCAN = stringCAN + "<br><b>Control Module Voltage: </b> " + str(controlModuleVoltage)

            if fuelType != -1 :
                stringCAN = stringCAN + "<br><b>Fuel Type: </b> " + str(fuelType)

            if ethanolRatio != -1 :
                stringCAN = stringCAN + "<br><b>Ethanol Ratio: </b> " + str(ethanolRatio)

            if oilTemperature != -1 :
                stringCAN = stringCAN + "<br><b>Oil Temperature: </b> " + str(oilTemperature)

            if engineRefTorque != -1 :
                stringCAN = stringCAN + "<br><b>Engine Ref Torque: </b> " + str(engineRefTorque)

            if currentGear != -1 :
                stringCAN = stringCAN + "<br><b>Current Gear: </b> " + str(currentGear)

            if clutchDigital != -1 :
                stringCAN = stringCAN + "<br><b>Clutch Digital: </b> " + str(clutchDigital)

            if brakeDigital != -1 :
                stringCAN = stringCAN + "<br><b>Brake Digital: </b> " + str(brakeDigital)

            if parkingBrakeDigital != -1 :
                stringCAN = stringCAN + "<br><b>Parking Brake: </b> " + str(parkingBrakeDigital)

            if motorBrakeDigital != -1 :
                stringCAN = stringCAN + "<br><b>Motor Brake: </b> " + str(motorBrakeDigital)

            if doorClosedDigital != -1 :
                stringCAN = stringCAN + "<br><b>Door Closed : </b> " + str(doorClosedDigital)

            if doorLockedDigital != -1 :
                stringCAN = stringCAN + "<br><b>Door Locked: </b> " + str(doorLockedDigital)

            if numDTCavailable != -1 :
                stringCAN = stringCAN + "<br><b>Num DTC: </b> " + str(numDTCavailable)

            if numDTCpacket != -1 :
                stringCAN = stringCAN + "<br><b>Fuel Consumption: </b> " + str(numDTCpacket)

            if speedCAN != -1 :
                stringCAN = stringCAN + "<br><b>Speed: </b> " + str(speedCAN)

            if RPM != -1 :
                stringCAN = stringCAN + "<br><b>RPM: </b> " + str(RPM)

            if odometerCAN != -1 :
                stringCAN = stringCAN + "<br><b>Fuel Consumption: </b> " + str(odometerCAN)
            return stringCAN

    def PosInfo(self, doc):
        gprs = Utils().get_gprsfix(doc)
        snr = Utils().get_snr(doc)
        svn = Utils().get_svn(doc)
        hdop = Utils().get_hdop(doc)
        ignition = Utils().get_ignition(doc)
        evento = Utils().get_event(doc)
        pos = Utils().get_memoryindex(doc)
        speed = Utils().get_speed(doc)
        gps  = Utils().get_gpsfix(doc)
        date = Utils().get_devdate(doc)
        extPwr = Utils().get_extpower(doc)

        product = self.protocol_to_product(doc)
        stringInfo = "<b>Position</b>: " + str(pos) \
					   + "<br><b>Event:</b> "    + str(evento)  \
					   + "<br><b>Date:</b> "     + str(date) \
                       + "<br><b>Ignition: </b> "  + str(ignition) \
					   + "<br><b>Speed:</b> "  + str(speed) \
                       + "<br><b>GPS Fix:</b> "  + str(gps) \
                       + "<br><b>GPRS Fix:</b> "  + str(gprs) \
                       + "<br><b>Ext Power:</b> "  + str(extPwr)

        if product == "MXT" :
            pass
        elif product == "MTC":
            pass

        return stringInfo

    def accelerometerEventInfo(self, doc):
        evento = Utils().get_event(doc)
        pos = Utils().get_memoryindex(doc)
        speed = Utils().get_speed(doc)
        gps  = Utils().get_gpsfix(doc)
        date = Utils().get_devdate(doc)

        protocol= self.get_protocol(doc)
        product = self.protocol_to_product(doc)
        if product == "MXT" :
            stringInfo = "<b>Position</b>: " + str(pos) \
					   + "<br><b>Event:</b> "    + str(evento)  \
					   + "<br><b>Date:</b> "     + str(date) \
					   + "<br><b>Speed:</b> "  + str(speed) \
                       + "<br><b>GPS Fix:</b> "  + str(gps)
            try:
                docEvento = doc["additional_data"]["telemetry_events"]["hard_braking_list"][0]
                evento = "Hard Breaking"
            except:
                try:
                    docEvento = doc["additional_data"]["telemetry_events"]["hard_lateral_list"][0]
                    if docEvento["side"] == 0:
                        evento = "Hard Lateral Left"
                    else:
                        evento = "Hard Lateral Right"
                except:
                    try:
                        docEvento = doc["additional_data"]["telemetry_events"]["hard_acceleration_list"][0]
                        evento = "Hard Acceleration"
                    except:
                        try:
                            docEvento = doc["additional_data"]["telemetry_events"]["impact_detected_list"][0]
                            evento = "Impact"
                        except:
                            docEvento = 0
            stringInfo = stringInfo \
                         + "<br><br><b>ACCELEROMETER EVENT</b> "\
                         + "<br><b>Type:</b> "    + evento  \
                         + "<br><b>Total Time:</b> "  + str(docEvento["total_time"])  \
                         + "<br><b>Time to Max:</b> " + str(docEvento["time_to_max"])\
                         + "<br><b>Max G:</b> "       + str(docEvento["max_g"])
            return stringInfo


        elif product == "MTC":
            stringInfo = "Bla bla bla Acelerometro MTC"
            return stringInfo

    def get_extpower(self, doc):
        linha = Utils().protocol_to_product(doc)
        try:
            if (linha == "MTC"):
                try:
                    supply = doc["aditional_data"]["adc_data"]["external_power"]
                except:
                    supply = 0
            elif linha == "MXT":
                supply = doc["hardware_monitor"]["detailed_supply"]
            elif linha == "MaxPB":
                try:
                    supply = doc["flags"]["deviceStatus"]["extPowerValue"]
                    supply = float(float(supply)/1000)
                except:
                    try:
                        supply = doc["flags"]["deviceInfo"]["extPowerValue"]
                        supply = float(float(supply)/1000)
                    except:
                        supply = 0
            else:
                supply = -1
        except:
            supply = -1
        return supply

    def get_gprsfix(self, doc):
        return doc["gprsfix"]

    def get_ignition(self, doc):
        return doc["ign"]

    def get_memoryindex(self, doc):
        return doc["pos"]

    def get_gtwdate(self, doc):
        return doc["date_gtw"]

    def get_mapType(self, doc):
        gps = self.get_gpsfix(doc)
        gprs = self.get_gprsfix(doc)
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

    def get_devdate(self, doc):
        return doc["date_dev"]

    def get_serial(self, doc):
        return doc["dev_id"]

    def get_protocol(self, doc):
        try:
            protocol = doc["firmware"]["protocol"]
            return protocol
        except:
            return 173

    def get_csq(self, doc):
        linha = Utils().protocol_to_product(doc)
        try:
            if (linha == "MXT"):
                csq = doc["gps_modem"]["csq"]
            elif linha == "MaxPB":
                try:
                    csq = doc["flags"]["connectionInfo"]["csq"]
                except:
                    csq = -1
            else:
                csq = 0
        except:
            csq = 0
        return csq

    def get_jamming(self, doc):
        linha = Utils().protocol_to_product(doc)
        try:
            if (linha == "MXT"):
                jamming = doc["gps_modem"]["flag_state"]["gsm_jamming"]
            elif linha == "MaxPB":
                try:
                    jamming = doc["flags"]["connectionInfo"]["jamming"]
                except:
                    jamming = -1
            else:
                jamming = False
        except:
            jamming = False
        return jamming

    def get_snr(self, doc):
        linha = Utils().protocol_to_product(doc)
        try:
            if (linha == "MXT"):
                snr = doc["gps_modem"]["snr"]
            elif linha == "MaxPB":
                snr = doc["gps"]["averageSnr"]
            else:
                snr = 0
        except:
            snr = 0
        return snr

    def get_svn(self, doc):
        linha = Utils().protocol_to_product(doc)
        try:
            if (linha == "MaxPB"):
                svn = doc["gps"]["svn"]
            else:
                svn = doc["gps_modem"]["svn"]
        except:
            svn = 0
        return svn

    def get_hdop(self, doc):
        linha = Utils().protocol_to_product(doc)
        try:
            if (linha == "MaxPB"):
                hdop = doc["gps"]["hdop"]
                hdop = hdop #  /10
            else:
                hdop = doc["gps_modem"]["hdop"]
        except:
            hdop = 0
        return hdop

    def get_speed(self, doc):
        return doc["speed"]

    def get_gpsfix(self, doc):
        return doc["gpsfix"]

    def get_antdisconnected(self, doc):
        linha = Utils().protocol_to_product(doc)
        if (linha == "MXT"):
            antdisconnected = doc["gps_modem"]["flag_state"]["gps_antenna_disconnected"]
        else:
            antdisconnected = 0
        return antdisconnected

    def get_GPSantennaFail(self, doc):
        linha = Utils().protocol_to_product(doc)
        try:
            if (linha == "MTC"):
                try:
                    GPSantennaFail = doc["gps_modem"]["flag_state"]["gps_antenna_status"]
                except:
                    GPSantennaFail = 0
            elif linha == "MXT":
                GPSantennaFail = doc["gps_modem"]["flag_state"]["gps_antenna_failure"]
            else:
                GPSantennaFail = 0
        except:
            GPSantennaFail = 0
        return GPSantennaFail

    def get_latitude(self, doc):
        linha = Utils().protocol_to_product(doc)
        if (linha == "MaxPB"):
            latitude = doc["positionInfo"][0]["latitude"]
            latitude = float(float(latitude)/1000000)
        else:
            latitude = doc["gps_modem"]["latitude"]
        return latitude
    def get_longitude(self, doc):
        linha = Utils().protocol_to_product(doc)
        if (linha == "MaxPB"):
            longitude = doc["positionInfo"][0]["longitude"]
            longitude = float(float(longitude)/1000000)
        else:
            longitude = doc["gps_modem"]["longitude"]
        return longitude

    def get_gsensor(self, doc):
        linha = Utils().protocol_to_product(doc)
        try:
            if linha == "MTC":
                try:
                    gsensor = doc["gps_modem"]["flag_state"]["moving"] ############################ VERIFICAR !
                except:
                    gsensor = 0
            elif linha == "MXT":
                gsensor = doc["gps_modem"]["flag_state"]["moving"]
            elif linha == "MaxPB":
                try:
                    gsensor = doc["telemetry"]["status"]["moving"]
                except:
                    gsensor = doc["telemetry"]["flags"]["moving"]
            else:
                gsensor = -1
        except:
            gsensor = False
        return gsensor
    def get_fuel_consumption(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                fuel_consumption = doc['additional_data']['position_information']['analogic_data']['fuel_consumption']
            except:
                fuel_consumption = -1
        return fuel_consumption
    def get_door_closed(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                door_closed_digital = int(doc['additional_data']['position_information']['digital_data']['door_closed'])
            except:
                door_closed_digital = -1
        return door_closed_digital
    def get_door_locked(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                door_locked_digital = int(doc['additional_data']['position_information']['digital_data']['door_locked'])
            except:
                door_locked_digital = -1
            return door_locked_digital
    def get_parking_brake(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                parking_brake_digital = int(doc['additional_data']['position_information']['digital_data']['parking_brake'])
            except:
                parking_brake_digital = -1
        return parking_brake_digital
    def get_motor_brake(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                motor_brake_digital = int(doc['additional_data']['position_information']['digital_data']['motor_brake'])
            except:
                motor_brake_digital = -1
        return motor_brake_digital
    def get_windshield_wipers(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                windshield_wipers_digital = int(doc['additional_data']['position_information']['digital_data']['windshield_wipers'])
            except:
                windshield_wipers_digital = -1
        return windshield_wipers_digital
    def get_speedCAN(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                speed = doc['additional_data']['position_information']['analogic_data']['speed']
            except:
                speed = -1
        return speed
    def get_rpm(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                rpm = doc['additional_data']['position_information']['analogic_data']['rpm']
            except:
                rpm = -1
        return rpm
    def get_odometer(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                odm = doc['additional_data']['position_information']['analogic_data']['odometer']
            except:
                odm = -1
        return odm
    def get_fuel_level1(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                fuel_level1 = doc['additional_data']['position_information']['analogic_data']['fuel_level1']
            except:
                fuel_level1 = -1
        return fuel_level1
    def get_fuel_level2(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                fuel_level2 = doc['additional_data']['position_information']['analogic_data']['fuel_level2']
            except:
                fuel_level2 = -1
        return fuel_level2
    def get_intake_air_temp(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                intake_air_temp = doc['additional_data']['position_information']['analogic_data']['intake_air_temp']
            except:
                intake_air_temp = -1
        return intake_air_temp
    def get_intake_air_flow(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                intake_air_flow = doc['additional_data']['position_information']['analogic_data']['intake_air_flow']
            except:
                intake_air_flow = -1
        return intake_air_flow
    def get_throttle_position(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                throttle_position = doc['additional_data']['position_information']['analogic_data']['throttle_position']
            except:
                throttle_position = -1
        return throttle_position
    def get_barometric_pressure(self, doc):
        if doc["firmware"]["protocol"]==172:
            try:
                barometric_pressure = doc['additional_data']['position_information']['analogic_data']['barometric_pressure']
            except:
                barometric_pressure = -1
        return barometric_pressure
    def get_control_module_voltage(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                control_module_voltage = doc['additional_data']['position_information']['analogic_data']['control_module_voltage']
            except:
                control_module_voltage = -1
        return control_module_voltage
    def get_air_temperature(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                air_temperature = doc['additional_data']['position_information']['analogic_data']['air_temperature']
            except:
                air_temperature = -1
        return air_temperature
    def get_fuel_type(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                fuel_type = doc['additional_data']['position_information']['analogic_data']['fuel_type']
            except:
                fuel_type = -1
        return fuel_type
    def get_ethanol_ratio(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                ethanol_ratio = doc['additional_data']['position_information']['analogic_data']['ethanol_ratio']
            except:
                ethanol_ratio = -1
        return ethanol_ratio
    def get_oil_temperature(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                oil_temperature = doc['additional_data']['position_information']['analogic_data']['oil_temperature']
            except:
                oil_temperature = -1
        return oil_temperature
    def get_engine_temperature(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                engine_temp = doc['additional_data']['position_information']['analogic_data']['engine_temperature']
            except:
                engine_temp = -1
        return engine_temp
    def get_engine_ref_torque(self, doc):
       if doc["firmware"]["protocol"] == 172:
            try:
                engine_ref_torque = doc['additional_data']['position_information']['analogic_data']['engine_ref_torque']
            except:
                engine_ref_torque = -1
       return engine_ref_torque
    def get_current_gear(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                current_gear = doc['additional_data']['position_information']['analogic_data']['current_gear']
            except:
                current_gear = -1
        return current_gear
    def get_engine_fuel_rate(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                engine_fuel_rate = doc['additional_data']['position_information']['analogic_data']['engine_fuel_rate']
            except:
                engine_fuel_rate = -1
        return engine_fuel_rate
    def get_num_dtc_available(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                num_dtc_available = doc['additional_data']['position_information']['analogic_data']['num_dtc_available']
            except:
                num_dtc_available = -1
        return num_dtc_available
    def get_num_dtc_packet(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                num_dtc_packet = doc['additional_data']['position_information']['analogic_data']['num_dtc_packet']
            except:
                num_dtc_packet = -1
        return num_dtc_packet
    def get_brake(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                brake_digital = int(doc['additional_data']['position_information']['digital_data']['brake'])
            except:
                brake_digital = -1
        return brake_digital
    def get_clutch(self, doc):
        if doc["firmware"]["protocol"] == 172:
            try:
                clutch_digital = int(doc['additional_data']['position_information']['digital_data']['clutch'])
            except:
                clutch_digital = -1
        return clutch_digital
    def get_GMT(self):
        GMT = datetime.utcnow() - datetime.now()
        return GMT.seconds/3600

    def set_IntToDatetime(self,intDate):
        devdate = datetime.utcfromtimestamp(intDate).strftime('%Y-%m-%d %H:%M:%S')
        date_object = datetime.strptime(devdate, '%Y-%m-%d %H:%M:%S')
        return date_object

    def set_DatetimeToInt(self, timestamp):
        # timestamp += timedelta(hours=self.get_GMT())
        timestamp = (timestamp - datetime(1970, 1, 1)).total_seconds()
        return timestamp

    def get_temperature(self, doc):
        linha = Utils().protocol_to_product(doc)
        if (linha == "MaxPB"):
            try:
                temperature = doc["flags"]["deviceInfo"]["temperature"]
            except:
                temperature = -1000
            temperature = float(float(temperature)/1000)
        else:
            temperature = doc["hardware_monitor"]["temperature"]
        return temperature

    def get_battery(self, doc):
        linha = Utils().protocol_to_product(doc)
        try:
            if (linha == "MTC"):
                try:
                    bat = doc["aditional_data"]["adc_data"]["battery"]
                except:
                    bat = 0
            elif linha == "MXT":
                bat = doc["hardware_monitor"]["detailed_supply"]
                if float(bat) > 4.5:
                    bat = 0
            elif linha == "MaxPB":
                try:
                    bat = doc["flags"]["deviceStatus"]["battValue"]
                    bat = float(float(bat)/1000)
                except:
                    try:
                        bat = doc["flags"]["deviceInfo"]["battValue"]
                        bat = float(float(bat)/1000)
                    except:
                        bat = 0
            else:
                    bat = 0
        except:
            bat = 0
        return bat

    def get_batteryState(self, doc):
        linha = Utils().protocol_to_product(doc)
        try:
            bat = doc["flags"]["deviceInfo"]["battState"]
        except:
            bat = 0
        return bat

    def get_hourmeter(self, doc):
        linha = Utils().protocol_to_product(doc)
        if (linha == "MaxPB"):
            try:
                hourmeter = doc["telemetry"]["status"]["hourmeter"]
            except:
                try:
                    hourmeter = doc["telemetry"]["flags"]["hourmeter"]
                except:
                    hourmeter = 0
        else:
            try:
                hourmeter = doc["hardware_monitor"]["hourmeter"]
            except:
                hourmeter = 0
        return hourmeter

    def get_Odometro(self, doc):
        linha = Utils().protocol_to_product(doc)
        if (linha == "MaxPB"):
            try:
                odometer = doc["telemetry"]["odometer"]["gps"]
            except:
                odometer = 0
        else:
            try:
                odometer = doc["gps_modem"]["hodometer"]
            except:
                odometer = 0
        return odometer

    def get_uptime(self, doc):
        linha = Utils().protocol_to_product(doc)
        try:
            if (linha == "MaxPB"):
                uptime = doc["flags"]["deviceInfo"]["uptime"]
            else:
                uptime = 0
        except:
            uptime = 0
        return uptime


    def calculaDistancia(self, lat, long, referencia):

        ponto = (long, lat)
        distance = int(great_circle(referencia, ponto).meters)
        return distance

    def findGatewayInList(self, gatewayID, listGateways):
        count = 0
        for x in listGateways:
            if x.deviceID == gatewayID:
                return x.referencia, count
            count += 1


class GatewayLocation:
    def __init__(self, deviceID=0,referencia=0):
        self.deviceID=deviceID
        self.referencia=referencia
        self.isUsed = False
