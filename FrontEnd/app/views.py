from flask import render_template, request
from app import app
import flask_mobility.decorators as mobdec
from scriptMaps import n1_MapaclassMaxPB
from scriptDivCompare import Compareclass
from scriptPacotes import n1_PacotesclassMaxPB
from pprint import pprint
from dbmongo import *
from datetime import *
import time

@app.route('/')
@app.route('/index')
def index():
    return render_template("untitled2teste.html")


###################################################################     MAPA     #######################################
@app.route('/maps')
def n0MapaMaxPB():
	listEquipment=""
	try:
		a = Compareclass()
		listEquipment = a.leitura()
	except:
		print "Error"
		a = 0
	return render_template("n0_tabMapMaxPB.html", listEquipment=listEquipment)

@app.route('/n1_Maps')
def n1MapaMaxPB():
	lista=""

	try:
		serial1 = request.args['serial1']
		limiteinferior = request.args['linf']
		limitesuperior = request.args['lsup']
		anoS, mesS, diaS, horaS, minutoS, segundoS = limitesuperior.split(':')
		anoI, mesI, diaI, horaI, minutoI, segundoI = limiteinferior.split(':')

		dtsup  = datetime(int(anoS),int(mesS),int(diaS),int(horaS),int(minutoS),int(segundoS))
		dtinf  = datetime(int(anoI),int(mesI),int(diaI), int(horaI),int(minutoI),int(segundoI))

		a = n1_MapaclassMaxPB(serial1,dtsup ,dtinf)
		print "01"
		lista = a.leitura()
	except:
		print "Error"
		a = 0
	return render_template("n1_Maps.html", lista=lista)

###################################################################    PACOTES    ######################################
@app.route('/pacotesgprs')
def n0PacotesMaxPB():
	listEquipment=""
	try:
		a = Compareclass()
		listEquipment = a.leitura()
	except:
		print "Error"
		a = 0
	return render_template("n0_tabPacotesMaxPB.html", listEquipment=listEquipment)

@app.route('/n1_Pacotes')
def n1PacotesMaxPB():
	lista=""
	try:
		serial1 = request.args['serial1']
		limiteinferior = request.args['linf']
		limitesuperior = request.args['lsup']
		anoS, mesS, diaS, horaS, minutoS, segundoS = limitesuperior.split(':')
		anoI, mesI, diaI, horaI, minutoI, segundoI = limiteinferior.split(':')

		dtsup  = datetime(int(anoS),int(mesS),int(diaS),int(horaS),int(minutoS),int(segundoS))
		dtinf  = datetime(int(anoI),int(mesI),int(diaI), int(horaI),int(minutoI),int(segundoI))

		a = n1_PacotesclassMaxPB(serial1,dtsup ,dtinf)
		lista = a.leitura()
	except:
		print "Error"
		a = 0
	return render_template("n1_Pacotes.html", lista=lista)
