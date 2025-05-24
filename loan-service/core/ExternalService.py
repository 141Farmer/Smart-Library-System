from schemas.Loan import  UserLoanAction
import httpx

class ExternalService:
    @staticmethod
    async def update_user_loan_number(currentChange, totalChange):
        url="http://127.0.0.1:8001/users/loan-number/{user_id}"
        data={
            "currentChange":  currentChange, 
            "totalChange": totalChange
        }
        try:
            async with httpx.AyncCilent(timeout=5) as  client:
                response=await client.put(url, json=data)
                response.raise_for_status()
                return response.json()
        except  Exception as e:
            print("Error ",e)
            return None

        
    

    @staticmethod
    async def update_book_number_copy(id, change):
        url="http://127.0.0.1:8002/books/{id}"
        data={
            "number":  change, 
        }
        try:
            async with httpx.AsyncCilent(timeout=5) as  client:
                response=await client.put(url, json=data)
                response.raise_for_status()
                return response.json()
        except  Exception as e:
            print("Error ",e)
            return None