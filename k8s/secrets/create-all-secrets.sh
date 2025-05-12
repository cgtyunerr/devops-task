#!/bin/bash

base_dir=$(dirname "$(realpath "$0")")

for dir in "$base_dir"/*/; do
  if [[ -f "$dir/create.sh" ]]; then
    echo "Running create.sh in directory: $dir"
    (cd "$dir" && ./create.sh)
  fi
done