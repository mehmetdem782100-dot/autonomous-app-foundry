#!/bin/bash

# 1. Veritabanı göçlerini uygula
python -m alembic upgrade head

# 2. Worker/Bot işlemini arka planda başlat
python -u worker.py &

# 3. Ana Web uygulamasını başlat
uvicorn api.main:app --host 0.0.0.0 --port $PORT
