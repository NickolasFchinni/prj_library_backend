from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, database, schemas

router = APIRouter()

@router.post("/{user_id}/{book_id}", response_model=schemas.FavoriteOut)
def favorite_book(user_id: int, book_id: int, db: Session = Depends(database.get_db)):
    try:
        return crud.add_favorite(db, user_id, book_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{user_id}", response_model=list[schemas.FavoriteWithBook])
def get_favorites(user_id: int, db: Session = Depends(database.get_db)):
    favorites = crud.get_favorites_by_user(db, user_id)

    if not favorites:
        return ["Teste"]

    return [
        {
            "id": fav.id,
            "user_id": fav.user_id,
            "book_id": fav.book_id,
            "book": {
                "id": fav.book.id,
                "title": fav.book.title,
                "author": fav.book.author,
            }
        }
        for fav in favorites
    ]

@router.delete("/{user_id}/{book_id}")
def unfavorite_book(user_id: int, book_id: int, db: Session = Depends(database.get_db)):
    favorite = crud.get_favorite(db, user_id, book_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")
    crud.unfavorite_book(db, user_id, book_id)
    return {"detail": "Favorito removido com sucesso"}
