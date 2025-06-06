#!/usr/bin/env fish

# Check if the virtual environment exists
if not test -d bookvenv
    python -m venv bookvenv
end

# Activate the virtual environment
. bookvenv/bin/activate.fish

# Install dependencies
./bookvenv/bin/python -m  pip install --upgrade pip
./bookvenv/bin/python -m pip install -r requirements.txt

# Run the application
./bookvenv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8002 --reload