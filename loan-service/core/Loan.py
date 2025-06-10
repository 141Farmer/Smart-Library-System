from fastapi  import HTTPException,  status
from schemas.Loan import LoanResponse, LoanAction, ReturnAction,  ReturnResponse, UsersLoanHistoryResponse, SpecificLoanResponse, LoanHistoryResponse, ReturnUpdateAction
from models.Loan import Loan as LoanTable
from database.Session import session_instance
from typing import List
from datetime import datetime, timezone, timedelta
from core.ExternalService  import ExternalService
import asyncio

class Loan:

    async def issue_loan(self, loan_info: LoanAction) -> LoanResponse:
        user_exists = await ExternalService.check_user(loan_info.user_id)
        if user_exists is False:  
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        elif user_exists is None:  
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User service unavailable"
            )

        book_exists = await ExternalService.check_book(loan_info.book_id)
        if book_exists is False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        elif book_exists is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Book service unavailable"
            )

        update_success = await ExternalService.update_book_number_copy(loan_info.book_id, 'decrement')
        if update_success is False:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Not enough copies available"
            )
        elif update_success is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Book service unavailable"
            )

        # Only proceed if all checks passed
        loan = LoanTable(
            user_id=loan_info.user_id,
            book_id=loan_info.book_id,
            due_date=loan_info.due_date
        )
        
        session_instance.write(loan)
        
        if not loan:   
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create loan"
            )

        return LoanResponse(
            id=loan.id,
            user_id=loan.user_id,
            book_id=loan.book_id,
            issue_date=loan.issue_date,
            due_date=loan.due_date,
            status=loan.status
        )

    async def returns(self, loan_id: ReturnAction) -> ReturnResponse:
        # Check loan exists
        loan = session_instance.read_one(LoanTable, loan_id.loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )

        # Update loan status
        updates = ReturnUpdateAction(
            status="RETURNED",
            return_date=datetime.now(timezone.utc)
        )
        
        updated_loan = session_instance.update(LoanTable, loan_id.loan_id, updates)
        if not updated_loan:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update loan status"
            )

        # Update book inventory (with proper await)
        update_result = await ExternalService.update_book_number_copy(loan.book_id, 'increment')
        if update_result is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Book service unavailable"
            )
        if update_result is False:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Failed to update book inventory"
            )

        return ReturnResponse(
            id=updated_loan.id,
            user_id=updated_loan.user_id,
            book_id=updated_loan.book_id,
            issue_date=updated_loan.issue_date,
            due_date=updated_loan.due_date,
            return_date=updated_loan.return_date,
            status=updated_loan.status
        )

    async def get_user_loan_history(self, user_id: int) -> UsersLoanHistoryResponse:
    # Check user exists (with await)
        user_exists = await ExternalService.check_user(user_id)
        if user_exists is False:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        elif user_exists is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User service unavailable"
            )

        # Get loans from database
        loans = session_instance.read_filter_all(LoanTable, user_id=user_id)
        total = session_instance.count_filter(LoanTable, user_id=user_id)

        # Process loans with async book info
        loan_responses = []
        for loan in loans:
            book = await ExternalService.get_mini_book(loan.book_id)
            if book is None:  # Service error
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Book service unavailable"
                )
            
            loan_responses.append(
                LoanHistoryResponse(
                    id=loan.id,
                    book=book,
                    issue_date=loan.issue_date,
                    due_date=loan.due_date,
                    return_date=loan.return_date,
                    status=loan.status,
                )
            )

        return UsersLoanHistoryResponse(
            loans=loan_responses,
            total=int(total)
        )

    async def get_specific_loan(self, id: int) -> SpecificLoanResponse:
        loan = session_instance.read_one(LoanTable, id=id)
        
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
        
        # Get user and book info in parallel
        user, book = await asyncio.gather(
            ExternalService.get_mini_user(loan.user_id),
            ExternalService.get_mini_book(loan.book_id)
        )

        # Check for service errors
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User service unavailable"
            )
        if book is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Book service unavailable"
            )

        return SpecificLoanResponse(
            id=loan.id,
            user=user,
            book=book,
            issue_date=loan.issue_date,
            due_date=loan.due_date,
            return_date=loan.return_date,
            status=loan.status
        )