from fastapi import Request, HTTPException, Depends
import jwt
from typing import Optional
from app.settings import SECRET_KEY, ALGORITHM
from app.lib.sql import verif_session


async def get_current_user(request: Request, id_member: int):
    try:
        access_token = request.cookies.get("access_token")
        token_user = request.cookies.get("token_user")
        token_user = int(token_user)
        cookie_session_decode = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
        if (
                cookie_session_decode["user_id"] == token_user
                and id_member == cookie_session_decode["user_id"]
                and await verif_session(cookie_session_decode)
        ):
            return cookie_session_decode
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid token")
