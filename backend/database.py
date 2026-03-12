# SmartCurriculum Database Module
# Provides database abstraction layer using SQLAlchemy

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import get_config

# Initialize SQLAlchemy instance
# This will be bound to the Flask app in app.py
db = SQLAlchemy()


def init_db(app):
    """
    Initialize the database with the Flask application.
    
    This function:
    1. Gets the database URI from configuration
    2. Configures SQLAlchemy with the Flask app
    3. Creates all tables if they don't exist
    
    Args:
        app: Flask application instance
    """
    config = get_config()
    
    # Set the database URI in Flask config
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = config.DEBUG  # Log SQL in debug mode
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    # Create all tables within app context
    with app.app_context():
        db.create_all()
        print(f"Database initialized: {config.DATABASE_TYPE}")


def get_db_session():
    """
    Get a new database session for direct database operations.
    Useful for operations outside Flask request context.
    
    Returns:
        SQLAlchemy session object
    """
    config = get_config()
    engine = create_engine(config.get_database_uri())
    Session = sessionmaker(bind=engine)
    return Session()


def reset_db(app):
    """
    Reset the database by dropping and recreating all tables.
    WARNING: This will delete all data!
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database reset complete")


class DatabaseManager:
    """
    Database manager class for common database operations.
    Provides a consistent interface for CRUD operations.
    """
    
    @staticmethod
    def add(model_instance):
        """Add a new record to the database."""
        db.session.add(model_instance)
        db.session.commit()
        return model_instance
    
    @staticmethod
    def update():
        """Commit pending changes to the database."""
        db.session.commit()
    
    @staticmethod
    def delete(model_instance):
        """Delete a record from the database."""
        db.session.delete(model_instance)
        db.session.commit()
    
    @staticmethod
    def get_by_id(model_class, record_id):
        """Get a record by its ID."""
        return model_class.query.get(record_id)
    
    @staticmethod
    def get_all(model_class):
        """Get all records of a model."""
        return model_class.query.all()
    
    @staticmethod
    def filter_by(model_class, **kwargs):
        """Filter records by given criteria."""
        return model_class.query.filter_by(**kwargs).all()
    
    @staticmethod
    def first_or_none(model_class, **kwargs):
        """Get first matching record or None."""
        return model_class.query.filter_by(**kwargs).first()
