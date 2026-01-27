#!/bin/bash

CONTAINER_NAME="oracle-xe"
IMAGE="gvenzl/oracle-xe:21-slim"

if [ -z "$ORACLE_PASSWORD" ]; then
  echo "❌ ORACLE_PASSWORD is not set"
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "🐳 Starting Docker..."
  open -a Docker
  while ! docker info >/dev/null 2>&1; do
    sleep 1
  done
fi

echo "🐳 Docker is running..."

# Check if container is already running
if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "✅ Oracle XE already running"
  exit 0
fi

# Check if container exists but stopped
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "🔄 Starting existing Oracle XE container..."
  docker start ${CONTAINER_NAME}
  exit 0
fi

echo "🚀 Starting Oracle XE container..."

docker pull ${IMAGE}

docker run -d \
  --name ${CONTAINER_NAME} \
  -p 1521:1521 \
  -p 5500:5500 \
  -e ORACLE_PASSWORD="${ORACLE_PASSWORD}" \
  -v oracle_data:/opt/oracle/oradata \
  ${IMAGE}

echo "⏳ Waiting for Oracle to be ready..."
docker logs -f ${CONTAINER_NAME} | grep -m 1 "DATABASE IS READY TO USE!"

echo "✅ Oracle XE is ready"
