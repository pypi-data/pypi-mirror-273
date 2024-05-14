import time
from .sign import sign_request, get_machine_code
import requests


class Request:
    def __init__(self, base_url, appid, secret):
        self.__base_url = base_url
        self.__appid = appid
        self.__secret = secret
        self.__machine_code = get_machine_code()

    def request(self, method, url, data, params=None):
        timestamp = int(time.time() * 1000)
        sign = self._sign_request(method, url, timestamp)
        headers = {
            "appid": self.__appid,
            "timestamp": str(timestamp),
            "machine_code": self.__machine_code,
            "sign": sign,
        }
        response = requests.request(method, f"{self.__base_url}{url}", headers=headers, data=data, params=params)
        return response.json()

    def get(self, url, params=None):
        return self.request("GET", url, None, params)

    def post(self, url, data = None):
        return self.request("POST", url, data)

    def put(self, url, data):
        return self.request("PUT", url, data)

    def delete(self, url, data = None):
        return self.request("DELETE", url, data)

    def _sign_request(self, method: str, url: str, timestamp: int) -> str:
        return sign_request(self.__appid, self.__secret, method, url, timestamp)

    def __repr__(self):
        return self.__str__()
