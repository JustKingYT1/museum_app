from src.server.database import models as database_models
from src.server.database import pydantic_models
from src.server.service import RouterManager

routers = (
    RouterManager(
        database_model=database_models.Cities,
        pydantic_model=pydantic_models.Cities,
        prefix='/cities',
        tags=['Cities']
    ).fastapi_router,

    RouterManager(
        database_model=database_models.TypesUsers,
        pydantic_model=pydantic_models.TypesUsers,
        prefix='/types',
        tags=['TypesUsers']
    ).fastapi_router,

    RouterManager(
        database_model=database_models.Users,
        pydantic_model=pydantic_models.Users,
        prefix='/users',
        tags=['Users']
    ).fastapi_router,

    RouterManager(
        database_model=database_models.ListUsersOnExcursion,
        pydantic_model=pydantic_models.ListUsersOnExcursion,
        prefix='/list',
        tags=['ListUsersOnExcursion']
    ).fastapi_router,
    
    RouterManager(
        database_model=database_models.Excursions,
        pydantic_model=pydantic_models.Excursions,
        prefix='/excursions',
        tags=['Excursions']
    ).fastapi_router,

    RouterManager(
        database_model=database_models.Rooms,
        pydantic_model=pydantic_models.Rooms,
        prefix='/rooms',
        tags=['Rooms']
    ).fastapi_router,

    RouterManager(
        database_model=database_models.Itineraries,
        pydantic_model=pydantic_models.Itineraries,
        prefix='/itineraries',
        tags=['Itineraries']
    ).fastapi_router
)