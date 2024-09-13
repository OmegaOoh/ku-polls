# KU POLLS - Simple Polls Web Application

[![Django CI](https://github.com/OmegaOoh/ku-polls/actions/workflows/django.yml/badge.svg)](https://github.com/OmegaOoh/ku-polls/actions/workflows/django.yml)

Polls web application powered by Django based on [Django Tutorial](https://docs.djangoproject.com/en/5.1/intro/) used to conduct polls or surveys in the KU community
with a simple web interface for creating polls with opening and closing for each poll or survey question,
responding to opened polls and seeing the results of a poll even if the poll is closed.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

## Installations

Guide for installation is written in [Installation Guide](installation.md)

## How to Run

*Notes: Python will called `python` in Windows and `python3` in Linux/MacOS in this guide will use `python3`

If you are created virtual environment from [Intstallation](#installations) you can use `python3 manage.py runserver` to start the server.

To create environment and run the server follow these steps

1. Create python virtual environment

   ```shell
   python3 -m venv myvenv
   ```

2. Activate virtual environment

   ```shell
   myvenv/Scripts/Activate
   ```

3. Install the required Python package

   ```shell
   pip install -r requirements.txt
   ```

4. Run server

    ```shell
    python3 manage.py runserver
    ```

## How to use

After server is running, application can be access by visit `localhost:8000` from any web browser. You can login with [Demo User](#demo-user) or created using [python shell](#how-to-create-user)

Add or Remove of any question or choice can be done from `localhose:8000/admin` which needed to login as superuser, Demo credentials can be found [here](#super-user), or create new superuser using

```shell
python3 manage.py createsuperuser
```

## Demo User

Stored in `data/user.json`

| Username | Password |
|----------|----------|
| demo1    | hackme11 |
| demo2    | hackme22 |
| demo3    | hackme33 |

### Super User

| Username | Password |
|----------|----------|
|admin     | p@ssword |

## How to create user

1. Run python shell

   ```shell
   python3 manage.py shell
   ```

2. import auth module

   ```python
   from django.contrib.auth.models import User
   ```

3. add the user username and password (email is optional), replace all `<...>` your the value needed to adds.

   ```python
   User.objects.create_user(username=<user_name>, password=<password>, email=<email>)
   ```


## Project Documents

All details can be found at [KU Polls Wiki](../../wiki/Home) including:

- [Project Vision and Scope](/../../wiki/Vision-and-Scope)
- [Project Plan](/../../wiki/Project-Plan)
- [Project Requirements](/../../wiki/Requirements)
- [Domain Diagram](../../wiki/Domain-Model)

[Technical Notes](../../wiki/Technical-Note) contains minor technical note along the development of the project
