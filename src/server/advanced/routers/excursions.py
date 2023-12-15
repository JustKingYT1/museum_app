from src.server.router import routers
from src.server.database.pydantic_models import ExcursionFind
from src.server.advanced.resolvers.excursions import find_excursions


rout = routers[4]

@rout.get(path='/search', response_model=dict)
def search_excursions(data: ExcursionFind) -> dict:
    return find_excursions(data=data)