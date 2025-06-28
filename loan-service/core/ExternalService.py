from schemas.Loan import MiniBookResponse, MiniUserResponse, BookAvailabiltyAction
import httpx
from datetime import datetime, timedelta
from fastapi import HTTPException
import logging
from typing import Union, Optional

logger = logging.getLogger(__name__)

class CircuitBreaker:
    def __init__(self, max_failures=3, reset_timeout=30):
        self.max_failures = max_failures
        self.reset_timeout = timedelta(seconds=reset_timeout)
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def check_state(self):
        if self.is_open:
            if datetime.now() - self.last_failure_time > self.reset_timeout:
                self.is_open = False 
                logger.info("Circuit breaker: Attempting recovery")
                return False
            return True  
        return False  

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.max_failures:
            self.is_open = True
            logger.error(f"Circuit breaker: Tripped! Service unavailable")

    def record_success(self):
        self.failure_count = 0
        self.is_open = False

class ExternalService:
    _user_circuit = CircuitBreaker()
    _book_circuit = CircuitBreaker()

    @staticmethod
    async def _make_request(url: str, method: str = "GET", json_data: Optional[dict] = None) -> Union[dict, bool, None]:
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
                if method.upper() == "GET":
                    response = await client.get(url)
                elif method.upper() == "PUT":
                    response = await client.put(url, json=json_data)
                elif method.upper() == "PATCH":
                    response = await client.patch(url, json=json_data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                
                if response.status_code == 404:
                    return False  
                
                response.raise_for_status()
                return response.json() or True 

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} from {url}: {str(e)}")
            return None
        except httpx.RequestError as e:
            logger.error(f"Request failed to {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error with {url}: {str(e)}")
            raise  

    @staticmethod
    async def check_user(user_id):

        if ExternalService._user_circuit.check_state():
            logger.warning("User service circuit breaker open - skipping request")
            return None

        url = f"http://127.0.0.1:8001/api/users/{user_id}"
        try:
            result = await ExternalService._make_request(url)
            if result is None:
                return False
            ExternalService._user_circuit.record_success()
            return bool(result)
        except Exception:
            ExternalService._user_circuit.record_failure()
            return None

    @staticmethod
    async def check_book(book_id):
        if ExternalService._book_circuit.check_state():
            logger.warning("Book service circuit breaker open - skipping request")
            return None

        url = f"http://127.0.0.1:8002/api/books/{book_id}"
        try:
            result = await ExternalService._make_request(url)
            if result is None:
                return False
            ExternalService._book_circuit.record_success()
            return bool(result)
        except Exception:
            ExternalService._book_circuit.record_failure()
            return None

    @staticmethod
    async def update_book_number_copy(book_id: int, operation: str) -> Union[bool, None]:
        if ExternalService._book_circuit.check_state():
            logger.warning("Book service circuit breaker open - skipping update")
            return None  

        url = f"http://127.0.0.1:8002/api/books/{book_id}/availability"
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                
                check_response = await client.get(f"http://127.0.0.1:8002/api/books/{book_id}")
                if check_response.status_code == 404:
                    return False  

                
                data = {
                    "operation": operation,
                    "available_copies": 1  
                }
                response = await client.patch(url, json=data)  
                
                if response.status_code == 409:
                    return False  
                    
                response.raise_for_status()
                ExternalService._book_circuit.record_success()
                return True  
        except httpx.RequestError as e:
            logger.error(f"Book update failed: {str(e)}")
            ExternalService._book_circuit.record_failure()
            return None  
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            ExternalService._book_circuit.record_failure()
            return None

    @staticmethod
    async def get_mini_user(user_id: int) -> Union[MiniUserResponse, bool, None]:
        url = f"http://127.0.0.1:8001/api/users/{user_id}"
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(url)
                
                if response.status_code == 404:
                    return False  
                    
                response.raise_for_status()
                user = response.json()
                
                return MiniUserResponse(
                    id=user['id'],
                    name=user['name'],
                    email=user['email']
                )
        except httpx.RequestError as e:
            logger.error(f"User service request failed: {str(e)}")
            return None  
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None


    @staticmethod
    async def get_mini_book(book_id: int) -> Union[MiniBookResponse, bool, None]:
        url = f"http://127.0.0.1:8002/api/books/{book_id}"
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(url)
                
                if response.status_code == 404:
                    return False  
                    
                response.raise_for_status()
                book = response.json()
                
                return MiniBookResponse(
                    id=book['id'],
                    title=book['title'],
                    author=book['author']
                )
        except httpx.RequestError as e:
            logger.error(f"Book service request failed: {str(e)}")
            return None  
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None