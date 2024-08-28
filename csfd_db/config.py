import os

# Define your secret key and algorithms
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "please-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
