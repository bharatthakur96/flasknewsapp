from  os import environ


class Config:
    SECRET_KEY = '9c57435c2f80f446e6b8eed13d5dbc4d'
    SQLALCHEMY_DATABASE_URI = 'postgresql://bharat143:bharat<>?@localhost/news'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'EMAIL_USER'
    MAIL_PASSWORD = 'EMAIL_PASSWORD'

class Stripe_keys:
    secret_key = environ.get("STRIPE_SECRET_KEY")
    publishable_key = environ.get("STRIPE_PUBLISHABLE_KEY")
    price_id = environ.get("STRIPE_PRICE_ID")
    endpoint_secret = environ.get("STRIPE_ENDPOINT_SECRET")

