import os
import shutil

from sqlalchemy.pool import StaticPool

import pytest


@pytest.fixture(scope="session")
def app():
    os.environ["FLASK_ENV"] = "testing"
    os.environ["SQLITE_DATABASE_PATH"] = ":memory:"
    os.environ["SKIP_DB_INIT"] = "1"

    from app import app as flask_app
    from database import db, init_db

    flask_app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_ENGINE_OPTIONS": {
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            },
        }
    )

    with flask_app.app_context():
        init_db(flask_app)
        db.drop_all()
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

    os.environ.pop("SKIP_DB_INIT", None)


@pytest.fixture()
def client(app):
    return app.test_client()
