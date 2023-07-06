# api-francaises-des-dev
           
## To set up the project

Install dependence :

```
pip install -r requirements.txt 
```

Change .env.example to set up the database :

```
MYSQL_USER = ""
MYSQL_PASSWORD = ""
MYSQL_DATABASE = ""
MYSQL_PORT = 3306
MYSQL_HOST = "localhost"
```

remove .example extension from the file .env.example

To start the server :

```
uvicorn app.main:app --reload
```

>⚠️ You need a virtual environment -> see the FastAPI document

