from fastapi import APIRouter
from core.Loan import Loan
from schemas.Loan import LoanAction, LoanResponse, ReturnResponse,  LoanIdAction, LoanOfUserResponse, ExtendedLoanResponse, ExtendLoanAction, OverdueResponse
from typing import List

router=APIRouter(prefix='',tags=['Loan'])

loan=Loan()

@router.post("/loans/", response_model=LoanResponse)
def issueloan(loanInfo: LoanAction):
    return loan.issueloan(loanInfo)

@router.post("/returns/", response_model=ReturnResponse)
def returns(loanId: LoanIdAction):
    return loan.returns(loanId)

@router.get("/loans/{user_id}", response_model=List[LoanOfUserResponse])
def getLoansUser(user_id):
    return loan.getLoansUser(user_id)

@router.get("/loans/overdue/", response_model=List[OverdueResponse])
def getAllOverdueLoans():
    return loan.getAllOverdueLoans()

@router.put("/loans/{id}/extend",  response_model=ExtendedLoanResponse)
def extendUserLoan(loan_id, extendInfo: ExtendLoanAction):
    return loan.extendUserLoan(loan_id, extendInfo)