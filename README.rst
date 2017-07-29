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
