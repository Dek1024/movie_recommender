import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime,timedelta
import pytz
import module
import module.modules
import module.schemas
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import loaddotenv

loaddotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user_login")

IST = pytz.timezone('Asia/Kolkata') 

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

def create_access_token(data:dict):
    to_encode = data.copy()
    expire_time = datetime.now(IST) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_time = expire_time.strftime("%Y-%m-%d %H:%M:%S")
    to_encode.update({"expire_time":expire_time})
    encoded_jwt = jwt.encode(to_encode ,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = module.schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail = f"Could not validate credentials",
                                          headers = {"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token,credentials_exception)
    response = module.modules.check_username(token_data.username)
    if response["username"] == token_data.username:
        return token_data
    else:
        raise credentials_exception