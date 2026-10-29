from __future__ import annotations

import pytest

from app import create_app
from app.config import Config
from app.db import get_db, init_db
from app.services.auth_service import seed_demo_users


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test-secret"


@pytest.fixture()
def app(tmp_path):
    db_path = tmp_path / "test.db"
    TestConfig.DATABASE_PATH = str(db_path)
    application = create_app(TestConfig)
    with application.app_context():
        init_db()
        seed_demo_users()
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user_count(app):
    with app.app_context():
        row = get_db().execute("SELECT COUNT(*) AS c FROM users").fetchone()
        return int(row["c"])
