from pydantic import BaseModel
from typing import Optional


class ModifyBaseModel(BaseModel):
    id: Optional[int] = 0

class TypesUsers(ModifyBaseModel):
    title: str
    power_level: int

class Users(ModifyBaseModel):
    type_id: int
    login: str
    password: str

class Cities(ModifyBaseModel):
    name: str
    coordinates: str

class ExcursionFind(ModifyBaseModel):
    name: str

class Excursion(ExcursionFind):
    city: int
    cost: float

class ListUsersOnExcursion(ModifyBaseModel):
    user_id: int
    excursion_id: int

class Rooms(ModifyBaseModel):
    title: str

class Itineraries(ModifyBaseModel):
    room_id: int
    excursion_id: int

class UserAuth(BaseModel):
    userID: int
    login: str
    password: str
    power_level: int

class LoginData(BaseModel):
    login: str
    password: str

