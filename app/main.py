from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, books, favorites
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(books.router, prefix="/books")
app.include_router(favorites.router, prefix="/favorites")
