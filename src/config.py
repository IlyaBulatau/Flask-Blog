from environs import Env

class BaseConfig:
    
    env = Env()
    env.read_env()

    SECRET_KEY = env('SECRET_KEY')
    FLASK_APP = env('FLASK_APP')

    DB_LOGIN = env('DB_LOGIN')
    DB_PASSWORD = env('DB_PASSWORD')
    DB_NAME = env('DB_NAME')

    DEBUG = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_ECHO = None


class DeveloperConfig(BaseConfig):
    DEBUG = 1
    FLASK_DEBUG = 1
    
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{BaseConfig.DB_LOGIN}:{BaseConfig.DB_PASSWORD}@localhost/{BaseConfig.DB_NAME}'
    SQLALCHEMY_ECHO = 1

    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = True

    CKEDITOR_HEIGHT = 200
    CKEDITOR_WIDTH = 750
    CKEDITOR_PKG_TYPE = 'basic'
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class ProductConfig(BaseConfig):
    DEBUG = 0
    SQLALCHEMY_ECHO = 0
