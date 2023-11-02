from __future__ import annotations

from typing import Optional, Union, Annotated

import jwt
from fastapi import APIRouter, Cookie, Header
from starlette.requests import Request

from app.lib.sql import verif_session
from starlette.responses import Response

from app.models.session import SessionCookie
from app.settings import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/session",
    tags=["session"]
)


@router.get("/")
async def api_is_connected(request: Request):
    try:
        access_token = request.cookies.get('access_token')
        cookie_session_decode = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
        print(cookie_session_decode)
        if await verif_session(cookie_session_decode):
            return {"status": 200}
        else:
            return {"status": 401}
    except Exception as e:
        print(e)
        return {"status": 400}
