import json
import secrets
import jwt
from typing import List

from fastapi import FastAPI, Response, UploadFile
from fastapi.responses import ORJSONResponse
from fastapi_sso.sso.github import GithubSSO
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.lib.function import *
from app.lib.sql import *
from app.models import MemberIn, MemberOut, Category, CategoryOut, MemberWithCategory, MemberHasCategoryIn, \
    GetMemberHasNetwork, Network, MemberHasNetwork, MemberHasCategory, MemberHasNetworkIn
from app.settings import *

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

github_sso = GithubSSO(GITHUB["client_id"], GITHUB["client_secret"], f"{GITHUB['callback_uri']}/github/callback")


@app.get("/github/login")
async def github_login():
    """Generate login url and redirect"""
    return await github_sso.get_login_redirect()


@app.get("/github/callback")
async def github_callback(request: Request):
    """Process login response from Google and return user info"""
    user = await github_sso.verify_and_process(request)
    member = await get_member_by_username(user.display_name)
    if member is None:
        member_id = await register_new_member(user.display_name)
    else:
        member_id = member.id
    access_token = secrets.token_hex(16)
    refresh_token = secrets.token_hex(16)
    user_id = 1
    await register_token(access_token, refresh_token, member_id)
    token_data = {"user_id": user_id, "access_token": access_token, "refresh_token": refresh_token}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    # Créez un cookie HTTP avec le token
    response = JSONResponse(content={"message": "Bienvenue sur la page réservée aux utilisateurs connectés !"})
    response.set_cookie(key="access_token", value=token, httponly=True)
    # Redirigez l'utilisateur vers la page de profil
    url_response = f"http://localhost:5173/profil/{user_id}"
    response.headers["Location"] = url_response  # Réglez l'URL de redirection
    response.status_code = 303  # Utilisez le code de statut 303 pour indiquer une redirection
    return response


@app.get("/members", response_model=List[MemberWithCategory])
async def api_get_members():
    return await get_members()


@app.get("/members/{id:int}", response_model=MemberIn)
async def api_get_member_by_id(id: int):
    member = await get_member_by_id(id)
    if member is None:
        return Response(status_code=404)
    return member


@app.patch("/members")
async def api_patch_member_update(member: MemberOut):
    result = await patch_member_update(member)
    if result is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.get("/categories", response_model=List[Category])
async def api_get_categories():
    return await get_categories()


@app.post("/categories")
async def api_post_category(category: CategoryOut):
    result = await post_category(category)
    if result is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.get("/members/category={name:str}")
async def api_get_members_category(name: str):
    member = await get_members_category(name)
    if member is None:
        return Response(status_code=404)
    return member


@app.post("/members/category")
async def api_post_add_category_on_member(member: MemberHasCategoryIn):
    category = await post_add_category_on_member(member)
    if category is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.get("/network", response_model=List[Network])
async def api_get_network():
    return await get_network()


@app.get("/members/network", response_model=List[GetMemberHasNetwork])
async def api_get_network_of_member(id_member: int):
    return await get_network_of_member_by_id(id_member)


@app.get("/members/list_category/{id:int}", response_model=List[CategoryOut])
async def api_get_category_of_member_by_id(id: int):
    return await get_category_of_member_by_id(id)


@app.post("/members/network")
async def api_post_network_on_member(member: MemberHasNetwork):
    network = await post_network_on_member(member)
    if network is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.delete("/members/category")
async def api_delete_category_delete_by_member(member: MemberHasCategory):
    verif = await delete_category_delete_by_member(member)
    if verif is not None:
        return Response(status_code=400)
    return Response(status_code=200)


@app.delete("/members/network")
async def api_delete_network_delete_by_member(member: MemberHasNetworkIn):
    verif = await delete_network_delete_by_member(member)
    if verif is not None:
        return Response(status_code=400)
    return Response(status_code=200)


@app.post("/members/image_portfolio")
async def api_add_image_portfolio(file: UploadFile, id_member: int):
    if file.size > 200 * 10000:
        return Response(status_code=413)
    if file.content_type not in ['image/jpeg', 'image/png']:
        return Response(status_code=415)
    if verifIsPngAndJpeg(file) is None:
        return Response(status_code=415)
    verif = await add_image_portfolio(file, id_member)
    if verif is not None:
        return Response(status_code=500)
    return Response(status_code=200)


@app.get("/members/image_portfolio_by_id")
async def api_get_image_portfolio_by_id_member(id_member: int):
    return Response(content=await get_image_by_id_member(id_member), media_type="image/jpg")
