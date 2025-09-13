#!/bin/bash
set -e
echo "🚀 Deploying Ima automatically..."

source .env

docker stop ima || true
docker rm ima || true
docker build -t ima-app .
docker run -d --name ima -p 8080:8080 --env-file .env ima-app

echo "✅ Ima API live at http://localhost:8080"
