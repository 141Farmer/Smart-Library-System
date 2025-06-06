#!/usr/bin/env fish

# Activate the virtual environment
. uservenv/bin/activate.fish


./uservenv/bin/python -m  alembic  revision  --autogenerate

./uservenv/bin/python -m  alembic  upgrade  head