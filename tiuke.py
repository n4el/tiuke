#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################
#														#
# nombre/name: tiuke_chile								#
# versión/version: 0.1									#
# autor/author: n4el									#
# fuente/source: https://github.com/n4el/tiuke 			#
# fecha/date: nov.2016									#
#														#
#########################################################
#														#
# resumen/resume:										#
#  -es: aplicación  de recolección  de información		#
#       enfocado a personas para ingenería social.		#
#  -en: information gathering aplication of people		#
#       target for social engenering.					#
# 														#
# descripción/description:								#
#  -es: haciendo  uso del RUT  de una  persona chilena	#
#       o identificándola  con un rutificador se hacen 	#
#       búsquedas en  redes sociales,  google  y bases	#
#       de datos de uso público.  El producto consiste	#
#       en un ficha con toda la información encontrada.	#
#														#
# uso/usage:											#
#  -es: se puede ejecutar la aplicación sin  necesidad 	#
#       de ingresar una opción.	No se puede usar  "-r"	#
#       y "-n" al mismo tiempo.							#
#       opciones:										#
#       -n: búsqueda por nombres y/o apellidos.			#
#       -r: búsqueda por rut.							#
#       -v: verbose.									#
#       ejemplos:										#
#        ./tiuke -n "juan pérez pérez"					#
#        ./tiuke -r -v "12345678-9"						#
#        												#
#########################################################

"""
modules:
	- estado:
		def GobiernoTransparente
		def Servel
	- profesion:
		def Pjud
	- facebook:
	- twitter:
	- bing_correo:
	- linkedin:
	- google_exponsed_bd:
	- google:
	- aux:
		def Bomberos
tiuke:
	- class usage:
		- noop
		- opb
		- file
		- log
	def inic
targed:
	- rutificador:
tiuke.log

"""

import os
import sys
import getopt
import configparser
from modules import ruti

#import modules.servel
#import config
try :
	from lxml import html
except:
	print '\033[0;30m'+'[es]'+'\033[0m'+'\033[1;31m'+' la libreria "lxml" no fue encontrada. \n'+'\033[0m'
	print '\033[0;30m'+'[en]'+'\033[0m'+'\033[1;31m'+' "lxml" library not found.\n'+'\033[0m'
	sys.exit()
try:
	import requests
except:
	print '\033[0;30m'+'[es]'+'\033[0m'+'\033[1;31m'+' la libreria "requests" no fue encontrada. \n'+'\033[0m'
	print '\033[0;30m'+'[en]'+'\033[0m'+'\033[1;31m'+' "requests" library not found.\n'+'\033[0m'
	sys.exit()

def banner():
	print '\033[0;40m'+' ############################################## '+'\033[0m'
	print '\033[0;40m'+' #'+'\033[0;92m'+'    __  .__       __                        '+'\033[0;40m'+'# '+'\033[0m'
	print '\033[0;40m'+' #'+'\033[0;92m'+'  _/  |_|__|__ __|  | __ ____               '+'\033[0;40m'+'# '+'\033[0m'
	print '\033[0;40m'+' #'+'\033[0;92m'+'  \   __\  |  |  \  |/ // __ \              '+'\033[0;40m'+'# '+'\033[0m'
	print '\033[0;40m'+' #'+'\033[0;92m'+'   |  | |  |  |  /    <\  ___/              '+'\033[0;40m'+'# '+'\033[0m'
	print '\033[0;40m'+' #'+'\033[0;92m'+'   |__| |__|____/|__|_ \\\___  > _Chile.     '+'\033[0;40m'+'# '+'\033[0m'
	print '\033[0;40m'+' #'+'\033[0;92m'+'                      \/    \/              '+'\033[0;40m'+'# '+'\033[0m'
	print '\033[0;40m'+' #'+'\033[0;31m'+'  tiuke_chile v0.1                          '+'\033[0;40m'+'# '+'\033[0m'
	print '\033[0;40m'+' #'+'\033[0;31m'+'  autor/author: n4el                        '+'\033[0;40m'+'# '+'\033[0m'
	print '\033[0;40m'+' #'+'\033[0;31m'+'  referencia/referer:                       '+'\033[0;40m'+'# '+'\033[0m'
	print '\033[0;40m'+' #'+'\033[0;31m'+'   - https://github.com/n4el/tiuke          '+'\033[0;40m'+'# '+'\033[0m'
	print '\033[0;40m'+' #'+'\033[0;31m'+'                                            '+'\033[0;40m'+'# '+'\033[0m'
	print '\033[0;40m'+' ############################################## '+'\033[0m'+'\n'

class usage :
	def __init__(self,query,ruti,verbose):
		self.q = query
		self.r = ruti
		self.v = verbose
	# es: función de uso sin opciones de búsqueda.
	def noop(self):
		if self.r == True :
			print '\033[0;30m'+' [es]'+'\033[0m'+' ingrese nombre(s)/apellido(s) o un RUT:'
			q = raw_input('\033[0;30m'+' [en]'+'\033[0m'+' insert names or RUT:\n '+'\033[1;30m'+'#> '+'\033[0m')
			q = ruti.ruti_com(q,self.v)

		else :
			print '\033[0;30m'+' [es]'+'\033[0m'+' ingrese un RUT:'
			q = raw_input('\033[0;30m'+' [en]'+'\033[0m'+' insert RUT:\n '+'\033[1;30m'+'#> '+'\033[0m')
		return q
	#es: función de uso con opciones de búsqueda.
	def opb(self):
		if self.r == False :
			q = dict(name='',rut=self.q[:-3],dv=self.q[-1:],cedula=self.q)
		else:
			q = ruti.ruti_com(self.q,self.v)

		return q

# es: función de inicio principal del programa.
def init(argv=0):
	banner()
	print '\033[0;30m'+' ----------------------------------------------'+'\033[0m'
	u = sys.argv[1:]
	# es: definimos las variables asociadas a las opciones válidas.
	name = ''
	rut = ''
	verbose = False
	log = []
	ruti = True

	# es: si no se introducen opciones.
	if len(u) < 1 :
		# es: crea 'q' a través de 'usage.noop'.
		print '\033[0;30m'+' [es]'+'\033[0m'+' no ha seleccionado ninguna opción.'
		print '\033[0;30m'+' [en]'+'\033[0m'+' no option selected.'
		print '\033[0;30m'+'     ----------------------------------------------'+'\033[0m'
		q = usage(name,ruti,verbose)
		q = q.noop()
	# es: si se insertan opciones.
	else :
		try: # es: integra las opciones introducidas a las variables 'opts' y 'args'.
			opts, args = getopt.getopt(argv, "n:r:x:vl:")
		except getopt.GetoptError:
			print '\033[0;30m'+' [es]'+'\033[0;31m'+' error al introducir las opciones.'+'\033[0m'
			print '\033[0;30m'+' [en]'+'\033[0;31m'+' options insert failed.'+'\033[0m'
			print '\033[0;30m'+'     ----------------------------------------------'+'\033[0m'
			q = usage(rut,ruti,verbose)
			q = q.noop()

		# es: toma el contenido de las opciones.
		for o, a in opts:
			if o == '-n':
				name = str(a)
			elif o == '-r':
				rut = str(a)
			elif o == '-x':
				ruti = False
			elif o == '-v':
				verbose = True
			elif o == '-l':
				targets = list(a)
		# es: proceder a realizar la consulta.
		if name != '' :
			if rut != '':
				print '\033[0;30m'+' [es]'+'\033{0;31m'+' no se puede usar la opción "-n" y "-r" al mismo tiempo.'+'\033[0m'
				print '\033[0;30m'+' [en]'+'\033{0;31m'+' ---.'+'\033[0m'
				print '\033[0;30m'+'     ----------------------------------------------'+'\033[0m'
				sys.exit()

			elif ruti == False :
				print '\033[0;30m'+' [es]'+'\033{0;31m'+' no puede usar opción "-n" sin activar módulo "ruti" '+'\033[0m'
				print '\033[0;30m'+' [en]'+'\033{0;31m'+' ---.'+'\033[0m'
				print '\033[0;30m'+'     ----------------------------------------------'+'\033[0m'
				sys.exit()
			else:
				q = usage(name,ruti,verbose)
				q = q.opb()
		elif rut != '' :
			q = usage(rut,ruti,verbose)
			q = q.opb()
		else :
			q = usage(name,ruti,verbose)
			q = q.noop()	
	# ya se dispone del diccionario de identificación en 'q'.	
	print q
	if verbose == True :
		print '\033[0;30m'+' [v][es]'+'\033{0m'+' se procede a consultar módulos...'+'\033[0m'
	# consulta al archivo de configuración 'config.py'.
	print 'pre_config.Modules'
	mod == configparser.ConfigParser()
	print '202'
	mod.read('tiuke.cfg')
	mod == mod['modulos']
	
	if mod.getboolean['servel'] == True :
		print 'si'
		r = modules.servel.consulta(q)
		r = mod.servel()
		print r
	#else:
	#	print 'no toma servel'
	#	sys.exit()

		



if __name__ == "__main__":

	try:
		init(sys.argv[1:])
	
    # excepción de interrupción del usuario.
	except KeyboardInterrupt:
		print '\033[0;30m'+' [es]'+'\033{0;31m'+' aplicación interrupida por el usuario.'+'\033[0m'
	except:
		sys.exit()

		"""


def __main__ 	

		else :


			iden = iden.ConOpc()
		r = Motores(iden)
		servel = r.Servel()
		bombero = r.Bombero()
		abogado = r.Abogados()
		trans = r.GobiernoTransparente()
		print 'd_main'
		print trans
		Salida(iden, servel, bombero, abogado)
	if 

	# función cuando lleva opciones. 		
	def ConOpc(self): 		
"""