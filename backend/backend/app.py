from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import auth, games, reviews, users

app = FastAPI()

allowed_origins = [
    'http://localhost',
    'http://localhost:3001',
    'http://localhost:5173',
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(games.router)
app.include_router(reviews.router)
