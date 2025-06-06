#!/usr/bin/env fish

if not test -d uservenv
    python -m venv uservenv
end

. uservenv/bin/activate.fish

./uservenv/bin/python -m pip install --upgrade pip
./uservenv/bin/python -m pip install -r requirements.txt

./uservenv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload