from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from .security import hash_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),  # Aqui você deve fazer a criptografia da senha
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed):
    return pwd_context.verify(plain_password, hashed)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.name == username).first()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def list_books(db: Session):
    return db.query(models.Book).all()

def add_favorite(db: Session, user_id: int, book_id: int):
    existing_favorite = get_favorite(db, user_id, book_id)
    if existing_favorite:
        raise ValueError("Livro já favoritado")
    fav = models.Favorite(user_id=user_id, book_id=book_id)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav

def get_favorite(db: Session, user_id: int, book_id: int):
    return db.query(models.Favorite).filter(
        models.Favorite.user_id == user_id,
        models.Favorite.book_id == book_id
    ).first()

def get_favorites_by_user(db: Session, user_id: int):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()
