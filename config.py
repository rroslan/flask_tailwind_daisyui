import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base configuration with common settings"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    
    # PostgreSQL configuration
    POSTGRES_USER = os.environ.get('POSTGRES_USER') or 'flask_user'
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD') or 'flask_password'
    POSTGRES_DB = os.environ.get('POSTGRES_DB') or 'flask_app'
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST') or 'localhost'
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT') or '5432'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300
    }

class DevelopmentConfig(Config):
    """Development specific configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production specific configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False

# Default to development config
config = DevelopmentConfig

