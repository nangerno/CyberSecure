#!/bin/sh

# Function to wait for a service to be ready
wait_for_service() {
    local host="$1"
    local port="$2"

    while ! nc -z "$host" "$port"; do
        sleep 0.1
    done
}

# Wait for Neo4j database to be ready
wait_for_service "$NEO_SERVER" "$NEO_PORT"

# Wait for the web server to be ready
wait_for_service "$DJANGO_SERVER" "$DJANGO_PORT"

# Load initial data or perform other setup steps
python manage.py load_initial_data

exec "$@"
