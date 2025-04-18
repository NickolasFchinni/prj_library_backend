from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter()

@router.post("/", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    return crud.create_book(db, book)

@router.get("/", response_model=list[schemas.BookOut])
def get_books(db: Session = Depends(database.get_db)):
    return crud.list_books(db)

@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(database.get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return crud.update_book(db, book_id, book)

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    crud.delete_book(db, book_id)
    return {"detail": "Livro deletado com sucesso"}
