#!/bin/sh

docker build -t ecal_image .

docker-compose up
