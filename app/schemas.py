from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    author: str

class BookUpdate(BaseModel):
    title: str
    author: str

class BookOut(BaseModel):
    id: int
    title: str
    author: str

    class Config:
        orm_mode = True

class FavoriteWithBook(BaseModel):
    id: int
    user_id: int
    book_id: int
    book: BookOut  # <- Aqui entra o livro embutido

    class Config:
        orm_mode = True

class FavoriteOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    class Config:
        orm_mode = True
