#!/bin/bash

set -e
set -x

if [ "$DB__HOST" != "localhost" ] && [ "$DB__HOST" != "127.0.0.1" ]; then
    echo "DB__HOST is not set to localhost or 127.0.0.1. Exiting."
    exit 1
fi

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path-module>"
    exit 1
fi

module="$1"

poetry run python -m coverage run --source=$module -m pytest -lv $module
poetry run python -m coverage report -m --omit="*/setup/*" --omit="*/tests/*"
