Django Meeting
==============

Instalation
-----------

Install all python packages: ::

    pip install -r requirements.txt


Database installation
---------------------

Create the PostgreSQL Database User, with the following command (Password m33t1ng): ::

	sudo -u postgres createuser -sP meeting

Create the PostgreSQL Database called 'bizwi', with the following command: ::

	sudo -u postgres createdb -Ttemplate0 -O meeting -EUTF-8 meeting

Meeting configuration
---------------------

All extra and confidential configuration (like database params) is in ``etc/meeting.ini`` file.

Migrate models
--------------

Migrate all django models and meeting models: ::

    ./manage.py migrate

Load data fixtures
------------------

Load all initial data: ::

    ./manage.py loaddata meeting/fixtures/*

Crete a superuser
-----------------

Create a superuser: ::

    ./manage.py createsuperuser

NOTE: The system administrators will be superusers (``is_superuser = True``). The employees are those users who belong to the staff (``is_staff = True``)
