#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <arg1> <arg2>"
    exit 1
fi

script_dir=$(dirname "$0")
path="$1"
schema="$2"

poetry run python $script_dir/python-scripts/migration.py $path $schema
