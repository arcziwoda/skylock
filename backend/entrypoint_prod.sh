#!/bin/sh

DATA_DIR="data"
if [ ! -d "$DATA_DIR" ]; then
    mkdir "$DATA_DIR"
fi

alembic upgrade head

exec gunicorn skylock.app:app \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 2 \
    --timeout 120 \
    --log-level info \
    --worker-class uvicorn.workers.UvicornWorker
