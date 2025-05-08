#!/bin/bash

set -e
set -x

if [ "$DB__HOST" != "localhost" ] && [ "$DB__HOST" != "127.0.0.1" ]; then
    echo "DB__HOST is not set to localhost or 127.0.0.1. Exiting."
    exit 1
fi
