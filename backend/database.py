# SmartCurriculum Database Module
# MongoDB connection management using PyMongo

import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError
from config import get_config

logger = logging.getLogger(__name__)

# Global MongoDB client and database references
_client = None
_db = None


def get_db():
    """
    Get the MongoDB database instance.
    Returns the database object for direct collection access.
    """
    global _db
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db(app) first.")
    return _db


def get_client():
    """Get the underlying MongoClient instance."""
    global _client
    return _client


def init_db(app):
    """
    Initialize the MongoDB connection with the Flask application.

    This function:
    1. Reads MONGODB_URI from configuration
    2. Creates a MongoClient connection
    3. Validates the connection with a ping
    4. Stores the db reference globally

    Args:
        app: Flask application instance
    """
    global _client, _db

    cfg = get_config()
    mongo_uri = cfg.MONGODB_URI
    db_name = cfg.MONGODB_DB_NAME

    try:
        # Create client with a sensible timeout for cloud connections
        _client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=30000
        )

        # Validate connection with ping
        _client.admin.command('ping')

        # Select the database
        _db = _client[db_name]

        # Create indexes for performance
        _ensure_indexes(_db)

        logger.info(f"MongoDB connected: {db_name}")
        print(f"[DB] MongoDB connected: {db_name}")

    except ServerSelectionTimeoutError:
        logger.error("MongoDB connection timed out. Check MONGODB_URI and network access.")
        raise
    except ConnectionFailure as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise
    except ConfigurationError as e:
        logger.error(f"MongoDB configuration error: {e}")
        raise


def close_db():
    """Close the MongoDB connection."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB connection closed.")


def _ensure_indexes(db):
    """
    Create necessary indexes for query performance.
    Called once at startup.
    """
    try:
        # Users collection indexes
        db.users.create_index("email", unique=True)

        # Curricula collection indexes
        db.curricula.create_index("user_id")
        db.curricula.create_index([("user_id", 1), ("status", 1)])
        db.curricula.create_index([("user_id", 1), ("created_at", -1)])

        # Topics collection indexes
        db.topics.create_index("curriculum_id")
        db.topics.create_index([("curriculum_id", 1), ("week", 1), ("order_index", 1)])

        # Skills collection indexes
        db.skills.create_index("user_id")

        logger.info("MongoDB indexes ensured.")
    except Exception as e:
        logger.warning(f"Could not create indexes (non-fatal): {e}")
