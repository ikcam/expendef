import os


FLASK_ENV = os.getenv('FLASK_ENV', 'production')
SECRET_KEY = os.getenv('SECRET_KEY', 'UnsecuredKey')
JWT_SECRET_KEY = SECRET_KEY
JWT_REFRESH_JSON_KEY = 'refresh'
JWT_ERROR_MESSAGE_KEY = 'detail'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False


if FLASK_ENV == 'production':
    from .production_settings import *  # NOQA
elif FLASK_ENV == 'development':
    from .production_settings import *  # NOQA
elif FLASK_ENV == 'testing':
    from .testing_settings import *  # NOQA


try:
    from .local_settings import *  # NOQA
except ModuleNotFoundError:
    pass
