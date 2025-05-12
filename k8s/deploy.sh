#!/bin/bash

VERSION=$1

base_dir=$(dirname "$(realpath "$0")")

if [ -z "$VERSION" ]; then
  echo "Error: VERSION parameter is required for app."
  exit 1
fi

(cd "$base_dir/secrets" && ./create-all-secrets.sh)
(cd "$base_dir/database" && ./up-db.sh)
(cd "$base_dir/app" && ./up-app.sh $VERSION)
