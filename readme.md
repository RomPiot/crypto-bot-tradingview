## Installation
Open folder in WSL
python3 -m venv .venv
source .venv/bin/activate
pip install django
python3 -m django --version
Install packages like black, flake8, etc
pip freeze > requirements.txt
or pip install -r requirements.txt if project exists
django-admin startproject projectnamewanted

## Configuration
python3 src/manage.py startapp nameofffolder
create your entities
python3 src/manage.py makemigrations appname
python3 src/manage.py migrate
python3 src/manage.py showmigrations
python3 src/manage.py migrate APPLICATION PREVIOUS_MIGRATION_NAME

# Other
python3 src/manage.py shell

## Administration
python3 src/manage.py createsuperuser

# Open existing Project
Open project in WSL
source .venv/bin/activate
python3 src/manage.py runserver
yarn start



<!-- TODO : login / logout / registration -->
<!-- TODO : get request user connected from back & front -->
<!-- TODO : voltra pour remplacer node version -->
<!-- TODO : setup docker -->
<!-- TODO : admin : form with multi model field relation -->
<!-- TODO : admin : form in model admin -->
<!-- TODO : ajax form on change option -->
<!-- TODO : fix problem vscode discovering python interpreteds git since i pushed -->
<!-- TODO : gerer les mail avec maildev -->
<!-- TODO : gerer les messages flashes : https://betterprogramming.pub/django-flash-messages-6afbccd1b457 -->
