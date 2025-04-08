from sqlalchemy.orm import Session
from app import models, schemas
from app import auth
from fastapi import HTTPException, status


from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas
from app import auth

def create_user(db: Session, user: schemas.UserCreate):
    db_user_by_username = db.query(models.User).filter(models.User.username == user.username).first()
    db_user_by_email = db.query(models.User).filter(models.User.email == user.email).first()

    if db_user_by_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username allaqachon mavjud")
    if db_user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email alaqachon mavjud")

    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating user: {str(e)}")

    return db_user



def create_book(db: Session, book: schemas.BookCreate, user_id: int):
    db_book = models.Book(**book.dict(), owner_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    return None

def update_book(db: Session, book_id: int, book_data: schemas.BookCreate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db_book.title = book_data.title
        db_book.author = book_data.author
        db_book.description = book_data.description
        db.commit()
        db.refresh(db_book)
        return db_book
    return None



def get_book_or_404(db: Session, book_id: int):
    # Kitobni id orqali qidirish
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Afsuski hozirda bunday kitob mavjud emas ! UZUR !")
    return book
