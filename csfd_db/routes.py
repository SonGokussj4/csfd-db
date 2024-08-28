from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from csfd_db import auth, models, schemas, security
from csfd_db.db import get_db

router = APIRouter(
    tags=["authentication"],
    prefix="/auth",
)


@router.post("/register/", response_model=schemas.UserCreateDBBase)
async def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await auth.get_user(db, username=user_in.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(**user_in.model_dump(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/token/", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # user = await auth.authenticate_user(db, form_data.username, form_data.password)
    # if not user:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Get user from database and check password hash match
    user = await auth.get_user(db, form_data.username)
    if not user or not security.pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Create access token with user's username as subject and expiration time set to X minutes
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
