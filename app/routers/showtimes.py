from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import Optional, List
from database import database, models
from app import schemas, auth

router = APIRouter(
    prefix='/showtime',
    tags=['Showtimes']
)

@router.get('/', response_model=List[schemas.ShowtimeOut])
def get_all_showtimes(
    db: Session = Depends(database.get_db),
    limit: int = 100
):
    showtimes = db.query(models.Showtime).limit(limit).all()
    return showtimes

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_showtime(
    showtime: schemas.CreateShowtime,
    db: Session = Depends(database.get_db),
    current_admin: int = Depends(auth.get_current_admin)
):
    if not db.query(models.Movie).filter(models.Movie.id == showtime.movie_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID: {showtime.movie_id} doesn't exist")
    if not db.query(models.Screen).filter(models.Screen.id == showtime.screen_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Screen with ID: {showtime.movie_id} doesn't exist")
    showtime_model = models.Showtime(**showtime.model_dump())
    db.add(showtime_model)
    db.commit()
    db.refresh(showtime_model)
    return showtime_model

@router.patch('/{id}')
def update_showtime(
    id: int,
    showtime: schemas.UpdateShowtime,
    db: Session = Depends(database.get_db),
    current_admin: int = Depends(auth.get_current_admin)
):
    showtime_query = db.query(models.Showtime).filter(models.Showtime.id == id)
    if not showtime_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID: {id} doesn't exist")
    update_data = showtime.model_dump(exclude_unset=True)
    showtime_query.update(update_data, synchronize_session=False)
    db.commit()
    return showtime_query.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_showtime(
    id: int,
    db: Session = Depends(database.get_db),
    current_admin: int = Depends(auth.get_current_admin)
):
    showtime = db.query(models.Showtime).filter(models.Showtime.id == id)
    if showtime is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Showtime with ID: {id} doesn't exist")
    showtime.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)