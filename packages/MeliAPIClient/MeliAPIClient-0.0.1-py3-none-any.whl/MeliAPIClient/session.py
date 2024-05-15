from datetime import datetime, timedelta
from requests import request
import json


class Session:

    def __init__(self, keys: json, token: json, user: json) -> None:

        self.headers: dict = {
            "Authorization": "",
            "format-new": "true"
        }

        self.ml_keys = read(keys)
        self.ml_token = read(token)
        self.ml_user = read(user)

        self.access()

    def access(self) -> dict:

        time_flag = timedelta(hours=5, minutes=59, seconds=0.0)
        date_token = datetime.fromisoformat(self.ml_token['date'])
        token_time = datetime.now()-date_token

        if time_flag > token_time:
            self.headers['Authorization'] = \
                f'Bearer {self.ml_token["access_token"]}'
            return self.ml_token

        self.refresh()
        self.headers['Authorization'] = \
            f'Bearer {self.ml_token["access_token"]}'

        return self.ml_token

    def refresh(self) -> None:

        url = "https://api.mercadolibre.com/oauth/token"

        payload: dict = {
            "grant_type": "refresh_token",
            "client_id": self.ml_keys['client_id'],
            "client_secret": self.ml_keys['client_secret'],
            "refresh_token": self.ml_token['refresh_token']
        }

        headers: dict = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }

        response = request("POST", url, headers=headers, data=payload)

        ml_response: dict = json.loads(response.text)
        ml_response["date"] = datetime.isoformat(datetime.now())

        write("ml_token.json", ml_response)


def read(file_name: str) -> dict:
    with open(file_name, "r") as content:
        return (json.load(content))


def write(file_name: str, data: dict) -> None:
    with open(file_name, 'w') as content:
        json.dump(data, content, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    session = Session()
    print(session.user["id"])
