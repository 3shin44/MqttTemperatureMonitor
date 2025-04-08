#!/bin/bash

# Stop and remove publisher
docker compose -f ./publisher/docker-compose.yml down

# Stop and remove subscriber
docker compose -f ./subscriber/docker-compose.yml down
