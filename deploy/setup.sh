# make sure to run `chmod +x deploy/*.sh` to make setup.sh files excutable!! 

#!/usr/bin/env bash

set -e

# TODO: Set to URL of git repo.
PROJECT_GIT_URL='git@github.com:jeffk713/django-profile-api.git'

PROJECT_BASE_PATH='/usr/local/apps/django-profiles-api' # directory to save the project on AWS server

echo "Installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git
# git: to clone the project
# nginx, supervisor: web-server to serve static files and act as proxy to uwsgi server using supervisor

# Create project directory
mkdir -p $PROJECT_BASE_PATH
git clone $PROJECT_GIT_URL $PROJECT_BASE_PATH

# Create virtual environment
mkdir -p $PROJECT_BASE_PATH/env
python3 -m venv $PROJECT_BASE_PATH/env

# Install python packages
$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirements.txt
$PROJECT_BASE_PATH/env/bin/pip install uwsgi==2.0.18

# Run migrations and collectstatic
cd $PROJECT_BASE_PATH
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput # collect all the static files to serve HTML JS etc.. with Djago

# Configure supervisor, application on linux that allows us to manage proceses; python process & uwsgi server
cp $PROJECT_BASE_PATH/deploy/supervisor_profiles_api.conf /etc/supervisor/conf.d/profiles_api.conf 
  # copy supervisor config into where supervisor is on AWS server 
supervisorctl reread
supervisorctl update
supervisorctl restart profiles_api

# Configure nginx
cp $PROJECT_BASE_PATH/deploy/nginx_profiles_api.conf /etc/nginx/sites-available/profiles_api.conf # copy nginx config
rm /etc/nginx/sites-enabled/default # remove default config upon installing nginx
ln -s /etc/nginx/sites-available/profiles_api.conf /etc/nginx/sites-enabled/profiles_api.conf # add symbolic link
systemctl restart nginx.service

echo "DONE! :)"
