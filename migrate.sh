#!/usr/bin/env sh

export PYTHONPATH=.

alembic revision --autogenerate -m "db changes"