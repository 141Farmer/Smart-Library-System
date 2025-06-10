from fastapi import APIRouter
from core.Loan import Loan
from core.ExternalService import ExternalService
from schemas.Loan import LoanAction, LoanResponse, ReturnResponse,  ReturnAction, UsersLoanHistoryResponse, SpecificLoanResponse, MiniUserResponse, MiniBookResponse
from typing import List

router=APIRouter(prefix='',tags=['Loan'])

loan=Loan()

@router.post("/loans/", response_model=LoanResponse)
async def issue_loan(loan_info: LoanAction):
    return await loan.issue_loan(loan_info)

@router.post("/returns/", response_model=ReturnResponse)
async def returns(loan_id: ReturnAction):
    return await loan.returns(loan_id)

@router.get("/loans/user/{user_id}", response_model=UsersLoanHistoryResponse)
async def get_user_loan_history(user_id):
    return await loan.get_user_loan_history(user_id)

@router.get("/loans/{id}", response_model=SpecificLoanResponse)
async def get_specific_loan(id):
    return await loan.get_specific_loan(id)
