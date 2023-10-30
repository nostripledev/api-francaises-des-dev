from pydantic import BaseModel
from datetime import datetime


class Session(BaseModel):
    token_refresh = str
    id_member = int
    token_session = str
    date_created = datetime

