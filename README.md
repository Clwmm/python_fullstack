# Python FastApi Application

## Overview

This project utilizes Docker to run a frontend and backend application with a SQLite database. Below are the instructions for building, running, and interacting with the services.

## Table of Contents

- [Build and Run](#build-and-run)
- [Service Commands](#service-commands)
- [Accessing the Services](#accessing-the-services)
- [Database Access](#database-access)

## Build and Run

To build and run the application, use the following command:

```bash
docker-compose up --build
```
## Service Commands
Build the services:
```bash
docker-compose build
```

Start the services:
```bash
docker-compose up
```

Stop the containers:
```bash
docker-compose down
```

You can also stop the services by pressing Ctrl + C.

## Accessing the Services
 - Frontend: http://localhost:80
 - Backend: http://localhost:8080
 - FastAPI Docs: http://localhost:8080/docs

## Database Access
To interact with the SQLite database, use the following command:
```bash
sqlite3 backend/test.db
```
## Database Commands
List tables:
```sql
.tables
```
Query users:

```sql
SELECT * FROM users;
```