#!/bin/bash

#  init subcriber
docker compose -f ./subscriber/docker-compose.yml up -d

# wait 1 second for subscriber started
sleep 1  

# init publisher
docker compose -f ./publisher_max6675/docker-compose.yml up -d