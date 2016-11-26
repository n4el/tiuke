# -*- coding: utf-8 -*-
from lxml import html
import requests

class consulta:

	def __init__(self,query,verbose=False):
		self.q = query
		self.v = verbose

	# es: búsqueda en consulta de información electoral del Servicio Electoral de Chile [SERVEL].
	#     referencia: http://servel.cl/
	def servel(self):
		url='https://consulta.servel.cl/'
		s = requests.Session()
		s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6'})
		r = s.get(url)
		if r.statuscode == 200 :
			rg = html.fromstring(r.content)
			csrftoken = rg.xpath('//input[@id="_csrf"]/@value')
			r_headers = {
				'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
				'X-Requested-With': 'XMLHttpRequest',
				'Accept-Language': 'en-US,en;q=0.5',
				'Content-Length': '74',
				'Accept': 'text/html,*/*;q=0.01',
				'Referer': url
			}
			url='https://consulta.servel.cl/consulta'
			r = s.post(url, data=dict(
						rut = self.q['rut'],
						dv=self.q['dv'],
						_csrf=csrftoken,
						captchaResp='1'),
						headers=r_headers
						)
			r = r.json()
			r = r[0]
			r = r['consulta_datos_json']
			if self.v == True :
				print 'v: [es] conexión a servel.cl exitosa.'
				print '   [en] servel.cl connection ok.'
				if r == None :
					print 'v: [es] sin información electoral.'
				else :
					print 'v: [es] con información electoral.'
		else :
			r = None
			if self.v == True :
				print 'v: [es] conexión a servel.cl falló.'
				print '   [en] servel.cl connection failed.'
		return r
