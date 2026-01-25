#!/bin/bash

CONTAINER_NAME="oracle-xe"

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "🛑 Stopping Oracle XE..."
  docker stop ${CONTAINER_NAME}
  echo "✅ Oracle XE stopped"
else
  echo "ℹ️ Oracle XE is not running"
fi
