from src.server.router import routers
from src.server.database.pydantic_models import LoginData
from src.server.advanced.resolvers.users import log_in, change_password
from fastapi import FastAPI


rout: FastAPI = routers[2]

@rout.get(path='/login', response_model=dict)
def login(data: LoginData) -> dict:
    return log_in(login=data.login, password=data.password)

@rout.put(path='/change', response_model=dict)
def change(data: LoginData) -> dict:
    return change_password(login=data.login, password=data.password)