from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session,select
from ..security import get_current_user
from ..database import get_session
from ..models import Exercise,Hero,ExerciseCreate,Workout,ExerciseUpdate,ExercisePublic


router=APIRouter(prefix="/exercise",tags=["exercise"])
# A helper function to get the parent workout and verify ownership
# This will be used in multiple endpoints below or its a dependency function
def get_workout_and_verify_ownership(workout_id:int,current_user:Hero,db:Session):
    workout=db.get(Workout,workout_id)
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Workout not found")
    if workout.hero_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not authorized to access this workout")
    return workout

@router.post("/workout/{workout_id}/exercise",response_model=ExercisePublic)
def add_exercise(workout_id:int,exercise:ExerciseCreate,db:Session=Depends(get_session),current_user:Hero=Depends(get_current_user)):
    # First, verify the parent workout exists and belongs to the user
    get_workout_and_verify_ownership(workout_id,current_user,db) # authorization check
    # db_user=db.exec(select(Workout).where(Workout.id==workout_id and Workout.hero_id==current_user.id))
    # if not db_user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db_exercise=Exercise.model_validate(exercise,update={'workout_id':workout_id})
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)

    return db_exercise

@router.get("/exercise/{workout_id}",response_model=List[ExercisePublic])
def get_exercise(workout_id:int,db:Session=Depends(get_session),current_user:Hero=Depends(get_current_user)):
    # Verify ownership of the parent workout
    workout=get_workout_and_verify_ownership(workout_id,current_user,db)
    # The relationship 'workout.exercises' automatically contains the linked exercises
    return workout.exercises
    # db_exercise=db.exec(select(Exercise).where(Exercise.workout_id==workout_id))
    # if not db_exercise:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="exercise not found")
    # db_user=db.exec(select(Workout).where(Workout.id==workout_id and Workout.hero_id==current_user.id))
    # if not db_user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    # return db_exercise
@router.put("/update/{exercise_id}",response_model=ExercisePublic)
def update_exercise(workout_id:int,exercise_id:int,exercise_update:ExerciseUpdate,db:Session=Depends(get_session),current_user:Hero=Depends(get_current_user)):
    # Verify ownership of the parent workout
    get_workout_and_verify_ownership(workout_id,current_user,db)
    db_exercise=db.get(Exercise,exercise_id)
    if not db_exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Exercise not found")
    # Second check: ensure the exercise belongs to the correct workout
    if db_exercise.workout_id!=workout_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Exercise does not belong to the specified workout")
    # Get the update data, excluding any fields that were not set

    update_data=exercise_update.model_dump(exclude_unset=True)
    # Update the model's attributes
    for key, value in update_data.items():
        setattr(db_exercise, key, value)
    db.add(db_exercise) 
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.delete("/delete/{exercise_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(workout_id:int,exercise_id:int,db:Session=Depends(get_session),current_user:Hero=Depends(get_current_user)):
    db_exercise=db.get(Exercise,exercise_id)
    if not db_exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Exercise not found")
    # Verify ownership of the parent workout
    get_workout_and_verify_ownership(db_exercise.workout_id,current_user,db)
    # Second check: ensure the exercise belongs to the correct workout
    if db_exercise.workout_id!=workout_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Exercise does not belong to the specified workout")
    db.delete(db_exercise)
    db.commit()
    return
    

    
