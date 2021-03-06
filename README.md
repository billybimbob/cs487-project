# cs487-project

Make sure python and django are installed:

`python -m django --version`

Also install django-crispy-forms and django-credit-cards:

`pip install django-crispy-forms django-credit-cards`

## Running

Currently using a development server, to launch:

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`

After launching server, app found at:

<http://127.0.0.1:8000/>

## Structure

Divided into 3 main components:

* **accounts**: view or create new accounts to add to the system
* **parkview**: manages parking spot states, and displays views of the parking garages
* **payments**: manage and view future and past payments
