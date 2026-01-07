from sqlmodel import SQLModel,create_engine,Field,Relationship
from typing import Optional,List
from pydantic import BaseModel


# Pydantic model for creating a new user (request)
class UserCreate(BaseModel):
    name:str
    email:str
    password:str

# Pydantic model for reading user data (response)
# This ensures the hashed_password is never exposed.

class UserPublic(BaseModel):
    id:int
    email:str
    name:str

# Pydantic model for the token response

class Token(BaseModel):
    access_token:str
    token_type:str
    
class Hero(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    name:str=Field(index=True) # index=True makes searching by name faster
    email:str=Field(unique=True)
    hashed_password:str
    # The "Relationship" links this User model to the Workout model.
    # It tells SQLModel that the 'workouts' attribute is not a database column
    # but a list of related Workout objects.
    # 'back_populates' points to the 'user' attribute on the Workout model.
    workouts: List["Workout"] = Relationship(back_populates="user")


class Workout(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    name:str=Field(index=True)
    #user_id:Optional[int]=Field(default=None,foreign_key=True)this is wrong
    hero_id: int = Field(foreign_key="hero.id")
    # The relationship back to the User model.
    # This allows you to access workout.user to get the User object.
    user: Hero = Relationship(back_populates="workouts")
 
    # The forward relationship to the Exercise model.
    exercises: List["Exercise"] = Relationship(back_populates="workout")

class Exercise(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    workout_id:int=Field(foreign_key="workout.id")
    
    # The relationship back to the Workout model.
    workout: Workout = Relationship(back_populates="exercises")
    
# This is the "input" model. It defines what a client must provide
# when they want to create a new workout.
class WorkoutCreate(BaseModel):
    name:str

# This is the "output" model. It defines the rich data structure we
# will send back to the client after a successful operation.
class WorkoutPublic(WorkoutCreate):
    id:int
    hero_id:int
    user:UserPublic
    exercises:List["ExercisePublic"]

# Pydantic model for reading an exercise
# A simple output model for exercises, used within WorkoutPublic.
class ExercisePublic(BaseModel):
    id:int
    name:str
    sets:int
    reps:int
    weight:Optional[float]=None

class ExerciseCreate(BaseModel):
    exercise_list:List[str]=[]
# Pydantic model for creating an exercise (request)
class ExerciseCreate(BaseModel):
    name:str
    sets:int
    reps:int
    weight:Optional[float]=None

# Pydantic model for updating an exercise (request)
# All fields are optional so the client can update just one if they want.
class ExerciseUpdate(BaseModel):
    name:Optional[str]=None
    sets:Optional[int]=None
    reps:Optional[int]=None
    weight:Optional[float]=None


# This is needed to help Pydantic work with the SQLAlchemy relationships
# This line helps Pydantic resolve the reference to "ExercisePublic"
# which is defined after it is used in the WorkoutPublic model.
WorkoutPublic.model_rebuild()
ExercisePublic.model_rebuild()
# update_forward_refs: This is a technical helper function. 
# When Python reads WorkoutPublic, it hasn't seen the definition for ExercisePublic yet. 
# This line tells Pydantic to go back after everything is defined and correctly link the two models together.

