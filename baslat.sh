#!/bin/bash

# 1. Veritabanı göçlerini (migrations) uygula
python -m alembic upgrade head

# 2. Worker/Bot işlemini arka planda başlat
python worker.py &

# 3. Ana Web uygulamasını başlat (Bu işlem ön planda kalmalı)
python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT