# ENDPOINT_STAGE = 'http://stage.ventanillaunica.chaco.gov.ar'
# ENDPOINT_PROD = 'https://gobiernodigital.chaco.gob.ar'
#
# API_ENDPOINTS = {
#     'oauth_base_uri': '_endpointbase_/oauth/v2/',
#     'get_token_via_authorization_code': '_endpointbase_/oauth/v2/token',
#     'get_token_application': '_endpointbase_/oauth/v2/token',
#     'get_persona_via_cuil': '_endpointbase_/api/v1/persona/cuil/_cuil_',
#     'get_persona_via_token': '_endpointbase_/api/v1/persona'
# }
#
# # VERSION 2: Nueva llamada 2023
#
# ENDPOINT_STAGE_NEW = ' https://core.tgdpruebas.chaco.gob.ar'
# ENDPOINT_PROD_NEW = 'https://gobiernodigital.chaco.gob.ar'
#
# API_ENDPOINTS_NEW = {
#     'oauth_base_uri': '_endpointbase_',
#     'get_token_via_authorization_code': '_endpointbase_/token',
#     'get_token_application': '_endpointbase_/token',
#     'get_persona_via_cuil': '_endpointbase_/api/v2/persona/cuil/_cuil_',
#     'get_persona_via_token': '_endpointbase_/api/v2/persona'
# }

SETTINGS = {"V1": {"ENDPOINT_STAGE": 'http://stage.ventanillaunica.chaco.gov.ar',
                   "ENDPOINT_PROD": 'https://gobiernodigital.chaco.gob.ar',
                   "API_ENDPOINTS": {
                       'oauth_base_uri': '_endpointbase_/oauth/v2/',
                       'get_token_via_authorization_code': '_endpointbase_/oauth/v2/token',
                       'get_token_application': '_endpointbase_/oauth/v2/token',
                       'get_persona_via_cuil': '_endpointbase_/api/v1/persona/cuil/_cuil_',
                       'get_persona_via_token': '_endpointbase_/api/v1/persona',
                       'Content-Type': 'application/json'
                   }
                   },

            "V1.1": {"ENDPOINT_STAGE": 'https://core.tgdpruebas.chaco.gob.ar',
                     "ENDPOINT_PROD": 'https://gobiernodigital.chaco.gob.ar',
                     "API_ENDPOINTS": {
                         'oauth_base_uri': '_endpointbase_',
                         'get_token_via_authorization_code': '_endpointbase_/token',
                         'get_token_application': '_endpointbase_/token',
                         'get_persona_via_cuil': '_endpointbase_/api/v2/persona/cuil/_cuil_',
                         'get_persona_via_token': '_endpointbase_/api/v2/persona',
                         'Content-Type': 'application/x-www-form-urlencoded'
                     }
                     },
            }
