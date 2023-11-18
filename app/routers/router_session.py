from __future__ import annotations

import jwt
from fastapi import APIRouter
from starlette.requests import Request
from fastapi.responses import RedirectResponse

from app.lib.sql import verif_session, delete_session
from app.auth.auth import *

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
async def api_delete_session(id_member: str, current_user: dict = Depends(get_current_user)):
    id_user = int(id_member)
    await delete_session(id_user)
    return RedirectResponse("http://127.0.0.1:5173/")
