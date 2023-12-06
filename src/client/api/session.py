from src.server.database.pydantic_models import UserAuth, Users
from src.client.api.resolvers import login, register
from src.server.database.pydantic_models import LoginData


class Session:
    auth: bool = False
    user: UserAuth = UserAuth(
        userID=-1,
        login='',
        password='',
        access_level=-1
    )
    error: str = None

    def login(self, log_in: str, password: str):
        answer = login(data=LoginData(
            login=log_in,
            password=password))
        
        match answer['code']:
            case 400:
                self.error = answer['msg']

            case 200:
                self.error = None
                self.user = UserAuth(
                    userID=answer['result']['id'],
                    login=answer['result']['login'],
                    password=answer['result']['password'],
                    power_level=answer['result']['power_level']
                )
                self.auth = True
        
    def register(self, type_id: int, login: str, password: str):
        answer = register(data=Users(
            id=0,
            type_id=type_id,
            login=login,
            password=password
        ))
        match answer:
            case 400:
                self.error = answer['msg']
            
            case 200:
                self.error = None

    def leave(self):
        self.user.power_level = -1
        self.user.login = ''
        self.user.password = ''
        self.auth = False