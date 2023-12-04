import peewee
import settings

db = peewee.SqliteDatabase(database=f'{settings.DB_PATH}/{settings.DB_NAME}')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class TypesUsers(BaseModel):
    title: peewee.CharField = peewee.CharField(max_length=15, unique=True)
    power_level: peewee.IntegerField = peewee.IntegerField(unique=True) 

class Users(BaseModel):
    typeID: peewee.ForeignKeyField = peewee.ForeignKeyField(model=TypesUsers, related_name='fk1_users_of_type_users', on_delete="CASCADE")
    login: peewee.CharField = peewee.CharField(max_length=20, unique=True)
    password: peewee.CharField = peewee.CharField(max_length=25)

class Cities(BaseModel):
    name: peewee.CharField = peewee.CharField(max_length=50, unique=True)
    coordinates: peewee.CharField = peewee.CharField(max_length=20, unique=True)

class Excursions(BaseModel):
    cityID: peewee.ForeignKeyField = peewee.ForeignKeyField(model=Cities, related_name='fk2_cities_of_excursions', on_delete="CASCADE")
    name: peewee.CharField = peewee.CharField(max_length=50, unique=True)
    cost: peewee.FloatField = peewee.FloatField()

class ListUsersOnExcursion(BaseModel):
    userID: peewee.ForeignKeyField = peewee.ForeignKeyField(model=Users, related_name='fk3_users_of_list_users_on_excursion', on_delete="CASCADE")
    excursionID: peewee.ForeignKeyField = peewee.ForeignKeyField(model=Excursions, related_name='fk4_excursion_of_list_users_on_excursion', on_delete="CASCADE")
    class Meta:
        database = db
        constraints = [peewee.Check('userID || excursionID NOT IN (SELECT userID || excursionID FROM ListUsersOnExcursion)')]

class Rooms(BaseModel):
    title: peewee.CharField = peewee.CharField(max_length=25, unique=True)

class Itineraries(BaseModel):
    roomID: peewee.ForeignKeyField = peewee.ForeignKeyField(model=Rooms, related_name='fk5_room_of_itineraries', on_delete='CASCADE')
    excursionID: peewee.ForeignKeyField = peewee.ForeignKeyField(model=Excursions, related_name='fk6_excursion_of_itineraries', on_delete="CASCADE")
    class Meta:
        database = db
        constraints = [peewee.Check('roomID || excursionID in (SELECT roomID || excursionID FROM itineraries)')]