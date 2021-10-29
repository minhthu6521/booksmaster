docker exec -i books-postgres-db /bin/bash -c "pg_dump -U postgres ${POSTGRES_DATABASE:-books} > /app/temp/db.pgsql"
docker cp books-postgres-db:db.pgsql temp/