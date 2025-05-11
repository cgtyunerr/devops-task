#!/bin/bash

file_path=".env.registry"

if [[ ! -f "$file_path" ]]; then
  echo "Error: File '$file_path' does not exist. Please create it like '.env.registry.test'."
  exit 1
fi

set -a
source .env.registry
set +a

kubectl create secret docker-registry regcred \
  --docker-server=$DOCKER_SERVER \
  --docker-username=$DOCKER_USERNAME \
  --docker-password=$DOCKER_PASSWORD \
  --docker-email=$DOCKER_EMAIL
