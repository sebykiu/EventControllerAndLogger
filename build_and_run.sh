#!/bin/sh

docker compose down

docker build -t ecal_image .

docker compose up
