#!/bin/bash

set -e
set -x

if [ "$DB__HOST" != "localhost" ] && [ "$DB__HOST" != "127.0.0.1" ]; then
    echo "DB__HOST is not set to localhost or 127.0.0.1. Exiting."
    exit 1
fi

scripts/migrate.sh app/modules/user/pymigrate users
scripts/migrate.sh app/modules/airline/pymigrate airlines
scripts/migrate.sh app/modules/aircraft/pymigrate aircrafts

poetry run python app/modules/user/tests/setup/manual_setup.py
poetry run python app/modules/airline/tests/setup/manual_setup.py
poetry run python app/modules/aircraft/tests/setup/manual_setup.py
