#!/usr/bin/env fish

# Check if the virtual environment exists
if not test -d loanvenv
    python -m venv loanvenv
end

# Activate the virtual environment
source loanvenv/bin/activate.fish

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the application
uvicorn main:app --host 127.0.0.1 --port 8003 --reload