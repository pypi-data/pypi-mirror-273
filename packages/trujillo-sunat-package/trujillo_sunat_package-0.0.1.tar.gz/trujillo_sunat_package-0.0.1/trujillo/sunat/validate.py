import requests
import json
from concurrent.futures import ThreadPoolExecutor


class ValidateReceip():
    def __init__(self, token: str, ruc: str):
        self.__token = token
        self.__ruc = ruc

    def __get_record(self, data_input: dict):
        url = f"https://api.sunat.gob.pe/v1/contribuyente/contribuyentes/{self.__ruc}/validarcomprobante"
        payload = json.dumps(data_input)
        headers = {'Authorization': self.__token,
                   'Content-Type': 'application/json'}

        response = requests.request("POST", url, headers=headers, data=payload)
        response.encoding = 'utf-8'
        dataset = response.json()

        newRecord = data_input
        if dataset["success"]:
            # Validamos si existen las claves dentro del JSON,
            # ya que la API omite en ocasiones estas claves en su respuesta
            if dataset["data"].get('estadoCp') != None:
                newRecord["estadoCp"] = dataset["data"]["estadoCp"]

            if dataset["data"].get('estadoRuc') != None:
                newRecord["estadoRuc"] = dataset["data"]["estadoRuc"]

            if dataset["data"].get('condDomiRuc') != None:
                newRecord["condDomiRuc"] = dataset["data"]["condDomiRuc"]

        return newRecord

    def get_records(self, workers: int = 1, consult: list = None):
        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = executor.map(self.__get_record, consult)

        return results
