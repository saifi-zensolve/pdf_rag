#!/usr/bin/env bash
set -e

QDRANT_NAME="qdrant"

if docker ps --format '{{.Names}}' | grep -q "^${QDRANT_NAME}$"; then
  echo "🛑 Stopping Qdrant..."
  docker stop ${QDRANT_NAME}
else
  echo "🛑 Qdrant is not running"
fi
