from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime
from typing import Optional, List

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

class CreateGenre(BaseModel):
    genre: str

class SetGenre(BaseModel):
    movie_id: int
    genre_id: int

class GenreOut(BaseModel):
    id: int
    genre: str

class MovieGenreOut(BaseModel):
    genre: GenreOut

class CreateScreen(BaseModel):
    total_rows: int
    total_columns: int

class ScreenOut(CreateScreen):
    id: int

class UpdateScreen(BaseModel):
    total_rows: Optional[int] = None
    total_columns: Optional[int] = None

class CreateSeat(BaseModel):
    row: int
    number: int
    screen_id: int
    seat_type: str
    price: int

class SeatOut(CreateSeat):
    id: int

class UpdateSeat(BaseModel):
    row: Optional[int] = None
    number: Optional[int] = None
    screen_id: Optional[int] = None
    seat_type: Optional[str] = None
    price: Optional[int] = None
    available: Optional[bool] = None

class CreateShowtime(BaseModel):
    movie_id: int
    showtime: datetime
    screen_id: int

class ShowtimeOut(BaseModel):
    showtime: datetime
    screen_id: int

    class Config:
        from_attributes = True

class MovieOut(BaseModel):
    id: int
    title: str
    description: str
    release_date: datetime
    rating: float | None
    poster_image: str
    showtimes: List[ShowtimeOut]
    movie_genres: List[MovieGenreOut]

    class Config:
        from_attributes = True

class UpdateShowtime(BaseModel):
    movie_id: Optional[int] = None
    showtime: Optional[datetime] = None
    screen_id: Optional[int] = None

class CreateReservation(BaseModel):
    showtime_id: int
    seat_id: int

class ReservationOut(CreateReservation):
    id: int
    user_id: int

class ReservationShowtimesOut(BaseModel):
    id: int
    seat_id: int
    showtimes: ShowtimeOut

class ReservationShowtimesOutAdmin(BaseModel):
    id: int
    user_id: int
    seat_id: int
    showtime_id: int
    showtimes: ShowtimeOut

class CreateReport(BaseModel):
    reservation_id: int
    report: str

class ReportOut(BaseModel):
    id: int
    user_id: int
    reservation_id: int
    report: str
    created_at: datetime
    updated_at: datetime

class UpdateReport(BaseModel):
    reservation_id: Optional[int] = None
    report: Optional[str] = None