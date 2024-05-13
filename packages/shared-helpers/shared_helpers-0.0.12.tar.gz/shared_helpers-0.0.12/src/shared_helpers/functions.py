import calendar
import requests
from datetime import date
from datetime import datetime
import json
import time
import jwt
import os

from urllib3.util import Retry
from requests.adapters import HTTPAdapter

req = requests.Session()
retries = Retry(total=5,
                backoff_factor=2,
                status_forcelist=[429, 500, 502, 503, 504])

req.mount('http://', HTTPAdapter(max_retries=retries))

class TokenHelper():
    def __init__(self, json_file_path=None, api_key=None, endpoint_url=None):
        self.json_file_path = json_file_path
        self.api_key = api_key
        self.endpoint_url = endpoint_url
        

    def get_iam_token_from_endpoint(self, api_key=None, endpoint_url=None):
        """Fetch IAM token from the endpoint using the API key."""
        if not self.api_key or not self.endpoint_url:
            return None
        headers = {'Authorization': f'Api-Key {self.api_key}'}
        response = req.get(self.endpoint_url, headers=headers)
        try:
            #token = response.json().get('token').get('access_token')
            token = response.json()
        except (AttributeError, ValueError):
            token = None
        return token
    def file_exists(self,json_file_path=None):
        if json_file_path:
            return os.path.isfile(json_file_path)
    def get_iam_token_from_file(self,json_file_path=None):
        """Fetch IAM token from a JSON file."""
        if not os.path.isfile(json_file_path):
            return None
        with open(self.json_file_path) as json_file:
            json_dict = json.load(json_file)
            service_account_id=json_dict.get("service_account_id")
            key_id=json_dict.get("id")
            private_key = json_dict.get("private_key")
            now = int(time.time())
            payload = {
                    'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
                    'iss': service_account_id,
                    'iat': now,
                    'exp': now + 360}
            encoded_token = jwt.encode(
                payload,
                private_key,
                algorithm='PS256',
                headers={'kid': key_id})
            jwt_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
            headers = {"Accept": "application/json"}
            data = "{'jwt':'" + encoded_token + "'}"
            response = req.post(jwt_url,headers=headers,data=data)
            data = json.loads(response.text)
            return data["iamToken"]

class DatesHelper():
    def __init__(self):
        pass
        
    def get_days_between(self, start: str, end: str) -> int:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        return (end_date - start_date).days

    def get_next_month_last_day(self) -> str:
        today = date.today()
        next_month = (today.year, today.month % 12 + 1) if today.month < 12 else (today.year + 1, 1)
        last_day = calendar.monthrange(next_month[0], next_month[1])[1]
        return today.replace(month=next_month[1], year=next_month[0], day=last_day).strftime("%Y-%m-%d")

    def get_next_month_first_day(self) -> str:
        today = date.today()
        next_month = (today.year, today.month % 12 + 1) if today.month < 12 else (today.year + 1, 1)
        return today.replace(month=next_month[1], year=next_month[0], day=1).strftime("%Y-%m-%d")



