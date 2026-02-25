from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None

class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

class CreateMovie(BaseModel):
    title: str
    description: str
    release_date: datetime
    rating: float
    poster_image: HttpUrl

class UpdateMovie(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    poster_image: Optional[HttpUrl] = None
    genre: Optional[str] = None
    showtime_date: Optional[datetime] = None

class MovieOut(CreateMovie):
    id: int

class CreateGenre(BaseModel):
    genre: str

class SetGenre(BaseModel):
    movie_id: int
    genre_id: int

class CreateReservation(BaseModel):
    movie_id: int
    seat_id: int
    schedule_showtime: datetime

class ReservationOut(CreateReservation):
    id: int