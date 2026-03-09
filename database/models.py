from database.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, UniqueConstraint, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default='user')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    reports = relationship("Report", back_populates="users")
    reservations = relationship("Reservation", back_populates="users")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    release_date = Column(TIMESTAMP(timezone=True), nullable=False)
    rating = Column(Float)
    poster_image = Column(String, nullable=False)

    showtimes = relationship("Showtime", back_populates="movies")
    movie_genres = relationship("MovieGenre", back_populates="movie")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, nullable=False)
    genre = Column(String, nullable=False, unique=True)

    movie_genres = relationship("MovieGenre", back_populates="genre")

class MovieGenre(Base):
    __tablename__ = "movie_genres"

    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)

    movie = relationship("Movie", back_populates="movie_genres")
    genre = relationship("Genre", back_populates="movie_genres")

class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(Integer, primary_key=True, nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
    showtime = Column(TIMESTAMP(timezone=True), nullable=False)
    screen_id = Column(Integer, ForeignKey("screens.id", ondelete="CASCADE"))

    movies = relationship("Movie", back_populates="showtimes")
    reservations = relationship("Reservation", back_populates="showtimes")
    screens = relationship("Screen", back_populates="showtimes")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    reservation_id = Column(Integer, ForeignKey("reservations.id", ondelete="CASCADE"))
    report = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    users = relationship("User", back_populates="reports")
    reservations = relationship("Reservation", back_populates="reports")

class Screen(Base):
    __tablename__ = "screens"

    id = Column(Integer, primary_key=True, nullable=False)
    total_rows = Column(Integer, nullable=False)
    total_columns = Column(Integer, nullable=False)

    showtimes = relationship("Showtime", back_populates="screens")
    seats = relationship("Seat", back_populates="screens")

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, nullable=False)
    row = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    screen_id = Column(Integer, ForeignKey("screens.id", ondelete="CASCADE"))
    seat_type = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    reservations = relationship("Reservation", back_populates="seats")
    screens = relationship("Screen", back_populates="seats")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    showtime_id = Column(Integer, ForeignKey("showtimes.id", ondelete="CASCADE"))
    seat_id = Column(Integer, ForeignKey("seats.id", ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint("showtime_id", "seat_id", name="unique_showtime_seat"),)

    users = relationship("User", back_populates="reservations")
    showtimes = relationship("Showtime", back_populates="reservations")
    seats = relationship("Seat", back_populates="reservations")
    reports = relationship("Report", back_populates="reservations")