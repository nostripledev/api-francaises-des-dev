import os

user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST", default="localhost")
database = os.environ.get("MYSQL_DATABASE")
port = os.environ.get("MYSQL_PORT", default=3306)


HOST = "127.0.0.1"
USER = "root"
PASSWORD = "root"
DB = "API_francaises_des_dev"
PORT = 8889
