# KU POLLS

Polls web application powered by Django by follow [Django Tutorial](https://docs.djangoproject.com/en/5.1/intro/) used to conduct polls or surveys in the KU community
with a simple web interface for creating polls with opening and closing for each poll or survey question,
responding to opened polls and seeing the results of a poll even if the poll is closed.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

## Requirements
- Python 3.11.x or newer
- Django 5.1

## Installation
1.  Create python virtual environment `python -m venv venv`
2.  Activate the virtual environment `venv/Scripts/activate.bat`
3.  Install required package `pip install -r requirements.txt`
2. run `python manage.py migrate` to apply the database schema and initialize the database.

## Running the application
1.  Load the poll data `python manage.py loaddata data/<filename>`
2.  Run `python manage.py runserver` to start the web application.


## Project Details
All details can be found at [KU Polls Wiki](../../wiki/Home) including:
- [Project Vision and Scope](/../../wiki/Vision-and-Scope)
- [Project Plan](/../../wiki/Project-Plan)
- [Project Requirements](/../../wiki/Requirements)
