#!/bin/bash

file_path=".env.db"

if [[ ! -f "$file_path" ]]; then
  echo "Error: File '$file_path' does not exist. Please create it like '.env.db.test'."
  exit 1
fi

set -a
source .env.db
set +a

kubectl create secret generic db-pass \
  --from-literal=password=$POSTGRES_PASSWORD

echo "Secret 'db-credentials' created successfully."
