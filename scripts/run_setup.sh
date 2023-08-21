#!/bin/bash

mkdir -p ./apps/static
mkdir -p ./apps/templates
mkdir -p staticfiles

VENV_PATH="venv"
LOCAL_ENV_PATH="./.envs/.local"
DB_PATH="db.sqlite3"
ENV_PATH="./.envs"

# Check if venv exists
if [ -d "$VENV_PATH" ]; then
  echo "Deleting venv: $VENV_PATH"
  rm -rf "$VENV_PATH"
else
  echo "venv not found: $VENV_PATH"
fi

# Check if envs exists
if [ -f "$ENV_PATH" ]; then
  echo "Deleting local_env: $ENV_PATH"
  rm -rf "$ENV_PATH"
else
  echo "local_env not found: $LOCAL_ENV_PATH"
fi

# Check if the file exists
if [ -f "$DB_PATH" ]; then
  echo "Deleting db: $DB_PATH"
  rm "$DB_PATH"
else
  echo "db not found: $DB_PATH"
fi

#Creating .local in .envs
mkdir -p .envs
touch .envs/.local

cat << EOF > "$LOCAL_ENV_PATH"
## do not put this file under version control!
DEBUG=False

## Super-User Credentials
SUPER_USER_NAME='root'
SUPER_USER_PASSWORD='root'
SUPER_USER_EMAIL='kushagraagra002@gmail.com'

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=moneyeem_postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234

DJANGO_SETTINGS_MODULE=moneyeem_backend.settings.production

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.zoho.in'
EMAIL_PORT=465
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD='#Password008'
DEFAULT_FROM_EMAIL=''
EMAIL_USE_SSL=True
EMAIL_USE_TSL=False

DOMAIN=''
EOF

echo "File created: $LOCAL_ENV_PATH"

# Generate a random key using /dev/urandom
KEY=$(python3 -c 'import random; import string; print("".join(random.SystemRandom().choice(string.ascii_letters + string.digits + "!@#$%^&*(-_=+)") for _ in range(50)))')

#.local file update
echo "SECRET_KEY='$KEY'" >> $LOCAL_ENV_PATH
echo "GENERATED KEY: $KEY"

pip3 install virtualenv==20.15.1

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements/local.txt

# Run migrations
echo "RUNNING MIGRATIONS"
python manage.py makemigrations --settings=config.settings.local


# Run migrate
echo "RUNNING MIGRATE"
python manage.py migrate --settings=config.settings.local


# Run local script
python manage.py runserver $1 --settings=config.settings.local
