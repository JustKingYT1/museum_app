import sys

sys.path.append('C:/museum_app')

from src.server.database.models import Excursions
from src.server.database.pydantic_models import Excursion, ExcursionFind
import requests
import settings


def find_excursions(data: ExcursionFind) -> dict:
    excursions = Excursions.select().where(Excursions.name ** f'{data.name}%')
    excursions_list = []
    for excursion in excursions:
        excursions_list.append(Excursion(id=excursion.id, name=excursion.name, city=excursion.city_id, cost=excursion.cost))
    
    return {'code': 200, 'msg': 'Succesfully', 'result': excursions_list} if len(excursions_list) > 0 else requests.get(url=f'{settings.URL}/excursions/get_all').json()
 