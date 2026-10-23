# SmartCurriculum Test Configuration
# Uses in-memory mongomock for fast, isolated MongoDB testing

import os
import sys

# Ensure backend root is in Python module search path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import mongomock
import pytest
import database


@pytest.fixture(scope="session")
def app():
    os.environ["FLASK_ENV"] = "testing"
    os.environ["SKIP_DB_INIT"] = "1"

    # Set up in-memory mongomock database
    mock_client = mongomock.MongoClient()
    mock_db = mock_client["smartcurriculum_test"]

    # Inject into database module
    database._client = mock_client
    database._db = mock_db

    from app import app as flask_app
    flask_app.config["TESTING"] = True

    yield flask_app

    database.close_db()
    os.environ.pop("SKIP_DB_INIT", None)


@pytest.fixture()
def client(app):
    """Provide a test client with freshly cleared test collections."""
    db = database.get_db()
    for col in ["users", "curricula", "topics", "skills"]:
        db[col].drop()
    return app.test_client()
