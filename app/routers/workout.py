from fastapi import APIRouter,Depends,HTTPException,status
from typing import List
from ..database import get_session
from ..models import Workout,Hero,WorkoutCreate,WorkoutPublic
from ..security import get_current_user
from sqlmodel import select,Session

router=APIRouter(
    prefix="/workouts",tags=["Workouts"]
)
# --- CREATE a new workout ---
@router.post("/",response_model=WorkoutPublic)
def add_workout(workout:WorkoutCreate,current_user:Hero=Depends(get_current_user),db:Session=Depends(get_session)):
    # Create a new Workout instance, linking it to the current user
    #existing_user=db.exec(select(Workout).where(workout.hero_id==current_user.id))
    db_workout=Workout.model_validate(workout,update={'hero_id':current_user.id})
    # db_user=Workout(
    #     name=workout.name
    # )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)

    return db_workout

# --- READ all workouts for the current user ---
@router.get("/",response_model=List[WorkoutPublic])
def workout_list(current_user:Hero=Depends(get_current_user),db:Session=Depends(get_session)):
    # Select only the workouts that belong to the logged-in user
    existing_user=db.exec(select(Workout).where(Workout.hero_id==current_user.id)).all

    return existing_user

# --- READ a single workout by ID ---
@router.get("/{workout_id}",response_model=WorkoutPublic)
def single_workout(workout_id:int,current_user:Hero=Depends(get_current_user),db:Session=Depends(get_session)):
   workout=db.get(Workout,workout_id)
   if not workout:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Workout not found")
   # **Authorization Check**: Ensure the workout belongs to the current user
   if workout.hero_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Workout not found")
   return workout

# @router.put("/update",response_model=Workout)
# def update(workout:Workout,current_user:Depends=(get_current_user),db:Session=Depends(get_session)):
#     db_user=Workout(
#         name=workout.name
#     )
#     db.commit(db_user)
#     db.refresh()
#     return db_user

# --- DELETE a workout ---
@router.delete("/delete/{workout_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(workout_id:int,current_user:Hero=Depends(get_current_user),db:Session=Depends(get_session)):
    # existing_user=db.exec(select(Workout).where(workout.hero_id==current_user.id))
    workout=db.get(Workout,workout_id) #it will return row
    if not workout:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Workout not found")
    if workout.hero_id!=current_user.id:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Workout not found")

    db.delete(workout)
    db.commit()
    return 
    






