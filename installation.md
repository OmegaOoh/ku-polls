# Installation Guide

## Prerequisite

- For MacOS need to install package manager manually which in ths guide will based on [HomeBrew](https://docs.brew.sh/Homebrew-and-Python).

- Linux guide is based on [Ubuntu](https://ubuntu.com)/[Debian](https://www.debian.org/) which has [Apt Package Manager](https://ubuntu.com/server/docs/package-management#advanced-packaging-tool).

1. Have `Python 3.11` Installed.
    You can verify if python version using

   - Windows `python --version`
   - MacOS/Linux `python3 --version`

    If it failed or you're using older version, newer version installer can be found at [Python website](https://www.python.org/downloads/) or you install using system package manager

   - Windows `winget install Python.Python.3.11`
   - MacOS `brew install pyenv` then `pyenv install 3.11`
   - Linux `sudo apt install python3.11`, `sudo apt install python3-pip` then `sudo apt install python3.11-venv`

1. Have `Git` installed verify using `git --version`

    If Git does not install it can be install from [Git Downloads](https://git-scm.com/download/) or using package manager

    - Windows `winget install --id Git.Git -e --source winget`
    - MacOS `brew install git`
    - Linux `apt-get install git`

## Command Line Guide

Most of the Installation will be done in commandline which is **Terminal** in MacOS/Linux and **Command Prompt** in Windows

- `cd <directory_name>` to change directory
- `mkdir <directory_name>` to create directory

## KU Polls Installations

Before installation change working directory to where you want to install the application.

**Notes: Python will called `python` in Windows and `python3` in Linux/MacOS in this guide will use `python3`.

1. Clone the app repository from github using `git clone https://github.com/OmegaOoh/ku-polls.git`
2. Change directory using `cd ku-polls`
3. Create python virtual environment `python3 -m venv myvenv`
4. Activate virtual environment `myvenv/Scripts/Activate`
5. Install required Python package `pip install -r requirements.txt`
6. Migrate Database `python3 manage.py migrate`
7. Load needed data `python3 manage.py loaddata <path-to-file>`
    - Sample data can be found at Data directory, which contains polls (Question + Choice), Votes, and User.
8. Create env file (use sample.env)
    - Windows `copy sample.env .env`
    - MacOS/Linux `cp sample.env .env`
9. Run server `python3 manage.py runserver`

## Further Details

- CSS won't be load while server is ran with out debug
  - If you don't want to turn on DEBUG to True you can runserver with `python3 manage.py runserver --insecure` to have CSS loaded (**NOT RECOMMENDED**)
- You can customize app configuration in `.env` file.
  - SECRET_KEY is key generate by Django with commands
        `python manage.py shell -c "from django.core.management import utils; print(utils.get_random_secret_key())"`
  - DEBUG is Boolean to turn on or off
  - ALLOWED_HOSTS host/domain name django site can server
  - TIME_ZONE is [Timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) the site will works on.
