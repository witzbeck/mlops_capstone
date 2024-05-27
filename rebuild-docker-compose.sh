#!/bin/bash
# Build and log script for Docker Compose

# Create a log file with a timestamp
TIMESTAMP=$(date +%Y-%m-%d_%H:%M:%S)
LOG_FILE="logs/build_log_latest.txt"

docker-compose down --rmi all

echo "Starting build at $TIMESTAMP" >"$LOG_FILE"
docker-compose up --build --remove-orphans >>"$LOG_FILE" 2>&1
echo "Build completed at $(date)" >>"$LOG_FILE"
