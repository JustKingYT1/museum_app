import fastapi
import peewee
from typing import Type
from src.server.database.models import BaseModel
from src.server.database.pydantic_models import ModifyBaseModel

class RouterManager:
    def __init__(
            self, 
            database_model: Type[BaseModel], 
            pydantic_model: Type[ModifyBaseModel], 
            prefix: str, 
            tags: [str]) -> None:
        self.pydantic_model = pydantic_model
        self.database_model = database_model
        self.fastapi_router: fastapi.APIRouter = fastapi.APIRouter(prefix=prefix, tags=tags)
        self.resolver_manager = ResolverManager(self.database_model, self.pydantic_model)
        self.__init_routers()
    
    def __init_routers(self):
        pm = self.pydantic_model

        @self.fastapi_router.get(path='/get_all', response_model=dict)
        def get_all_records():
            return self.resolver_manager.get_all()
        
        @self.fastapi_router.get(path='/get/{id}', response_model=dict)
        def get_record(id: int): 
            return self.resolver_manager.get(id=id)
        
        @self.fastapi_router.post(path='/new', response_model=dict)
        def new(new_model: pm):
            return self.resolver_manager.new(new_model=new_model)
        
        @self.fastapi_router.put(path='/update/{id}', response_model=dict)
        def update(id: int, new_model: pm):
            return self.resolver_manager.update(id=id, new_model=new_model)
        
        @self.fastapi_router.delete(path='/delete/{id}', response_model=dict)
        def delete(id: int):
            return self.resolver_manager.delete(id=id)
        

class ResolverManager:
    def __init__(self, database_model: Type[BaseModel], pydantic_model: Type[ModifyBaseModel]) -> None:
        self.database_model = database_model
        self.pydantic_model = pydantic_model

    def check_for_errors(self, id=0) -> dict:
        try:
            self.get(id)
            return {'code': 200, 'msg': 'Successfully', 'result': False}
        except peewee.DatabaseError as ex:
            return {'code': 400, 'msg': str(ex), 'result': True}
        except peewee.InternalError as ex:
            return {'code': 400, 'msg': str(ex), 'result': True}
        except peewee.IntegrityError as ex:
            return {'code': 400, 'msg': str(ex), 'result': True}
        except peewee.InterfaceError as ex:
            return {'code': 400, 'msg': str(ex), 'result': True}
        except peewee.OperationalError as ex:
            return {'code': 400, 'msg': str(ex), 'result': True}
        

    def new(self, new_model: Type[ModifyBaseModel]) -> dict:
        check = self.check_for_errors()
        if check['result']:
            return check

        
        new_database_model = self.database_model.create()

        for atr in dir(new_model):
            if atr.startswith('__') or atr.startswith('id'):
                continue
            setattr(new_database_model, atr, getattr(new_model, atr))

        new_database_model.save()

        return self.get(id=new_database_model.id)

    def get(self, id: int) -> dict:
        try:
            check = self.check_for_errors()
            if check["result"]:
                return check
        except RecursionError:
            pass

        try:
            return {'code': 200, 'msg': 'Succesfully', 'result': self.database_model.get(self.database_model.id == id).__data__}
        except peewee.DoesNotExist as ex:
            return {'code': 400, 'msg': 'Not found', 'result': None}
    
    def get_all(self) -> dict:
        check = self.check_for_errors()
        if check['result']:
            return check
        models_list = []
        for model in self.database_model.select():
            new_model = {}

            for atr in model.__data__:
                get_atr = getattr(model, atr)

                new_model[atr] = get_atr.id if isinstance(get_atr, peewee.Model) else get_atr

            models_list.append(new_model)

        return {'code': 200, 'msg': 'Succesfully', 'result': models_list} if len(models_list) > 0 else {'code': 400, 'msg': 'Not found', 'result': None}
    
    def update(self, id: int, new_model: Type[ModifyBaseModel]) -> dict:
        check = self.check_for_errors()
        if check['result']:
            return check
        
        self.get(id=id)
        
        model = self.database_model.get(self.database_model.id == id)

        for atr in dir(new_model):
            if atr.startswith('__') or atr.startswith('id'):
                continue

            setattr(model, atr, getattr(new_model, atr))

        model.save()

        return {"code": 200, 'msg': 'Successfully', 'result': self.get(id=model.id)['result']}
    
    def delete(self, id: int) -> dict:
        check = self.check_for_errors()
        if check['result']:
            return check
        result = self.get(id=id)
        if result['code'] != 200:
            return result
        self.database_model.get(self.database_model.id == id).delete_instance()
        result['result'] = None
        return result
    