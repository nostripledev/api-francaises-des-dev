import secrets

import jwt
from fastapi import APIRouter, Response
from starlette.responses import RedirectResponse

from fastapi_sso.sso.github import GithubSSO
from app.lib.sql import *
from starlette.requests import Request

from app.settings import GITHUB

# Clé secrète pour signer le token JWT
SECRET_KEY = "votre_clé_secrète"
# Algorithme de signature JWT
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/github",
    tags=["github"]
)


github_sso = GithubSSO(GITHUB["client_id"], GITHUB["client_secret"], f"{GITHUB['callback_uri']}/github/callback")


@router.get("/login")
async def github_login():
    """Generate login url and redirect"""
    return await github_sso.get_login_redirect()


@router.get("/callback")
async def github_callback(request: Request) -> Response:
    """Process login response from Google and return user info"""
    user = await github_sso.verify_and_process(request)
    member = await get_member_by_username(user.display_name)
    if member is None:
        member_id = await register_new_member(user.display_name)
    else:
        member_id = member.id
    access_token = secrets.token_hex(16)
    refresh_token = secrets.token_hex(16)
    await register_token(access_token, refresh_token, member_id)
    token_data = {"user_id": member_id, "access_token": access_token, "refresh_token": refresh_token}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    # Redirigez l'utilisateur vers la page de profil
    url_response = f"http://localhost:5173/profil/{member_id}"
    response = RedirectResponse(url=url_response)
    # Créez un cookie HTTP avec le token
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response
