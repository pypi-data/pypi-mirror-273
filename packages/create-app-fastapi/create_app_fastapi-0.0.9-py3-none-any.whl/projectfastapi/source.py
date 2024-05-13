# main file data
def main(name):
    result= '{"message": "Service is running"}'
    return f"""from fastapi import FastAPI
from APIs import api

app = FastAPI(
    title="{name} API",
    version="1.0"
)

@app.get('/')
def root():
    return {result}

# include api routes with main app
app.include_router(api.app)

"""
# gitignore file data
def gitignore(venv):
    return f"""__pycache__
    .pytest_cache
{venv}/
.env
"""

# auth file
def auth():
    return """from fastapi.security import OAuth2PasswordBearer

#jwt token code here
def genToken():
    pass

def authenticate():
    pass

#user password encrypt verify
def encrypt_pwd():
    pass

def verify_pwd():
    pass
"""

# env file
def env(data:dict):
    return """# environment varibales here
DATABASE=<dbname>
DBUSER=<dbusername>
PASSWORD=<db password>
HOST=<db host>
PORT=<db port>
""" if not data.keys() else f"""# environment varibales here
DATABASE={data['database']}
DBUSER={data['dbuser']}
PASSWORD={data['password']}
HOST={'localhost' if data['host']=='' else data['host']}
PORT={data['port']}
"""

# config file
def config():
    return """from pydantic_settings import BaseSettings, SettingsConfigDict
    
# env variable access code here
class Secret(BaseSettings):
    database: str
    dbuser: str
    password: str
    host: str
    port: str
    
    model_config= SettingsConfigDict(env_file=".env")
    
secret= Secret()

"""

#db file
def db(data:dict):
    db= False
    if data.keys():
        if data['db'].lower()=='mysql':
            driver= 'mysql+mysqlconnector'
        else:
            driver= 'postgresql'
        db=f"""
db_url= URL.create(
    drivername= '{driver}',
    username= secret.dbuser,
    password= secret.password,
    host= secret.host,
    port= secret.port
)

engine= create_engine(db_url, pool_pre_ping= True)
session_local= sessionmaker(autocommit= False, autoflush= False, bind= engine)
Base= declarative_base()

def get_db():
    db= session_local()
    try:
        yield db
    finally:
        db.close()

try:
    db= session_local()
    db.execute(text('SELECT 1'))
    print('\\n----- Connected to db! -----')
except Exception as e:
    print('\\n----- Connection failed! ERROR : ', e)

"""

    return f"""from sqlalchemy import create_engine, URL, {'text' if db else ''}
from sqlalchemy.orm import sessionmaker, declarative_base
from settings.config import secret

# database connection code here
{db if db else ''}
"""
#model file
def model():
    return"""from sqlalchemy import Column, Integer, String, Float
from settings.db import Base

# model code here
"""
#schema file
def schema():
    return """from pydantic import BaseModel

# schema code here
class Sample(BaseModel):
    pass
"""
#api file
def api():
    return """from fastapi import APIRouter
from settings.db import get_db

# api code here
app= APIRouter(
    prefix="/api/v1",
    tags=["api"]
)
@app.get('/')
def initial():
    return {"message": "Serive from API routes"}
"""

#api file
def test_main():
    return """from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# the main service test case
def test_main():
    response= client.get('/')
    assert response.status_code == 200

# the api test case
def test_api():
    response= client.get('/api/v1')
    assert response.status_code == 200
""" 

def getFileData(name, venv, db_data):
    return {
            'auth.py': auth(),
            'config.py': config(),
            'db.py': db(db_data),
            'model.py': model(),
            'schema.py': schema(),
            'api.py': api(),
            'main.py': main(name),
            'test_main.py': test_main(),
            '.gitignore':gitignore(venv),
            '.env':env(db_data),
            }

