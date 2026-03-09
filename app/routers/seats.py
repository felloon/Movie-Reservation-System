from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import Optional, List
from database import database, models
from app import schemas, auth

router = APIRouter(
    prefix='/seat',
    tags=['Seats']
)

@router.get('/', response_model=List[schemas.SeatOut])
def get_all_seats(
    db: Session = Depends(database.get_db),
    limit: int = 100, 
):
    seats = db.query(models.Seat).limit(limit).all()
    return seats

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_seat(
    seat: schemas.CreateSeat,
    db: Session = Depends(database.get_db),
    current_admin: int = Depends(auth.get_current_admin)
):
    if not db.query(models.Screen).filter(models.Screen.id == seat.screen_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Screen with ID: {seat.screen_id} doesn't exist")
    seat_model = models.Seat(**seat.model_dump())
    db.add(seat_model)
    db.commit()
    db.refresh(seat_model)
    return seat_model

@router.patch('/{id}')
def update_seat(
    id: int,
    seat: schemas.UpdateSeat,
    db: Session = Depends(database.get_db),
    current_admin: int = Depends(auth.get_current_admin)
):
    seat_query = db.query(models.Seat).filter(models.Seat.id == id)
    if not seat_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID: {id} doesn't exist")
    update_data = seat.model_dump(exclude_unset=True)
    seat_query.update(update_data, synchronize_session=False)
    db.commit()
    return seat_query.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_seat(
    id: int,
    db: Session = Depends(database.get_db),
    current_admin: int = Depends(auth.get_current_admin)
):
    seat = db.query(models.Seat).filter(models.Seat.id == id)
    if seat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Showtime with ID: {id} doesn't exist")
    seat.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)