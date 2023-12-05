import peewee

import sys

sys.path.append('C:/museum_app')

import settings

db = peewee.SqliteDatabase(database=f'{settings.DB_PATH}/{settings.DB_NAME}')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class TypesUsers(BaseModel):
    title: peewee.CharField = peewee.CharField(max_length=15, default='')
    power_level: peewee.IntegerField = peewee.IntegerField(default=0) 

class Users(BaseModel):
    type: peewee.ForeignKeyField = peewee.ForeignKeyField(model=TypesUsers, related_name='fk1_users_of_type_users', on_delete="CASCADE", default=0)
    login: peewee.CharField = peewee.CharField(max_length=20, default='')
    password: peewee.CharField = peewee.CharField(max_length=25, default='')

class Cities(BaseModel):
    name: peewee.CharField = peewee.CharField(max_length=50, default='')
    coordinates: peewee.CharField = peewee.CharField(max_length=20, default='')

class Excursions(BaseModel):
    city: peewee.ForeignKeyField = peewee.ForeignKeyField(model=Cities, related_name='fk2_cities_of_excursions', on_delete="CASCADE", default=0)
    name: peewee.CharField = peewee.CharField(max_length=50, default='')
    cost: peewee.FloatField = peewee.FloatField(default=0)

class ListUsersOnExcursion(BaseModel):
    user: peewee.ForeignKeyField = peewee.ForeignKeyField(model=Users, related_name='fk3_users_of_list_users_on_excursion', on_delete="CASCADE", default=0)
    excursion: peewee.ForeignKeyField = peewee.ForeignKeyField(model=Excursions, related_name='fk4_excursion_of_list_users_on_excursion', on_delete="CASCADE", default=0)
    class Meta:
        database = db
        constraints = [peewee.SQL('UNIQUE(user_id, excursion_id)')]

class Rooms(BaseModel):
    title: peewee.CharField = peewee.CharField(max_length=25, default='')

class Itineraries(BaseModel):
    room: peewee.ForeignKeyField = peewee.ForeignKeyField(model=Rooms, related_name='fk5_room_of_itineraries', on_delete='CASCADE', default=0)
    excursion: peewee.ForeignKeyField = peewee.ForeignKeyField(model=Excursions, related_name='fk6_excursion_of_itineraries', on_delete="CASCADE", default=0)
    class Meta:
        database = db
        constraints = [peewee.SQL('UNIQUE(room_id, excursion_id)')]

db.create_tables([
    TypesUsers,
    Users,
    Cities,
    Excursions,
    ListUsersOnExcursion,
    Rooms,
    Itineraries
])
