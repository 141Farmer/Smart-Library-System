#!/usr/bin/env fish

# Check if the virtual environment exists
if not test -d loanvenv
    python -m venv loanvenv
end

# Activate the virtual environment
. loanvenv/bin/activate.fish
# Install dependencies
#./loanvenv/bin/python -m pip install --upgrade pip
#./loanvenv/bin/python -m pip install -r requirements.txt

# Run the application
./loanvenv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8003 --reload