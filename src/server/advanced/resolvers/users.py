from src.server.database.models import Users, TypesUsers
from src.server.database.pydantic_models import UserAuth

def log_in(login: str, password: str) -> dict:
    user = Users.get_or_none(Users.login == login, Users.password == password)
    return {'code': 200, 'msg': 'Succesfully', 'result': UserAuth(
            userID=user.id,
            login=user.login,
            password=user.password,
            power_level=TypesUsers.get_or_none(TypesUsers.id == user.type_id).power_level)} if user else {'code': 400, 'msg': 'Not found', 'result': None}    
        
def change_password(login: str, password: str) -> dict:
    user = Users.get_or_none(Users.login == login)
    if user:
        user.password = password
        user.save()
    return {'code': 200, 'msg': 'Succesfully', 'result': UserAuth(
        userID=user.id,
        login=user.login,
        password=user.password,
        power_level=TypesUsers.get_or_none(TypesUsers.id == user.type_id).power_level
    )} if user else {'code': 400, 'msg': 'Not found', 'result': None}