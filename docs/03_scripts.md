# Scripts

## Table of contents
* [General Information](#general-information)
* [Test script](#test-script)
* [Migrate script](#migrate-script)
* [Add Migration Script](#add-migration-script)
* [Add Module Script](#add-module-script)
* [Test Setup Script](#test-setup-script)


## General Information
There are five helper scripts added to the project's `./scripts` folder.
These scripts are used to automate some tasks.

**Note: If you are not sure about how to use the scripts, please read the documentation and ask to someone before trying it.**

## Test script

This script is added to run our Python tests using the `pytest`
framework while also measuring the code coverage. It accepts
a single argument which is the path of the module that you want to test.

**Note: Even if it ensures that the database host is set to either "localhost" or "127.0.0.1", please
use this script carefully.**

### How to use it?

```bash
./scripts/test.sh <path_to_module>
```

For example, to test the `data` module:

```bash
./scripts/test.sh app/modules/data
```

## Migrate script

Database migrations are changes to the database needed for the current
`emp-backend` version to work properly. They can modify the schema and/or the
data.

We use our own tool for dealing with database migrations, which is located in
`scripts/python-scripts/migration.py`. It gets the migrations from the selected
migration folder and runs the ones that haven't been already run by considering
the given database schema.

So, this script is added to run new migration files. It accepts two arguments:

1. Path of the migration folder
2. Database schema to run files

**Note: Please be sure that you are giving the correct database schema. Otherwise,
the script will create a new database schema and run the migration files.**

### How to use it?

```bash
./scripts/migrate.sh <path_of_pymigrate_folder> <database_schema>
```

For example, to run the migrations of the `data` module:

```bash
./scripts/migrate.sh app/modules/data/pymigrate data
```

## Add Migration Script

This script is added for creating a new migration file to the selected module. It accepts two arguments:

1. The path of the migration folder
2. The name of the new migration file

This script uses the current time as a prefix for the new migration file name.

### How to use it?

```bash
./scripts/add-migration.sh <path_of_pymigrate_folder> <migration_name>
```

For example, to add a new migration file to the `data` module:

```bash
./scripts/add-migration.sh app/modules/data/pymigrate add-device-data-table
```

## Test Setup Script
This script is added to set up the test environment.
It first runs all the migration files for each module and then, setup the test data.

**Note: Even if it ensures that the database host is set to either "localhost" or "127.0.0.1", please
use this script carefully.**

### How to use it?

```bash
./scripts/test-setup.sh
```

## Deployment Scripts
They are just use in production. Main purpose of these scripts make database migration. Kubernetes' job use them.
