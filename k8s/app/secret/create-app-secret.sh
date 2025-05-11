#!/bin/bash

file_path=".env"

if [[ ! -f "$file_path" ]]; then
  echo "Error: File '$file_path' does not exist. Please create it like '.env.test'."
  exit 1
fi

set -a
source .env
set +a

kubectl create secret generic airlines-backend-env \
  --from-literal=DB__PASS=$DB__PASS \
  --from-literal=DB__PORT=$DB__PORT \
  --from-literal=DB__USER=$DB__USER \
  --from-literal=DB__NAME=$DB__NAME \
  --from-literal=DB__HOST=$DB__HOST \
  --from-literal=LOG_LEVEL=$LOG_LEVEL \
  --from-literal=JWT_SECRET=$JWT_SECRET

echo "Secret 'airlines-backend-env' created successfully."
