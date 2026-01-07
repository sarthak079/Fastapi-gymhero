from fastapi import FastAPI,Depends
from sqlmodel import Field, create_engine, Session, select, SQLModel
from .database import get_session,create_db_and_tables
from .models import Hero, Workout, Exercise
from app.routers import users, auth,workout,exercises

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include the routers in the app
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(workout.router)
app.include_router(exercises.router)

@app.post("/heroes/",response_model=Hero)
def create_hero(hero:Hero,session:Session=Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/")
def read_root():
    return {"Hello": "World"}


