#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path> <name>"
    exit 1
fi

path=$1
name=$2

current_date=$(date +"%Y%m%d%H%M%S")

sql_file="$path/$current_date-$name.sql"

touch "$sql_file"

echo "/* Replace with your SQL commands */" >> "$sql_file"

echo "SQL file created: $sql_file"
