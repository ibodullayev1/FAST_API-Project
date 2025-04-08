from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas, database, auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from jose import JWTError, jwt

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Database sessionni yaratish
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Register
@app.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return db_user


# Login (JWT)
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = auth.get_user_by_email(db, form_data.username)
    if not db_user or not auth.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Book CRUD
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_current_user(db, token)
    return crud.create_book(db=db, book=book, user_id=user.id)


@app.get("/books/", response_model=List[schemas.Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    # Kitobni tekshirish
    book = crud.get_book_or_404(db, book_id)
    return book


# Tokenni tekshirish va foydalanuvchini olish
def get_current_user(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = auth.get_user_by_email(db, email=email)
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user


# Kitobni o'chirish (DELETE)
@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = auth.get_current_user(db, token)
    book = auth.get_book_by_owner(db, book_id, user.id)
    db.delete(book)
    db.commit()
    return book


# Kitobni tahrirlash (PUT)
@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db),
                token: str = Depends(oauth2_scheme)):
    user = auth.get_current_user(db, token)
    existing_book = auth.get_book_by_owner(db, book_id, user.id)

    existing_book.title = book.title
    existing_book.author = book.author
    existing_book.description = book.description

    db.commit()
    db.refresh(existing_book)
    return existing_book



