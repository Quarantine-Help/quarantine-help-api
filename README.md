# Quarantined help [Backend]

[![Build Status](https://travis-ci.com/github/Quarantine-Help/quarantine-help-api.svg?branch=master)](https://travis-ci.com/github/Quarantine-Help/quarantine-help-api)

Backend for a wishful quarantine people helper application that would be out soon.
Fighting #COVID-19 one step at a time. My wish for this project:

1. Lookup people who are ready to help you out when you are quarantined. For buying groceries etc.
2. Register yourself as someone who can do these errands.
3. A map view with markers and other stuff making it easy for people to access.

## First looks

API documentation: http://docs.quarantinehelp.space/#/

Collaborate at: [Slack:Quarantine Help](https://join.slack.com/t/quarantinehelp/shared_invite/zt-dyk4k8bq-AuymMUti4vs7dm0Glxn5KQ)

## Dependencies

We use `python 3.7.5` for development. Make sure you have this installed on
your machine, or use `pyenv` as described later in this documentation.

## Steps for local development

1. [Mac](#mac-installation)
2. [Windows](#windows-installation)
3. [Ubuntu/Linux](#linux-installation)

<h4 id="mac-installation">Instructions for Mac</h4>

1. Install pyenv and its virtualenv manager using

   ```
   $ brew install pyenv
   $ brew install pyenv-virtualenv
   $ pyenv install 3.7.5
   $ eval "$(pyenv init -)"
   quarantine-help-api/$ pyenv virtualenv 3.7.5 env-3.7.5
   ```

   This will create a pyenv-virtualenv for you and probably place it on your
   `~/home/<username>/.pyenv/versions/`. You can activate that manually using

   ```
   quarantine-help-api/$ source ~/.pyenv/versions/env-3.7.5/bin/activate
   ```

   or even better:

   ```
   quarantine-help-api/$ pyenv activate env-3.7.5
   ```

   or, there are better ways to do this if you follow [Pyenv:Docs](https://github.com/pyenv/pyenv-virtualenv)

2. Now you are in the right environment, install dependencies using:
   ```
   (env-3.7.5) quarantine-help-api/$ pip install -r requirements.txt
   ```
3. Install `postgis` using `brew install postgis`. You can create a database and set the user roles using the following commands:
   ```
   CREATE DATABASE quarantined_db;
   CREATE EXTENSION postgis;
   ALTER EXTENSION postgis UPDATE;
   CREATE USER quarantined_user WITH PASSWORD 'ABCD123<changeThis>';
   GRANT ALL PRIVILEGES ON DATABASE quarantined_db TO quarantined_user;
   ALTER ROLE quarantined_user SET timezone TO 'UTC';
   ALTER ROLE quarantined_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE quarantined_user SET client_encoding TO 'utf8';
   ```
4. We use `pre-commit` hooks to format code. See that you install it using
   https://pre-commit.com/. Later, install our pre-commit hooks using
   `(env-3.7.5) quarantine-help-api/$ pre-commit install`
5. There are some `localsettings` you need to have as part of running the
   server. You can copy a template using:
   `(env-3.7.5) quarantine-help-api/$ cp quarantined_backend/local_settings_sample.py quarantined_backend/local_settings.py`
   You need to modify the values there to use the applicaiton in full.
6. Run the Django standard runserver steps:
   ```
   (env-3.7.5) quarantine-help-api/$ python manage.py migrate
   (env-3.7.5) quarantine-help-api/$ python manage.py collectstatic
   (env-3.7.5) quarantine-help-api/$ python manage.py runserver
   ```
   or even better, run it from pyCharm using your debugger.
7. Create a superuser and add some initial data to the database.

```
(env-3.7.5) quarantine-help-api/$ python manage.py createsuperuser
```

See that we would need a crises object to start with.

<h4 id="windows-installation">Instructions for Windows</h4>

1. Fork and clone the repo:
   After forking this repo, do
   ```
   $ git clone git@github.com:<your-username>/quarantine-help-api.git
   $ cd quarantine-help-api
   quarantine-help-api/$
   ```
2. Create a new environment using **venv** and activate it:

   ```
   quarantine-help-api/$ python -m venv env-3.7.5 python=3.7.5
   (env-3.7.5) quarantine-help-api/$ env-3.7.5/Scripts/activate
   ```

   - You will see a folder named **env-3.7.5** created
   - Here, _env-3.7.5_ is the environment name and we need the environment to run Python 3.7.5

3. Now you are in the right environment, install the dependencies using:
   ```
   (env-3.7.5) quarantine-help-api/$ pip install -r requirements.txt
   ```
4. Install PostGIS - [Reference](https://www.gpsfiledepot.com/tutorials/installing-and-setting-up-postgresql-with-postgis/)

   1. Go to [PostgreSQL windows downloads](https://www.postgresql.org/download/windows)
   2. Download the installer from Enterprise DB
   3. Click windows on the EnterpriseDB page and download the appropriate version for your computer (64bit or 32bit)
   4. Run the `.exe` that has been downloaded to install PostgreSQL
   5. The default settings should be good. When prompted enter a password that you can remember
   6. PostgreSQL's Application Stack Builder will open after finishing the installation
   7. Select **PostgreSQL** from the dropdown and click next

      <!-- ![PostgreSQL Applciation Stack Builder start window](docs/images/postgresql-application-stack-builder-first-window.png) -->
      <p>
      <img src="docs/images/postgresql-application-stack-builder-first-window.png" alt="PostgreSQL Applciation Stack Builder start window" width="360">
      </p>

   8. Under "Spatial Extensions" check the most recent version of PostGIS
      <!-- ![PostgreSQL Applciation Stack Builder second window](images/postgresql-application-stack-builder-second-window.png) -->
      <p>
         <img src="docs/images/postgresql-application-stack-builder-second-window.png" alt="PostgreSQL Applciation Stack Builder second window" width="360">
      </p>
   9. Use default options and after the download finishes click next to start installing
   10. Make sure "create spatial database" is checked and change the database name to **postgis**

5. We use pre-commit hooks to format code. See that you install it using https://pre-commit.com/. Later, install our pre-commit hooks using
   ```
   (env-3.7.5) quarantine-help-api/$ pre-commit install
   ```
6. There are some **localsettings** you need to have as part of running the server.
   You can copy a template using:

   ```
   (env-3.7.5) quarantine-help-api/$ cp quarantined_backend/local_settings_sample.py quarantined_backend/local_settings.py
   ```

   You need to modify the values there to use the application in full

7. Run the Django standard runserver steps:

   ```
   (env-3.7.5) quarantine-help-api/$ python manage.py migrate
   (env-3.7.5) quarantine-help-api/$ python manage.py collectstatic
   (env-3.7.5) quarantine-help-api/$ python manage.py runserver
   ```

   or even better, run it from pyCharm using your debugger

<h4 id="linux-installation">Instructions for Ubuntu/Linux</h4>

1. Install pyenv and its virtualenv manager using

   ```
   $ sudo apt-get update
   $ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
   $ curl https://pyenv.run | bash
   ```

   add the following lines to your `~/.bashrc`:

   ```
   export PATH="$HOME/.pyenv/bin:$PATH"
   eval "$(pyenv init -)"
   eval "$(pyenv virtualenv-init -)"
   ```

   continue installing `python-3.7.5`

   ```
   $ pyenv install 3.7.5
   $ eval "$(pyenv init -)"
   quarantine-help-api/$ pyenv virtualenv 3.7.5 env-3.7.5
   ```

   This will create a pyenv-virtualenv for you and probably place it on your
   `~/home/<username>/.pyenv/versions/`. You can activate that manually using

   ```
   quarantine-help-api/$ source ~/.pyenv/versions/env-3.7.5/bin/activate
   ```

   or even better:

   ```
   quarantine-help-api/$ pyenv activate env-3.7.5
   ```

   or, there are better ways to do this if you follow [Pyenv:Docs](https://github.com/pyenv/pyenv-virtualenv)

2. Now you are in the right environment, install dependencies using:
   ```
   (env-3.7.5) quarantine-help-api/$ pip install -r requirements.txt
   ```
3. Install `postgis` using `sudo apt-get install postgis`. You can create a database and set the user roles using the following commands:
   ```
   CREATE DATABASE quarantined_db;
   CREATE EXTENSION postgis;
   ALTER EXTENSION postgis UPDATE;
   CREATE USER quarantined_user WITH PASSWORD 'ABCD123<changeThis>';
   GRANT ALL PRIVILEGES ON DATABASE quarantined_db TO quarantined_user;
   ALTER ROLE quarantined_user SET timezone TO 'UTC';
   ALTER ROLE quarantined_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE quarantined_user SET client_encoding TO 'utf8';
   ```
4. We use `pre-commit` hooks to format code. See that you install it using
   https://pre-commit.com/. Later, install our pre-commit hooks using
   `(env-3.7.5) quarantine-help-api/$ pre-commit install`
5. There are some `localsettings` you need to have as part of running the
   server. You can copy a template using:
   `(env-3.7.5) quarantine-help-api/$ cp quarantined_backend/local_settings_sample.py quarantined_backend/local_settings.py`
   You need to modify the values there to use the applicaiton in full.
6. Run the Django standard runserver steps:
   ```
   (env-3.7.5) quarantine-help-api/$ python manage.py migrate
   (env-3.7.5) quarantine-help-api/$ python manage.py collectstatic
   (env-3.7.5) quarantine-help-api/$ python manage.py runserver
   ```
   or even better, run it from pyCharm using your debugger.
7. Create a superuser and add some initial data to the database.

```
(env-3.7.5) quarantine-help-api/$ python manage.py createsuperuser
```

See that we would need a crises object to start with.

## Development initial data

You can load fixtures from the folder "fixtures", e.g. `quarantine-help-api/$ python manage.py loaddata fixtures/small`

## Automated tests

You can run the test suite by executing `(env-3.7.5) quarantine-help-api/$ python manage.py test` or setting up the
django test configuration to PyCharm.

## FAQ

1. Getting this error when running `python manage.py migrate` on Windows:
  ```
   django.core.exceptions.ImproperlyConfigured: Could not find the GDAL library (tried "gdal204", "gdal203", "gdal202", "gdal201", "gdal20"). Is GDAL installed? If it is, try setting GDAL_LIBRARY_PATH in your settings.
   ``` 
   
   1. Install GDAL via OSGeo4W - https://stackoverflow.com/a/49159195/9734484
   2. If you are still getting the same error after executing `python manage.py migrate` add gdal version present in `C:/OSGeo4W/bin` to libgdal.py file shown in the error stack, for instance, if gdal300.dll is present add "gdal300" to the list, `lib_names` under os=="nt" for Windows

2. Getting this error when running `python manage.py migrate` on Windows:
   ```
   psycopg2.OperationalError: could not translate host name "DATABASE_HOST" to address: Unknown host
   ```
   Update `quarantined_backend/local_settings.py` file with the right `Database` configurations.
