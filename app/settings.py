import os

USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
HOST = os.environ.get("MYSQL_HOST", default="localhost")
DATABASE = os.environ.get("MYSQL_DATABASE")
PORT = os.environ.get("MYSQL_PORT", default=3306)
ALGORITHM = os.environ.get("ALGORITHM")
SECRET_KEY = os.environ.get("SECRET_KEY")

GITHUB = {
    "client_id": os.environ.get("GITHUB_CLIENT_ID"),
    "client_secret": os.environ.get("GITHUB_CLIENT_SECRET"),
    "callback_uri": os.environ.get("GITHUB_CALLBACK_URI")
}
