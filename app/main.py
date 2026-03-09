from fastapi import FastAPI
from database import models
from database.database import engine
from .routers import users, movies, reservations, seats, screens, showtimes, reports

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(reservations.router)
app.include_router(seats.router)
app.include_router(screens.router)
app.include_router(showtimes.router)
app.include_router(reports.router)

@app.get('/')
def root():
    return {"message": "Hello world!"}