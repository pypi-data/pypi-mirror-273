import requests

class Token():
    def __init__(self, args: dict):
        self.__client_id = args["client_id"]
        self.__client_secret = args["client_secret"]
        
    
    def generate_token(self):
        try:
            # Endpoint
            endpoint = f'https://api-seguridad.sunat.gob.pe/v1/clientesextranet/{self.__client_id}/oauth2/token/'
            payload = {
                'grant_type': 'client_credentials',
                'scope': 'https://api.sunat.gob.pe/v1/contribuyente/contribuyentes',
                'client_id': self.__client_id,
                'client_secret': self.__client_secret
            }
            
            req = requests.post(endpoint, payload, timeout=3)
            req.raise_for_status()

            # Create token
            token = ""
            if req.status_code == 200:
                access_token = req.json()['access_token']
                token = f'Bearer {access_token}'
                
            return token
        
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)     
    
    