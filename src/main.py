from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from src import routes


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["Authorization"],
)
app.include_router(routes.auth.router, prefix="/api")
app.include_router(routes.v1.router, prefix="/api")
add_pagination(app)
