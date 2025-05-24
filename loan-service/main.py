from fastapi import FastAPI
from api.Loan import router as loan_router
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

app.include_router(loan_router)

@app.get("/")
async def root():
    return {"message": "Hello, world!"}