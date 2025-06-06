from fastapi import FastAPI
from api.Book import router as book_router
from database.Session import session_instance
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],  #origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_instance.create_tables()

app.include_router(book_router)

@app.get("/")
async def root():
    return {"message": "Book service running at port 8002!"}