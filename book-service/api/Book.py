from fastapi import APIRouter
from core.Book import Book
from schemas.Book import AddBookAction, DetailedBookResponse, BookResponse, UpdateBookAction, BookAvailabiltyAction, BookAvailabiltyResponse

router=APIRouter(prefix='/api',tags=['Book'])

book=Book()

@router.post("/books/", response_model=BookResponse)
def add(book_info: AddBookAction):
    return book.add(book_info)

@router.get("/books/{id}", response_model=DetailedBookResponse)
def get_book(id):
    return book.get_book(id)

@router.put("/books/{id}", response_model=DetailedBookResponse)
def update_book(id, update_info: UpdateBookAction):
    return book.update_book(id, update_info)


@router.patch("/books/{id}/availability", response_model=BookAvailabiltyResponse)
def book_availability(id, availability_info: BookAvailabiltyAction):
    return book.book_availability(id, availability_info)

@router.delete("/deletebook/{id}")
def delete(id):
    return book.delete(id)