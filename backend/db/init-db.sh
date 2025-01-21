#!/bin/bash

# Define PostgreSQL environment variables
DB_NAME=${POSTGRES_DB}
INIT_SQL_FILE="/docker-entrypoint-initdb.d/init.sql"

# Check if the database exists
psql -U "$POSTGRES_USER" -tc "SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}'" | grep -q 1

if [ $? -eq 0 ]; then
    echo "Database '${DB_NAME}' already exists. Skipping initialization."
else
    echo "Database '${DB_NAME}' does not exist. Creating and initializing..."
    psql -U "$POSTGRES_USER" -c "CREATE DATABASE ${DB_NAME};"
    if [ -f "$INIT_SQL_FILE" ]; then
        echo "Running initialization SQL file: ${INIT_SQL_FILE}"
        psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$INIT_SQL_FILE"
        echo "Database '${DB_NAME}' initialized successfully."
    else
        echo "Initialization SQL file not found: ${INIT_SQL_FILE}. Database created but not initialized."
    fi
fi
