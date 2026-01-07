from datetime import datetime,timedelta,timezone
from typing import Optional
from jose import JWTError,jwt
from passlib.context import CryptContext
from fastapi import HTTPException,FastAPI,Depends,status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session,select

# This file will contain all our security logic: password hashing, 
# token creation, and the dependency to get the current logged-in user.
from .database import get_session
from .models import Hero
#configuration
SECRET_KEY="a_super_secret_key_that_is_very_long_and_random" #Use a secrets manager in production
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OAuth2 scheme
oauth2_schem=OAuth2PasswordBearer(tokenUrl="/token")
# Password hashing context
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_pass(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password:str):
    return pwd_context.hash(password[:72])

def create_access_token(data:dict,expires_delta:Optional[timedelta]=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

# The dependency to get the current user
def get_current_user(token:str=Depends(oauth2_schem),db:Session=Depends(get_session)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payloads=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payloads.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user=db.exec(select(Hero).where(Hero.name==username)).first()
    if user is None:
        raise credentials_exception
    
    return user

