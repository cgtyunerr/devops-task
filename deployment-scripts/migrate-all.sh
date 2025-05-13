#!/bin/bash

deployment-scripts/migrate.sh app/modules/user/pymigrate users
deployment-scripts/migrate.sh app/modules/airline/pymigrate airlines
deployment-scripts/migrate.sh app/modules/aircraft/pymigrate aircrafts
