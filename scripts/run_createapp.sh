#!/bin/sh

# Get the app name argument
APP_NAME=$1

# Check if app name is provided
if [ -z "$APP_NAME" ]; then
  echo "Please provide an app name."
  exit 1
fi

# Run the startapp command
python manage.py startapp "$APP_NAME" --settings=config.settings.local
echo "APP $APP_NAME CRAETED" 


# Move the app to the apps folder
echo "MOVING APP TO apps FOLDER"
mv "$APP_NAME" ./apps/
echo "APP $APP_NAME MOVED TO apps FOLDER"


# update the configs file
echo "UPDATING $APP_NAME CONFIG"
python ./scripts/update_apps.py "$APP_NAME"
echo "UPDATED $APP_NAME CONFIG"


# Update config/settings/base.py
echo "UPDATING SETTINGS"
python scripts/update_settings.py "$APP_NAME"


# Run migrations
echo "RUNNING MIGRATIONS"
python manage.py makemigrations --settings=config.settings.local


# Run migrate
echo "RUNNING MIGRATE"
python manage.py migrate --settings=config.settings.local

echo "SUCCESS!"
