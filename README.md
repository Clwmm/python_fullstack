Build and run:
    docker-compose up --build

Build the serbvices:
    docker-compose build

Start the services:
    docker-compose up

Stop the Containers:
    docker-compose down
    ctrl+c


Frontend:
    localhost:80

Backend:
    localhost:8080

FastApi Docs:
    localhost:8080/docs


Checking DB:
    sqlite3 backend/test.db

    list tables:
        .tables

    Query:
        SELECT * from users;
