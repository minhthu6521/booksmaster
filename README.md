This project is for collecting all the epubs books
## Prerequisites
- Docker & docker-compose
- Python 3.8

## Project structure
### Scripts
- For adding new epub books to database
- How to add new book 
```
export PYTHONPATH=`pwd`
python scripts/add_book.py <directory-here>
```
The project uses:
- **ElasticSearch** for the book content 
- **FastAPI** for backend apis
- **PostgreSQL** for other metadata
- **React** for frontend

## Configure Docker
For not using `sudo` for docker anymore in Ubuntu
```
 sudo gpasswd -a $USER docker
 newgrp docker
```

## Setup repository
- Launch the project
```
docker-compose up
```

- First time setup: 
  - Initialize db
    ```
    export PYTHONPATH=`pwd`
    bash books_backend/init-postgres-db.sh
    ```
  - Update alembic
    ```
    alembic upgrade head
    ```
  - Create book index `curl -X PUT "localhost:9201/books?pretty"`
  - Create a user (there is no user management yet) 
- After building
  - Run `docker exec -d database-api /bin/bash -c "install-nltk-package.sh"`

## Useful URLs
- For UI: `localhost:3000`
- ElasticSearch API: `localhost:9201`
- For books content API: `localhost:8001`

## Dev commands

- Create new alembic `alembic revision --autogenerate -m "First migration"`
