#!/usr/bin/env bash
set -e

QDRANT_NAME="qdrant"
QDRANT_PORT="6333"

echo "🔍 Checking Docker..."

if ! docker info >/dev/null 2>&1; then
  echo "🐳 Starting Docker..."
  open -a Docker
  while ! docker info >/dev/null 2>&1; do
    sleep 1
  done
fi

echo "🐳 Docker is running..."

# Is qdrant container already running?
if docker ps --format '{{.Names}}' | grep -q "^${QDRANT_NAME}$"; then
  echo "✅ Qdrant already running..."
  exit 0
fi

# Is qdrant container created but stopped?
if docker ps -a --format '{{.Names}}' | grep -q "^${QDRANT_NAME}$"; then
  echo "▶️ Starting existing Qdrant container..."
  docker start ${QDRANT_NAME}
  exit 0
fi

# Else create it
echo "🚀 Creating Qdrant container..."
docker run -d \
  --name ${QDRANT_NAME} \
  -p 6333:6333 \
  -p 6334:6334 \
  -v "$(pwd)/DO_NOT_COMMIT/qdrant_data:/qdrant/storage" \
  qdrant/qdrant

echo "✅ Qdrant started"
