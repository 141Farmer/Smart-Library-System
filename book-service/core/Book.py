from fastapi import HTTPException
from schemas.Book import AddBookAction, BookResponse, DetailedBookResponse, BookAvailabiltyResponse, AvailableCopyAction
from models.Book import Book as BookTable
from database.Session import session_instance
from typing import List

class Book:

    def add(self, bookInfo: AddBookAction) -> BookResponse:
        book=BookTable(title=bookInfo.title,
                        author=bookInfo.author,
                        isbn=bookInfo.isbn,
                        copies=bookInfo.copies
                    )
        session_instance.write(book)
        if book is not None:
            return BookResponse(
                id=book.id,
                title=book.title,
                author=book.author,
                isbn=book.isbn,
                copies=book.copies,
                available_copies=book.available_copies,
                created_at=book.created_at
            )

        raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_book(self, id) -> DetailedBookResponse:
        book=session_instance.read_one(BookTable,id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return DetailedBookResponse(
            id=book.id,
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            copies=book.copies,
            available_copies=book.available_copies,
            created_at=book.created_at,
            updated_at=book.updated_at
        )

    def update_book(self, id, update_info) -> DetailedBookResponse:
        book=session_instance.read_one(BookTable,id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        updated_book=session_instance.update(BookTable, id, update_info)
        return DetailedBookResponse(
            id=updated_book.id,
            title=updated_book.title,
            author=updated_book.author,
            isbn=updated_book.isbn,
            copies=updated_book.copies,
            available_copies=updated_book.available_copies,
            created_at=updated_book.created_at,
            updated_at=updated_book.updated_at
        )
    
    def delete(self, id) :
        if session_instance.delete(BookTable, id):
            return {"message": "204  no  content"}
        
        return {"message": "Book not found"}

    def book_availability(self, id, availability_info):
        book=session_instance.read_one(BookTable,id)
        if availability_info.operation == 'decrement' and book.available_copies<=0:
            raise HTTPException(status_code=404, detail="Book not available")

        change=availability_info.available_copies if availability_info.operation == 'increment' else -availability_info.available_copies
        
        available_copy_action=AvailableCopyAction(
            available_copies=change
        )

        updated_book=session_instance.update(BookTable, id, available_copy_action)
        
        return BookAvailabiltyResponse(
            id=updated_book.id,
            available_copies=updated_book.available_copies,
            updated_at=updated_book.updated_at
        )