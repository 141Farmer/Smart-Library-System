@echo off
echo Activating virtual environment...
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
call .\microvenv\Scripts\activate 

echo Installing dependencies...
pip install -r requirements.txt