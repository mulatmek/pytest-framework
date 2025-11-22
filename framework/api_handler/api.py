import requests
from requests import RequestException


class APIHandler:
    def __init__(self, base_url):
        self.base_url = base_url

    def ping(self, endpoint="/"):
        """
        Checks if the API is reachable.
        Returns True if status code is 200, False otherwise.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=2)
            return response.status_code == 200
        except RequestException:
            return False

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params, headers=headers)
        return response

    def post(self, endpoint, data=None, json=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, data=data, json=json, headers=headers)
        return response

    def put(self, endpoint, data=None, json=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, data=data, json=json, headers=headers)
        return response

    def delete(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=headers)
        return response
