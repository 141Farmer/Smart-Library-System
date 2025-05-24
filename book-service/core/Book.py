from fastapi import HTTPException
from schemas.Book import AddBookAction, DetailedBookResponse, BookNumberAction, MiniBookResponse
#from schemas.Stats import PopularBookResponse
from models.Book import Book as BookTable
from database.Session import session_instance
from typing import List

class Book:

    def add(self, bookInfo: AddBookAction):
        book=BookTable(title=bookInfo.title,
                        author=bookInfo.author,
                        isbn=bookInfo.isbn,
                        copies=bookInfo.copies
                    )
        session_instance.write(book)
        if book is not None:
            raise HTTPException(status_code=201, detail="Book added successfully")

        raise HTTPException(status_code=500, detail="Internal Server Error")

    def getBook(self, id) -> DetailedBookResponse:
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

    def update(self, id, updateInfo) -> DetailedBookResponse:
        book=session_instance.read_one(BookTable,id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        updatedBook=session_instance.update(BookTable, id, updateInfo)
        return DetailedBookResponse(
            id=book.id,
            title=updatedBook.title,
            author=updatedBook.author,
            isbn=updatedBook.isbn,
            copies=updatedBook.copies,
            available_copies=updatedBook.available_copies,
            created_at=updatedBook.created_at,
            updated_at=updatedBook.updated_at
        )
    
    def delete(self,  id) :
        if session_instance.delete(BookTable, id):
            return {"message": "204  no  content"}
        else:
            return {"message": "Book not found"}

    def updateBookCopy(self, id, change):
        book=session_instance.read_one(BookTable,id)
        bookNumberAction=BookNumberAction(
            available_copies=book.available_copies+change,
            borrow_count=book.borrow_count+1
        )
        session_instance.update(BookTable, id, bookNumberAction)

    def getMiniBook(self, id) -> List[MiniBookResponse]:
        book=session_instance.read_one(BookTable, id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        return MiniBookResponse(
            id=book.id,
            title=book.title,
            author=book.author,
        )

    '''
    def getMiniBooks(self) -> List[PopularBookResponse]:
        books=session_instance.read_all(BookTable)
        miniBooks=[]
        for book  in books:
            miniBooks.append(
                PopularBookResponse(
                    book_id=book.id,
                    title=book.title,
                    author=book.author,
                    borrow_count=book.borrow_count
                )
            )
        return miniBooks
    '''
    def getTotalBooks(self):
        return session_instance.count_all(BookTable)

    def getTotalAvailableBooks(self):
        books=session_instance.read_all(BookTable)
        count=0
        for book in books:
            count+=book.available_copies
        return count

    def getTotalBorrowedBooks(self):
        books=session_instance.read_all(BookTable)
        count=0
        for book in books:
            count+=book.borrow_count
        return count