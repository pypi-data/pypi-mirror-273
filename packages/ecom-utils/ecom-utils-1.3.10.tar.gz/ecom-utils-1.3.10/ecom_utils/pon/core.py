import datetime as dt
import json
import re
import requests

ENDPOINT_STAGE = 'https://devapp8.ecomchaco.com.ar'
ENDPOINT_PROD = 'https://apps8.chaco.gob.ar/ponapi'

API_ENDPOINTS = {
	'get_token_application': '_endpointbase_/ponapitest/oauth/access_token',
	'obtener_jurisdicciones': '_endpointbase_/ponapitest/rest/ConsultaJurisdicciones',
	'obtener_oficinas': '_endpointbase_/ponapitest/rest/ConsultaOficinas',
	'consulta_cargos_agente': '_endpointbase_/ponapitest/rest/ConsultaCargosAgente'
}

class Pon():
	def __init__(self, username, password, client_id, mode_stage=True):
		self.username = username
		self.password = password
		self.client_id = client_id
		self.mode_stage = mode_stage

		self.access_token = None
		self.scope = None
		self.refresh_token = None
		self.user_guid = None

	def get_endpoint_base(self):
		if self.mode_stage:
			return ENDPOINT_STAGE
		return ENDPOINT_PROD

	def get_token_application(self):
		url = API_ENDPOINTS['get_token_application'].replace("_endpointbase_", self.get_endpoint_base())
		headers = {
			"client_id": self.client_id,
			"grant_type": "password",
			"scope": "FullControl",
			'username': self.username,
			'password': self.password,
		}

		response = requests.post(url, headers=headers)
		if response.status_code == 200:
			data = response.json()
			self.access_token = data.get("access_token", None)
			self.scope = data.get("scope", None) 
			self.refresh_token = data.get("refresh_token", None)
			self.user_guid = data.get("user_guid", None)
	
	def obtener_jurisdicciones(self):
		if self.access_token is None:
			self.get_token_application()
			if self.access_token is None:
				return None
		jurisdicciones = []

		url = API_ENDPOINTS['obtener_jurisdicciones'].replace("_endpointbase_", self.get_endpoint_base())

		headers = {
			"Authorization": self.access_token,
			"Content-Type": "application/json"
		}

		data = json.dumps({
			"Orden": 0,
		    "Id": 0,
		    "Nombre": ""
		})
		response = requests.post(url, headers=headers, data=data)
		if response.status_code == 200:
			data = response.json()
			jurisdicciones = data["SDTJurisdicciones"]["Jurisdicciones"]
		return jurisdicciones

	def obtener_oficinas(self, jurId):
		if self.access_token is None:
			self.get_token_application()
			if self.access_token is None:
				return None
		oficinas = []

		url = API_ENDPOINTS['obtener_oficinas'].replace("_endpointbase_", self.get_endpoint_base())

		headers = {
			"Authorization": self.access_token,
			"Content-Type": "application/json"
		}

		data = json.dumps({
			"JurId": jurId
		})
		response = requests.post(url, headers=headers, data=data)

		if response.status_code == 200:
			data = response.json()
			oficinas = data["SDTOficinas"]["Oficinas"]
		return oficinas

	def obtener_cargos_persona(self, dni, cargos_activos=True, fecha_hasta=None):
		if self.access_token is None:
			self.get_token_application()
			if self.access_token is None:
				return None
		
		url = API_ENDPOINTS['consulta_cargos_agente'].replace("_endpointbase_", self.get_endpoint_base())

		headers = {
			"Authorization": self.access_token,
			"Content-Type": "application/json"
		}

		
		data = json.dumps({
			"Documento": dni
		})
		response = requests.post(url, headers=headers, data=data)

		agentes_cargos = []
		if response.status_code == 200:
			fecha_actual = dt.datetime.now().strftime('%Y-%m-%d')
			data = response.json()
			agentes = data.get("SDTAgentesCargos", {}).get("Agentes", [])
			for a in agentes:
				cargos = []
				for c in a["Cargos"]:
					agregar = False
					if cargos_activos:
						if fecha_actual < c["CargoHasta"]:
							agregar = True
					elif fecha_hasta:
						patron_fecha = re.compile(r'\d{4}-\d{2}-\d{2}')
						if not patron_fecha.match(fecha_hasta):
							ValueError("La fecha no tiene el formato correcto (YYYY-MM-DD).")
						
						if fecha_hasta < c["CargoHasta"]:
							agregar = True
					else:
						agregar = True

					if agregar:
						cargos.append({
							"JurId": c["JurId"],
							"JurNombre": c["JurNombre"],
							# "EscId": c["EscId"],
							# "EscNombre": c["EscNombre"],
							"CarId": c["CarId"],
							"CargoNombre": c["CargoNombre"],
							"CargoDesde": c["CargoDesde"],
							"CargoHasta": c["CargoHasta"],
							"OfiId": c["OfiId"],
							"OfiAnexo": c["OfiAnexo"],
							"OficinaNombre": c["OficinaNombre"]
						})
				
				agentes_cargos.append({
					"Prefijo": a["Prefijo"],
					"Documento": a["Documento"],
					"DigitoVerificador": a["DigitoVerificador"],
					"Apellido": a["Apellido"],
					"Nombre": a["Nombre"],
					"Sexo": a["Sexo"],
					"FechaNacimiento": a["FechaNacimiento"],
					"Cargos": cargos
				})
		return agentes_cargos