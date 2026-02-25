from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import database, models
from app import schemas, auth

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(
    create_user_request: schemas.CreateUser, 
    db: Session = Depends(database.get_db)
):
    if db.query(models.User).filter(models.User.email == create_user_request.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email: {create_user_request.email} is already exist")
    
    hashed_password = auth.get_password_hash(create_user_request.password)
    create_user_request.password = hashed_password
    create_user_model = models.User(**create_user_request.model_dump())
    db.add(create_user_model)
    db.commit()
    return create_user_model

@router.post('/login')
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    if not auth.verify_password(user_credentials.password, user.password): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    
    access_token = auth.create_access_token(data = {'user_id': user.id})

    return {'access_token': access_token, "token_type": "bearer"}