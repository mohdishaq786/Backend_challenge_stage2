set -m
# Start FastAPI application in the background
python3 main.py &
# Start Huey consumer and keep it in the foreground
huey_consumer tasks.huey
fg %1