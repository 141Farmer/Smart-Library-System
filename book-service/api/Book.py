from fastapi import APIRouter
from core.Book import Book
from schemas.Book import AddBookAction, DetailedBookResponse, UpdateBookAction

router=APIRouter(prefix='',tags=['Book'])

book=Book()

@router.post("/books/")
def add(bookInfo: AddBookAction):
    return book.add(bookInfo)

@router.get("/books/{id}", response_model=DetailedBookResponse)
def getBook(id):
    return book.getBook(id)

@router.put("/books/{id}", response_model=DetailedBookResponse)
def update(id, updateInfo: UpdateBookAction):
    return book.update(id, updateInfo)

@router.delete("/deletebook/{id}")
def delete(id):
    return book.delete(id)