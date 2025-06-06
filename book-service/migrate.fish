#!/usr/bin/env fish

# Check if the virtual environment exists
if not test -d bookvenv
    python -m venv bookvenv
end

# Activate the virtual environment
. bookvenv/bin/activate.fish


./bookvenv/bin/python -m  alembic  revision  --autogenerate

./bookvenv/bin/python -m  alembic  upgrade  head