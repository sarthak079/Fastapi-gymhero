#This endpoint is for existing users to exchange their credentials for a JWT.
from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session,select

from app.database import get_session
from app.models import Hero,Token
from app.security import create_access_token,verify_pass

router=APIRouter(tags=["Authentication"])

@router.post("/token",response_model=Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_session)):
    user=db.exec(select(Hero).where(Hero.name==form_data.username)).first()

    # Verify user exists and password is correct
    if not user or not verify_pass(form_data.password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    #Create and return the access token
    access_token=create_access_token(data={"sub":user.name})
    return {"access_token":access_token,"token_type":"bearer"}


