#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

#? depends on in docker compose waits for postgres container to start
# echo "Waiting for PostgreSQL to start..."
# python <<EOF
# import socket
# import time

# host = "postgres-container"
# port = 5432

# while True:
#     try:
#         with socket.create_connection((host, port), timeout=2):
#             print("PostgreSQL is ready!")
#             break
#     except (OSError, ConnectionRefusedError):
#         print("Waiting for PostgreSQL...")
#         time.sleep(1)
# EOF

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if not exists
echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin")
EOF

# Execute CMD passed from docker-compose.yml
exec "$@"
