import requests
import sys

sys.path.append('C:/museum_app')

import settings
from src.server.database.pydantic_models import LoginData, Users

def server_available(func):
    def need_it(*args, **kwargs):
        try:
            requests.get(url=settings.URL)
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError:
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
    return requests.post(url=f'{settings.URL}/users/new', data=f'{{"id": 0, "type_id": {data.type_id}, "login": "{data.login}", "password": "{data.password}"}}').json()

@server_available
def update_password(data: Users) -> dict:
    return requests.put(url=f'{settings.URL}/users/change', data=f'{{"login": "{data.login}", "password": "{data.password}"}}').json()

@server_available
def get_all_excursions() -> dict:
    return requests.get(url=f'{settings.URL}/excursions/get_all').json()

def search_excursions(name: str) -> dict:
    return requests.get(url=f'{settings.URL}/excursions/search', data=f'{{"name": "{name}"}}').json()

def get_city_per_id(id: int) -> dict:
    return requests.get(url=f'{settings.URL}/cities/get/{id}').json()

def delete_account(id: int) -> dict:
    return requests.delete(url=f'{settings.URL}/users/delete/{id}').json()