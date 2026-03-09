from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from datetime import datetime
from database import database, models
from app import schemas, auth

router = APIRouter(
    prefix='/movie',
    tags=['Movies']
)

@router.get('/', response_model=List[schemas.MovieOut])
def get_all_movies(
    db: Session = Depends(database.get_db),
    limit: int = 100,
    search: Optional[str] = "",
    genre: Optional[str] = None,
    showtime: Optional[datetime] = None
):
    movies = db.query(models.Movie).options(
        joinedload(models.Movie.showtimes), 
        joinedload(models.Movie.movie_genres).joinedload(models.MovieGenre.genre)
    ).group_by(models.Movie.id).filter(models.Movie.title.contains(search)).filter(models.Genre.genre.contains(genre))
    if showtime: 
        movies = movies.filter(models.Showtime.showtime == showtime)
    if genre: 
        movies = movies.join(models.Movie.movie_genres).join(models.MovieGenre.genre).filter(models.Genre.genre.ilike(f"%{genre}%"))
    return movies.all()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.MovieOut)
def create_movie(
    movie: schemas.CreateMovie, 
    db: Session = Depends(database.get_db), 
    current_admin: int = Depends(auth.get_current_admin)
):
    poster_image = str(movie.poster_image)
    movie.poster_image = poster_image
    movie_model = models.Movie(**movie.model_dump())
    db.add(movie_model)
    db.commit()
    db.refresh(movie_model)
    return movie_model

@router.patch('/{id}')
def update_movie(
    id: int, 
    movie: schemas.UpdateMovie, 
    db: Session = Depends(database.get_db), 
    current_admin: int = Depends(auth.get_current_admin)
):
    movie_query = db.query(models.Movie).filter(models.Movie.id == id)
    if not movie_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID: {id} doesn't exist")
    update_data = movie.model_dump(exclude_unset=True)
    movie_query.update(update_data, synchronize_session=False)
    db.commit()
    return movie_query.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    id: int, 
    db: Session = Depends(database.get_db), 
    current_admin: int = Depends(auth.get_current_admin)
):
    movie = db.query(models.Movie).filter(models.Movie.id == id)
    if not movie.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID: {id} doesn't exist")
    movie.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post('/genre', status_code=status.HTTP_201_CREATED)
def create_genre(
    genre: schemas.CreateGenre, 
    db: Session = Depends(database.get_db),
    current_admin: int = Depends(auth.get_current_admin)
):
    create_genre = models.Genre(**genre.model_dump())
    db.add(create_genre)
    db.commit()
    db.refresh(create_genre)
    return create_genre

@router.post('/set_genre', status_code=status.HTTP_201_CREATED)
def set_genre_to_movie(
    genre_movie: schemas.SetGenre,
    db: Session = Depends(database.get_db),
    current_admin: int = Depends(auth.get_current_admin)
):
    if not db.query(models.Movie).filter(models.Movie.id == genre_movie.movie_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with ID: {genre_movie.movie_id} doesn't exist")
    if not db.query(models.Genre).filter(models.Genre.id == genre_movie.genre_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Genre with ID: {genre_movie.genre_id} doesn't exist")
    set_genre_movie = models.MovieGenre(**genre_movie.model_dump())
    db.add(set_genre_movie)
    db.commit()
    db.refresh(set_genre_movie)
    return set_genre_movie