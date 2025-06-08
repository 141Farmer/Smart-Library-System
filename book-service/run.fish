#!/usr/bin/env fish

if not test -d bookvenv
    python -m venv bookvenv
end

. bookvenv/bin/activate.fish

./bookvenv/bin/python -m  pip install --upgrade pip
./bookvenv/bin/python -m pip install -r requirements.txt

./bookvenv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8002 --reload