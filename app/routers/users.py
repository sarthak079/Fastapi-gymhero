# This is the public endpoint where anyone can create a new account.
from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select
from ..database import get_session
from ..models import Hero,UserCreate,UserPublic
from app.security import get_password_hash,get_current_user

router=APIRouter(prefix="/users",tags=["Users"])

@router.post("/",response_model=UserPublic)
def create_user(user:UserCreate,db: Session=Depends(get_session)):
    # Check if user with that email already exists
    existing_user=db.exec(select(Hero).where(Hero.email==user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    
    #Hash the password before storing it
    hashed_password=get_password_hash(user.password)

    # Create a new User object, excluding the plaintext password
    db_user=Hero(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
     
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# This endpoint proves our authentication system works. 
# Only users with a valid token can access it.
@router.get("/me",response_model=UserPublic)
def read_users_me(current_user:Hero=Depends(get_current_user)):
    # The 'get_current_user' dependency handles all the security.
    # If the token is invalid, the code will never reach here.
    # If it's valid, 'current_user' will contain the authenticated user's data.

    return current_user
