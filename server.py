import uvicorn
import fastapi
import settings
from src.server.advanced_import import *

app = fastapi.FastAPI(
    title='MuseumAPI 2023-2024y', 
    version='PreAlpha 0.1', 
    description='This API is designed to improve the work of museums around the world!'
)

[app.include_router(router=rout) for rout in routers]

@app.get(path='/', include_in_schema=False)
def index() -> fastapi.responses.RedirectResponse:
    return fastapi.responses.RedirectResponse('/docs')


def start_server():
    uvicorn.run(app='server:app', reload=True, host=settings.HOST, port=settings.PORT)


if settings.DEBUG:
    if __name__ == "__main__":
        start_server()