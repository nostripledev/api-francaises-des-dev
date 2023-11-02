from pydantic import BaseModel
from datetime import datetime


class SessionCookie(BaseModel):
    access_token = str
    id_member = int
    refresh_token = str


class Session(SessionCookie):
    date_created = datetime

