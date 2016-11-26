# -*- coding: utf-8 -*-


from lxml import html
import requests
import sys
import os

def output(r,cedula=''):
	print 'out'
	if r == '':
		name = ''
		if cedula != '':
			dv = cedula[-1:]
			rut = cedula[:-3]
		else:
			dv = ''
			rut = ''
	else :
		print r
		name = r[u'name']
		print 'out1'
		rut = str(r['rut'])
		dv = str(r['dv'])
		if cedula == '':
			print 'd'
			cedula = str(rut)+'-'+str(dv)
	r = dict(name=name,rut=rut,dv=dv,cedula=cedula)
	return r

def ruti_com (query,verbose=False):
	url='http://chile.rutificador.com/'
	if verbose == True :
		print '\033[0;30m'+'[v][es]''\033[0m'+' conectando con: '+ url+'\n'
	s = requests.Session()
	s.headers.update({'User-Agent': None})
	r = s.get(url)
	if r.status_code == 200 :
		if verbose == True :
			print '\033[0;30m'+'[v][es]''\033[1;32m'+' en línea, se procede...\n'+'\033[0m'
	else :
		if verbose == True :
			print '\033[0;30m'+'[v][es]''\033[1;31m'+' error en la conexión.\n'+'\033[0m'
			print '\033[0;30m'+'[v][es]''\033[1;31m'+' codigo de estado: ', r,status_code, '\n'+'\033[0m'
		r = ''
		return r
	csrf_cookie = r.cookies['csrftoken']
	if verbose == True :
		print '\033[0;30m'+'[v][es/en]''\033[0m'+' csrftoken: ''\033[0;32m'+csrf_cookie+'\n'+'\033[0m'
	url='http://chile.rutificador.com/get_generic_ajax/'
	r = s.post(url, data=dict(
				csrfmiddlewaretoken=csrf_cookie,
				entrada=query)
				)
	r = r.json()
	if r['status'] == 'success' :
		if verbose == True :
			print '\033[0;30m'+'[v][es]''\033[1;32m'+' consulta exitosa.\n'+'\033[0m'
		r = r['value']
		if len(r) > 1 :
			c = 0
			print '\033[0;30m'+'[es]''\033[0m'+' Resultados: \n'
			for a in r:
				c=c+1
				print '\033[0;32m'+str(c)+'	'+'\033[0;33m'+a[u'name']+'\n 	'+'\033[0;31m'+str(a['rut'])+'-'+str(a['dv'])+'\033[0m'
			o = int(raw_input('\033[0;30m'+'[es]'+'\033[0m'+'Ingrese alguna opción: \n '+'\033[1;30m'+'#> '+'\033[0m'))
			r = r[o]
			#r = r['value']
			r = output(r)
			return r
		else :
			r = r[0]
			if query[-3] != '-' :
				r = output(r)
			else: 
				r = output(r, query)
			return r

	else :
		if verbose == True :
			print '\033[0;30m'+'[v][es]''\033[1;31m'+' consulta al rutificador sin resultados.\n'+'\033[0m'
		r = str(query).find('-')
		if r == 8 :
			print '\033[0;30m'+'[v][es]''\033[0m'+' se procederá a hacer uso del RUT ingresado.\n'+'\033[0m'
			r = ''
			r = output(r,query)
			return r
		else :
			print '\033[0;30m'+'[v][es]''\033[1;31m'+' no se puede proceder sin RUT.\n'+'\033[0m'
			sys.exit()


	