# Code structure

## Table of contents
* [Why a modular monolith architecture?](#why-a-modular-monolith-architecture)
* [Structure](#structure)
* [Module](#module)
* [Rules](#rules)

## Why a modular monolith architecture?

We've preferred a modular monolith architecture for our application due to its
balance of simplicity and scalability. By organizing our codebase into modular
components within a single codebase, we can maintain the benefits of a monolithic
architecture, such as simplified deployment and debugging, while also enabling us
to logically separate concerns and scale different parts of the application independently.
This approach promotes cohesive development practices, streamlines communication between modules,
and simplifies code refactoring and maintenance, all of which are crucial for our current
development stage and foreseeable growth.

One of our concerns is when we want to separate the modules to a completely different microservice,
we shouldn't spend a lot of time updating it. So, we agreed some rules that are explained below.

## Structure

The main package structure of our application consists of three distinct folders:

1. api
2. database
3. modules

### `api` folder

We centralize the management of our backend API endpoints, ensuring efficient communication and coordination between different
parts of our application.

### `database` folder
It is dedicated to handling database connections, and providing a centralized location
for database-related operations and configurations.

### `modules` folder
This folder embodies our modular monolith approach, where individual modules encapsulate specific
functionalities of our application, promoting modularization, maintainability, and scalability
while still operating within the cohesive structure of a monolithic architecture.

This folder has `common` folder which contains shared functionalities across different modules.

## Module

Each module is a self-contained unit that encapsulates a specific functionality of our application.

Their domain should be defined clearly and should not overlap with other modules. Also, each module
has its own database schema. Even these different schemas are in the same database, they should not
interact with each other. So, `join` operation is not allowed between different schemas. Moreover,
each module has its own tests, and they should be run independently.

The inner structure of a module is as follows:

```
  +------------+
  |  database  |
  +------------+
        |
+-------|--------------------+
|       |                    |
|  +-----------+  +--------+ |
|  | db(common)|  | domain | |
|  +-----------+  +--------+ |
|        |         |         |
|        +---------+         |
|        | service |         |
|        +---------+         |
|               |            |
| +-------------+            |
| | api(module) |            |
| +-------------+            |
|       |                    |
+-------|--------------------+
        |
   +------------------+
   | api(devops-task) |
   +------------------+
```

#### Database

This component is responsible for accessing the external database backend and
providing methods that abstract the SQL queries.

#### Service

This component obtains data from the `database` component when called by the `api` component.

### API(module)

This component provides a way to access the module's functionality.
Both the API layer of the project and the other modules can only use
this layer of the module.

This layer is responsible for response handling of the `service` layer
methods. It should return the appropriate response or error code.
