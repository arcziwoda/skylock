#!/bin/sh

alembic upgrade head

uvicorn skylock.app:app --host 0.0.0.0 --reload
