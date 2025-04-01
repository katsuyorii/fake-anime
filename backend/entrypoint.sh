#!/bin/bash

poetry run alembic revision --autogenerate -m "Initial migrations"
poetry run alembic upgrade head
poetry run uvicorn main:app --host 0.0.0.0 --port 8000