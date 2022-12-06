# yab_frontend

## Project Setup

### Prerequisites

* pyenv with a new virtual env

### Setup

```sh
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata apprenants
python manage.py loaddata briefs
```

### Run project

```sh
python manage.py runserver
```