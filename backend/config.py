# SmartCurriculum Backend Configuration
# This file contains all configuration settings for the application

import os
from datetime import timedelta

# Base directory of the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    """Base configuration class with common settings."""
    
    # Secret key for JWT and session management
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart-curriculum-secret-key-2024')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-smart-curriculum')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Database Configuration - Default to SQLite
    # Set DATABASE_TYPE to 'postgresql' to switch databases
    DATABASE_TYPE = os.environ.get('DATABASE_TYPE', 'sqlite')
    
    # SQLite Configuration
    SQLITE_DATABASE_PATH = os.environ.get(
        'SQLITE_DATABASE_PATH',
        os.path.join(BASE_DIR, 'smartcurriculum.db')
    )
    
    # PostgreSQL Configuration (when DATABASE_TYPE='postgresql')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'smartcurriculum')
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')
    
    # Supabase Configuration (alternative PostgreSQL)
    SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')
    
    # Anthropic Claude API Configuration for LLM features
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
    CLAUDE_MODEL = os.environ.get('CLAUDE_MODEL', 'claude-3-5-sonnet-20240620')
    
    # Application Settings
    DEBUG = False
    TESTING = False
    
    # CORS Settings
    CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']
    
    @classmethod
    def get_database_uri(cls):
        """
        Return the appropriate database URI based on configuration.
        Supports easy switching between SQLite and PostgreSQL.
        """
        if cls.DATABASE_TYPE == 'postgresql':
            return f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"
        elif cls.DATABASE_TYPE == 'supabase' and cls.SUPABASE_URL:
            # Parse Supabase connection string
            return cls.SUPABASE_URL
        else:
            # Default to SQLite
            sqlite_path = os.environ.get('SQLITE_DATABASE_PATH', cls.SQLITE_DATABASE_PATH)
            if sqlite_path == ":memory:":
                return "sqlite://"
            return f"sqlite:///{sqlite_path}"


class DevelopmentConfig(Config):
    """Development configuration with debug enabled."""
    DEBUG = True
    

class ProductionConfig(Config):
    """Production configuration with security settings."""
    DEBUG = False
    # In production, override SECRET_KEY via environment variable
    

class TestingConfig(Config):
    """Testing configuration with test database."""
    TESTING = True
    SQLITE_DATABASE_PATH = os.path.join(BASE_DIR, 'test_smartcurriculum.db')


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
