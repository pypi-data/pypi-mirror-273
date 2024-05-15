from requests import request
import json


class Actions:

    def get(self, url, headers, params={}, data={}):

        response = request("GET",
                           url,
                           headers=headers,
                           params=params,
                           data=data)

        if response.status_code == 404:
            return False

        return json.loads(response.text)

    def post(self, url: str, headers, params: dict = {},
             data: dict = {}, file: dict = {}):

        response = request("POST",
                           url,
                           headers=headers,
                           params=params,
                           data=data,
                           files=file)

        if response.status_code == 404:
            response = json.loads(response.text)
            return print("[ERROR] ", response)

        elif response.status_code == 204:
            response = json.loads(response.text)
            return print(response)
