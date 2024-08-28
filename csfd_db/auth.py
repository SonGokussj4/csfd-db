import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from csfd_db import models, schemas, security
from csfd_db.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_user(db: Session, username: str) -> models.User | None:
    """Get user from database by username"""
    # TODO: This is not async
    return db.query(models.User).filter(models.User.username == username).first()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> models.User:
    # Exception when token is invalid
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.JWT_SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)

    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except Exception:
        raise credentials_exception

    # Get user from database
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user
