import os


class Config:
    SECRET_KEY = '9c57435c2f80f446e6b8eed13d5dbc4d'
    SQLALCHEMY_DATABASE_URI = 'postgresql://bharat143:bharat<>?@localhost/news'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')



