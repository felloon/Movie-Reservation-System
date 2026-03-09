from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, timezone
from database import database, models
from app import schemas, auth

router = APIRouter(
    prefix='/reservation',
    tags=['Reservations']
)

@router.get('/{showtime_id}/available-seats', response_model=List[schemas.SeatOut])
def get_all_available_seats(
    showtime_id: int,
    db: Session = Depends(database.get_db)
):
    seats = db.query(models.Seat).join(models.Showtime, models.Showtime.screen_id == models.Seat.screen_id) \
        .outerjoin(
            models.Reservation, 
            and_(models.Reservation.seat_id == models.Seat.id, models.Reservation.showtime_id == showtime_id)) \
                .filter(models.Showtime.id == showtime_id).filter(models.Reservation.id == None)
    return seats.all()

@router.get('/', response_model=List[schemas.ReservationShowtimesOut])
def get_all_user_reservations(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(auth.get_current_user)
):
    reservations = db.query(models.Reservation).join(models.Showtime, models.Showtime.id == models.Reservation.showtime_id) \
        .filter(models.Reservation.user_id == current_user.id)
    return reservations.all()

@router.get('/admin/all', response_model=List[schemas.ReservationShowtimesOutAdmin])
def get_all_reservations(
    db: Session = Depends(database.get_db),
    current_admin: int = Depends(auth.get_current_admin)
):
    reservations = db.query(models.Reservation).join(models.Showtime, models.Showtime.id == models.Reservation.showtime_id)
    return reservations.all()

@router.get('/admin/capacity')
def get_all_reservations_capacity(
    db: Session = Depends(database.get_db),
    current_admin: int = Depends(auth.get_current_admin)
):
    count = db.query(func.count(models.Reservation.seat_id)).scalar()
    return {'total_reservations': count}

@router.get('/admin/revenue')
def get_all_reservations_revenue(
    db: Session = Depends(database.get_db),
    current_admin: int = Depends(auth.get_current_admin)
):
    count = db.query(func.coalesce(func.sum(models.Seat.price), 0)).select_from(models.Reservation).join(models.Seat).scalar()
    return {'total_revenue': count}

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

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def cancel_reservation(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(auth.get_current_user)
):
    reservation = db.query(models.Reservation).join(models.Showtime, models.Showtime.id == models.Reservation.showtime_id) \
        .filter(models.Reservation.id == id)
    if not reservation.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reservation with ID: {id} doesn't exist")
    if reservation.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this action")
    if datetime.now(timezone.utc) > reservation.first().showtimes.showtime:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot cancel past or ongoing reservations")
    reservation_delete = db.query(models.Reservation).filter(models.Reservation.id == id)
    reservation_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)