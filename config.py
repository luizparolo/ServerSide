import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'none'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://myaccount.google.com/'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'}]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'zaaappp.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
