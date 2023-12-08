import requests
import settings
from src.server.database.pydantic_models import LoginData, Users

def server_available(func):
    def need_it(*args, **kwargs):
        try:
            requests.get(url=settings.URL)
            print(1)
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            print(2)
            return {'code': 400, 'msg': 'Server is not available', 'result': None}
    
    return need_it

@server_available
def check_connection():
    return True

@server_available
def login(data: LoginData) -> dict:
    return requests.get(url=f'{settings.URL}/users/login', data=f'{{"login": "{data.login}", "password": "{data.password}"}}').json()

@server_available
def register(data: Users) -> dict:
    return requests.get(url=f'{settings.URL}/users/new', data=f'{{"id": 0, "type_id": {data.type_id}, "login": "{data.login}", "password": "{data.password}"}}')
