#!/bin/bash

set -e

export PYTHONPATH=${PYTHONPATH:-`pwd`}
export POSTGRES_USER=${POSTGRES_USER:-test}
export POSTGRES_PORT=${POSTGRES_PORT:-5432}
export POSTGRES_URL=${POSTGRES_URL:-localhost}
export POSTGRES_DATABASE=${POSTGRES_DATABASE:-books}
export POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-password}
export POSTGRES_DATABASE_TEST=${POSTGRES_DATABASE:-bookstest}


psql -U postgres -h "${POSTGRES_URL}" -p "${POSTGRES_PORT}" -c "CREATE ROLE ${POSTGRES_USER} PASSWORD '${POSTGRES_PASSWORD}' SUPERUSER CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS"
psql -U postgres -h "${POSTGRES_URL}" -p "${POSTGRES_PORT}" -c "CREATE DATABASE ${POSTGRES_DATABASE} WITH OWNER '${POSTGRES_USER}' ENCODING 'utf8'"
psql -U postgres -h "${POSTGRES_URL}" -p "${POSTGRES_PORT}" -c "CREATE DATABASE ${POSTGRES_DATABASE_TEST} WITH OWNER '${POSTGRES_USER}' ENCODING 'utf8'"
