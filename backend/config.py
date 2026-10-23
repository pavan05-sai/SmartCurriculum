# SmartCurriculum Backend Configuration
# All configuration settings for the application

import os
from datetime import timedelta

# Base directory of the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    """Base configuration class with common settings."""

    # Secret key for JWT and session management
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart-curriculum-secret-key-2024')

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-smart-curriculum-production-32bytes+')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # MongoDB Atlas Configuration
    MONGODB_URI = os.environ.get(
        'MONGODB_URI',
        'mongodb://localhost:27017/smartcurriculum'
    )
    MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME', 'smartcurriculum')

    # Anthropic Claude API Configuration for LLM features
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
    CLAUDE_MODEL = os.environ.get('CLAUDE_MODEL', 'claude-3-5-sonnet-20240620')

    # Application Settings
    DEBUG = False
    TESTING = False

    # CORS Settings - comma-separated origins from env or defaults
    _cors_raw = os.environ.get(
        'CORS_ORIGINS',
        'http://localhost:5173,http://localhost:3000'
    )
    CORS_ORIGINS = [o.strip() for o in _cors_raw.split(',') if o.strip()]

    # Server Port
    PORT = int(os.environ.get('PORT', 5000))


class DevelopmentConfig(Config):
    """Development configuration with debug enabled."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration with security settings."""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration with in-memory/test database."""
    TESTING = True
    MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME_TEST', 'smartcurriculum_test')


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get the current configuration based on environment."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
