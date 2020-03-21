# Quarantined help [Backend]

Backend for a wishful quarantine people helper application that would be out soon. 
Fighting #COVID-19 one step at a time. My wish for this project: 
1. Lookup people who are ready to help you out when you are quarantined. For buying groceries etc.
2. Register yourself as someone who can do these errands. 
3. A map view with markers and other stuff making it easy for people to access. 

## First looks 
A sample API result would look like: http://134.122.80.13/api/v1/crisis/1/participants/

## Dependencies

We use `python 3.7.5` for development. Make sure you have this installed on
your machine, or use `pyenv` as described later in this documentation.

## Steps for local development

1. Install pyenv and its virtualenv manager using
   ```
   $ brew install pyenv
   $ brew install pyenv-virtualenv
   $ pyenv install 3.7.5
   $ eval "$(pyenv init -)"
   quarantined_backend/$ pyenv virtualenv 3.7.5 env-3.7.5
   ```
   This will create a pyenv-virtualenv for you and probably place it on your
   `~/home/<username>/.pyenv/versions/`. You can activate that manually using
   ```
   quarantined_backend/$ source ~/.pyenv/versions/env-3.7.5/bin/activate
   ```
   or even better:
   ```
   quarantined_backend/$ pyenv activate env-3.7.5
   ```
   or, there are better ways to do this if you follow https://github
   .com/pyenv/pyenv-virtualenv
2. Now you are in the right environment, install dependencies using:
   ```
   (env-3.7.5) quarantined_backend/$ pip install -r requirements.txt
   ```
3. Install `postgis` using `brew install postgis` 
4. We use `pre-commit` hooks to format code. See that you install it using
   https://pre-commit.com/. Later, install our pre-commit hooks using
   `(env-3.7.5) quarantined_backend/$ pre-commit install`
5. There are some `localsettings` you need to have as part of running the
   server. You can copy a template using:
   `(env-3.7.5) quarantined_backend/$ cp quarantined_backend/local_settings_sample.py quarantined_backend/local_settings.py`
   You need to modify the values there to use the applicaiton in full.
6. Run the Django standard runserver steps:
   ```
   (env-3.7.5) quarantined_backend/$ python manage.py makemigrations
   (env-3.7.5) quarantined_backend/$ python manage.py migrate
   (env-3.7.5) quarantined_backend/$ python manage.py collectstatic
   (env-3.7.5) quarantined_backend/$ python manage.py runserver
   ```
   or even better, run it from pyCharm using your debugger.
