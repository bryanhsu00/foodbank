# foodbank

![Python Version](https://img.shields.io/badge/Python-3.6-green.svg)
![Django Version](https://img.shields.io/badge/django-2.2.4-green.svg)

## 說明

埔里地方食物銀行進銷存管理系統

## Usage

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
...
python3 manage.py runserver
```
then goto 127.0.0.1:8000 you will see the webpage

if you gonna to use this system, 
1. goto 127.0.0.1:8000/admin create a new foodbank 
2. goto the user editing section
3. add your user to the foodbank


## 結構

```
├── db.sqlite3
├── foodbank
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── inventory
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations/
│   ├── models.py
│   ├── recordViews.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── manage.py
├── media
│   └── images/
├── README.md
├── static
│   └── src
│       ├── bg.jpg
│       └── no_img.png
├── templates
│   ├── 404.html
│   ├── 500.html
│   ├── backstage/
│   ├── index.html
│   ├── inventory
│   │   ├── dashboard.html
│   │   ├── delete.html
│   │   ├── detail.html
│   │   ├── form.html
│   │   ├── formset.html
│   │   ├── read.html
│   │   └── readResource.html
│   ├── message.html
│   ├── registration
│   │   └── login.html
│   └── signup.html
└── user
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations/
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```
## 套件

```
├── Django 2.2.4
├── django-widget-tweaks 
```
