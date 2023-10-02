from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .routers import *


app = FastAPI()

# Clé secrète pour signer le token JWT
SECRET_KEY = "votre_clé_secrète"
# Algorithme de signature JWT
ALGORITHM = "HS256"

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router_github.router)
app.include_router(router_member.router)
app.include_router(router_category.router)
app.include_router(router_network.router)
