#!/bin/bash
source /home/ubuntu/venv/bin/activate

export $(cat /home/ubuntu/TC-Editor-Backend/backend/.env.production | xargs)

exec /home/ubuntu/venv/bin/gunicorn app:app --bind 0.0.0.0:8000 --workers 3
