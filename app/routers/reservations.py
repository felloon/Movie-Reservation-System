from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import database, models
from app import schemas, auth

router = APIRouter(
    prefix='/reservation',
    tags=['Reservations']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ReservationOut)
def create_reservation(
    reservation: schemas.CreateReservation,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(auth.get_current_user)
):
    reservation_model = models.Reservation(**reservation.model_dump(), user_id = current_user.id)
    db.add(reservation_model)
    db.commit()
    db.refresh(reservation_model)
    return reservation_model