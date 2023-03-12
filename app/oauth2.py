from .config import settings
from jose import JWSError, jwt
from datetime import datetime, timedelta
from . import schema, database, model
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY =
#Algorithm
#Expiration Time

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES   #Token will expire in 60 minutes

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return encoded_jwt

def verify_access_token(token:str, credentials_exception:JWSError):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        id:str = payload.get("user_id") # type: ignore

        if id is None:
            raise credentials_exception 
        token_data = schema.TokeData(id=id)
    except JWSError:
        raise credentials_exception
    
    return token_data


def get_current_user(token:str = Depends(oauth2_schema),db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token , credentials_exception) # type: ignore
    user = db.query(model.User).filter(model.User.id == token.id).first() # type: ignore
    return user 
