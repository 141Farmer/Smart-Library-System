#!/usr/bin/env fish

# Check if the virtual environment exists
if not test -d uservenv
    python -m venv uservenv
end

# Activate the virtual environment
source uservenv/bin/activate.fish

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the application
uvicorn main:app --host 127.0.0.1 --port 8001 --reload