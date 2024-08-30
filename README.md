# KU POLLS

Polls web application powered by Django used to conduct polls or surveys in the KU community
with a simple web interface for creating polls with opening and closing for each poll or survey question,
responding to opened polls and seeing the results of a poll even if the poll is closed.

## Create configuration file
1. Create file name `.env`
2. Add the configuration
```
SECRET_KEY = ''
DEBUG = False
ALLOWED_HOSTS = ''
TIME_ZONE = ''
```
To generate the secret key run this commands
</br>`python manage.py shell -c "from django.core.management import utils; print(utils.get_random_secret_key())"`

## How to run
1. Install required package `pip install -r requirements.txt`
2. Run `python manage.py migrate` to apply the database schema and initialize the database.
3. Run `python manage.py runserver` to start the web application.


## Project Details
All details can be found at [KU Polls Wiki](../../wiki/Home) including:
- [Project Vision and Scope](/../../wiki/Vision-and-Scope)
- [Project Plan](/../../wiki/Project-Plan)
- [Project Requirements](/../../wiki/Requirements)

