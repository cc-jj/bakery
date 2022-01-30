from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src import routes


app = FastAPI()
app.include_router(routes.auth.router)
app.include_router(routes.v1.router)
add_pagination(app)
