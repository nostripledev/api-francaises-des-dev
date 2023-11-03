from __future__ import annotations

import json

import jwt
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.lib.sql import verif_session, delete_session

from app.settings import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/session",
    tags=["session"]
)


@router.get("/")
async def api_is_connected(request: Request, id_member: int):
    try:
        access_token = request.cookies.get("access_token")
        token_user = request.cookies.get("token_user")
        token_user = int(token_user)
        cookie_session_decode = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
        if cookie_session_decode["user_id"] == token_user and id_member == cookie_session_decode["user_id"]:
            if await verif_session(cookie_session_decode):
                return {"status": 200}
            else:
                return {"status": 401}
        else:
            return {"status": 401}
    except Exception as e:
        print(e)
        return {"status": 400}


@router.delete("/delete")
async def api_delete_session(id_member: int):
    await delete_session(id_member)
    url_response = "http://127.0.0.1:5137/"
    response = RedirectResponse(url=url_response)
    return response
