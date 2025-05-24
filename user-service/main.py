from fastapi import FastAPI
from api.User import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from database.Session import session_instance

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],  #origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_instance.create_tables()

app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Hello, world!"}