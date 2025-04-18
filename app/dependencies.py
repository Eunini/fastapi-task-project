# app/dependencies.py

from sqlalchemy.orm import Session
from .database import SessionLocal

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
