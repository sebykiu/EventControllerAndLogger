#!/bin/sh

NETWORK_NAME="rovernet"

if docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
  echo "Network '$NETWORK_NAME' already exists."
else
  docker network create "$NETWORK_NAME"
  echo "Network '$NETWORK_NAME' created."
fi

docker compose down

docker build -t ecal_image .

docker compose up
