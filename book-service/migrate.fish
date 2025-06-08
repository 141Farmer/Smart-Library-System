#!/usr/bin/env fish

. bookvenv/bin/activate.fish


./bookvenv/bin/python -m  alembic  revision  --autogenerate

./bookvenv/bin/python -m  alembic  upgrade  head