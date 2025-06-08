from fastapi import APIRouter
from core.Loan import Loan
from schemas.Loan import LoanAction, LoanResponse, ReturnResponse,  LoanIdAction, UsersLoanHistoryResponse, SpecificLoanResponse
from typing import List

router=APIRouter(prefix='',tags=['Loan'])

loan=Loan()

@router.post("/loans/", response_model=LoanResponse)
def issue_loan(loan_info: LoanAction):
    return loan.issue_loan(loan_info)

@router.post("/returns/", response_model=ReturnResponse)
def returns(loan_id: LoanIdAction):
    return loan.returns(loan_id)

@router.get("/loans/user/{user_id}", response_model=UsersLoanHistoryResponse)
def get_user_loan_history(user_id):
    return loan.get_user_loan_history(user_id)

@router.get("/loans/{id}", response_model=SpecificLoanResponse)
def get_specific_loan(id):
    return loan.get_specific_loan(id)