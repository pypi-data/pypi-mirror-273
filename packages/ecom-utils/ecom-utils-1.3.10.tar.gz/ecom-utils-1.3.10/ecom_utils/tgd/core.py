import requests
import json

from datetime import datetime
from .base import SETTINGS


def get_endpoint_base(mode_stage, version):
    """
    Obtiene endpoint base acorde a el modo y su version. Ver el archivo de configuracion para los tipos de versiones permitidos.
    """
    if mode_stage:
        return SETTINGS[version]["API_ENDPOINTS"]["oauth_base_uri"].replace("_endpointbase_",
                                                                            SETTINGS[version]["ENDPOINT_STAGE"])
    return SETTINGS[version]["API_ENDPOINTS"]["oauth_base_uri"].replace("_endpointbase_",
                                                                        SETTINGS[version]["ENDPOINT_PROD"])


class TGD():
    def __init__(self, client_id, client_secret, url_base, redirect_url, mode_stage=True, version="v1"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.url_base = url_base
        self.redirect_url = redirect_url
        self.mode_stage = mode_stage
        self.version = version

    def get_endpoint_base(self):
        """
        Obtiene endpoint base acorde a el modo y su version. Ver el archivo de configuracion para los tipos de versiones permitidos.
        """
        if self.mode_stage:
            # print(f'GEB1- stage')
            return SETTINGS[self.version]["ENDPOINT_STAGE"]
        return SETTINGS[self.version]["ENDPOINT_PROD"]

    def get_token_application(self):
        url = SETTINGS[self.version]["API_ENDPOINTS"]['get_token_application'].replace("_endpointbase_",
                                                                                       self.get_endpoint_base())
        # print(f'GTA1-{url}')
        payload = (
        ("grant_type", "client_credentials"), ("client_id", self.client_id), ('client_secret', self.client_secret))
        # print(f'GTA2-{payload}')
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=payload)
        access_token, expires_in = None, None
        # print(f'GTA3-{response}')
        if response.status_code == 200:
            data = response.json()
            access_token = data['access_token']
            expires_in = data['expires_in']
        # print(f'GTA4-{access_token} {expires_in}')
        return access_token, expires_in


class TGD_OAUTH(TGD):
    def __init__(self, client_id, client_secret, url_base, redirect_url, mode_stage=True, version="V1"):
        super().__init__(mode_stage=mode_stage, client_id=client_id, client_secret=client_secret, url_base=url_base,
                         redirect_url=redirect_url, version=version)

    def get_user_by_cuil(self, cuil):
        # print(f'GUBC1-{cuil}')
        access_token, expires_in = self.get_token_application()
        url = SETTINGS[self.version]["API_ENDPOINTS"]['get_persona_via_cuil'].replace('_cuil_', cuil)
        # print(f'GUBC2-{access_token} {url}')
        user = None
        message = None
        if access_token and expires_in:
            # print(f'GUBC3-dentro')
            response = requests.get(url, headers={'Content-Type': 'application/json',
                                                  'Authorization': 'Bearer %s' % access_token})
            # print(f'GUBC4-{response}')
            if response.status_code == 200:
                data = response.json()
                # print(f'GUBC5-{data}')
                user = {'cuil': data['cuitCuil'], 'apellidos': data['apellidos'], 'nombres': data['nombres'],
                        'id': data['id']}
            elif response.status_code == 403:
                data = response.json()
                # print(f'GUBC6-{data}')
                message = data["message"]
            else:
                # print(f'GUBC7-error')
                message = "Ha ocurrido un inconveniente, contáctese con el Adminstrador (CODE_ERROR: 10-01-01 L45[%s])" % response.status_code

        # message = "Usuario obtenido corectamente"
        # user = {'cuil': '20362069247', 'apellidos': 'IBANEZ', 'nombres': 'Lucas Sebastian', 'id': 123456}
        # print(f'GUBC8-{user}')
        return user, message

    def get_token_via_authorization_code(self, code):
        # print(f'GTVAC1-{code}')
        url = SETTINGS[self.version]["API_ENDPOINTS"]['get_token_via_authorization_code'].replace("_endpointbase_",
                                                                                                  self.get_endpoint_base())
        # print(f'GTVAC2-{url}')
        payload = (
            ("code", code),
            ("grant_type", "authorization_code"),
            ("client_id", self.client_id),
            ('client_secret', self.client_secret),
            ("redirect_uri", self.redirect_url)
        )
        # print(f'GTVAC3-{payload}')
        if SETTINGS[self.version] == "V1":
            # print("1 ",SETTINGS[self.version]["API_ENDPOINTS"]['Content-Type'])
            response = requests.get(url, headers={'Content-Type': SETTINGS[self.version]["API_ENDPOINTS"]['Content-Type']}, params=payload)
        else:
            # print("2 ",SETTINGS[self.version]["API_ENDPOINTS"]['Content-Type'])
            response = requests.post(url,
                                    headers={'Content-Type': SETTINGS[self.version]["API_ENDPOINTS"]['Content-Type']},
                                    data=payload)
        access_token, expires_in, refresh_token = None, None, None
        # print(f'GTVAC4-{response}')
        if response.status_code == 200:
            data = response.json()
            access_token = data['access_token']
            expires_in = data['expires_in']
            refresh_token = data['refresh_token']
            # print(f'GTVAC5-{data}')
        return access_token, expires_in, refresh_token

    def get_persona_via_token(self, access_token):
        # print(f'GPVT1-{access_token}')
        url = SETTINGS[self.version]["API_ENDPOINTS"]['get_persona_via_token'].replace("_endpointbase_",
                                                                                       self.get_endpoint_base())
        # print(f'GPVT2-{url}')
        response = requests.get(url, headers={'Content-Type': 'application/json',
                                              'Authorization': 'Bearer %s' % (access_token)})
        # print(f'GPVT3-{response}')
        user, message = None, None
        if response.status_code == 200:
            data = response.json()
            email = None
            # print(f'GPVT1-{data}')
            try:
                email = data['emails'][0]['email']
            except Exception as e:
                print("ERROR - " + str(e))
                pass

            dni = None
            for documento in data.get("tiposDocumentoPersona", []):
                if documento["tipoDocumento"]["tipoDocumento"] == "DNI":
                    dni = documento["numeroDocumento"]
                    break
            fecha_nacimiento = None
            if data['fechaNacimiento']:  # FORMATO: 2020-06-26T10:24:13-0300
                fecha_nacimiento = datetime.strptime(data['fechaNacimiento'], '%Y-%m-%dT%H:%M:%S%z')
            user = {'cuil': data['cuitCuil'],
                    'apellidos': data['apellidos'],
                    'nombres': data['nombres'],
                    'id': data['id'],
                    'email': email,
                    'sexo': data['sexo'],
                    'fecha_nacimiento': fecha_nacimiento,
                    'dni': dni}
        # print(f'GPVT2-{user}')
        return user, message


class ApiComunicaciones(TGD_OAUTH):
    def __init__(self, client_id, client_secret, url_base, redirect_url, mode_stage=True, version="v1"):
        super().__init__(mode_stage=mode_stage, client_id=client_id, client_secret=client_secret, url_base=url_base,
                         redirect_url=redirect_url, version=version)

    def enviar_notificacion(self, asunto, plazo_dias, contenido, persona_envia, cuils=[], cuof="6-283-0",
                            lectura_obligatoria=False):
        access_token, expires_in = self.get_token_application()
        url = SETTINGS[self.version]["API_ENDPOINTS"]['comunicaciones'].replace("_endpointbase_", self.get_endpoint_base())

        data = None
        status = False

        x = {
            "cuof": cuof,
            "asunto": asunto,
            "contenido": contenido,
            "plazoDias": plazo_dias,
            "cuils": cuils,
            "lecturaObligatoria": lectura_obligatoria,
            "personaEnvia": persona_envia
        }
        if access_token and expires_in:
            response = requests.post(url, headers={'Content-Type': 'application/json',
                                                   'Authorization': 'Bearer %s' % access_token}, data=json.dumps(x))

            if response.status_code in [200, 201]:
                data = response.json()
                status = True
            else:
                try:
                    data = response.json()
                except Exception as e:
                    data = {"error": str(e)}

        return data, status
