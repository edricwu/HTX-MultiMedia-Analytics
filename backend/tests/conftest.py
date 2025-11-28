import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
import os

TEST_DB_PATH = "test_media.db"   # new test-only DB


@pytest.fixture(scope="session", autouse=True)
def setup_database():

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    os.environ["DB_PATH"] = TEST_DB_PATH
    
    init_db()  # create tables if not exists
    yield  # teardown ignored → small dataset OK

@pytest.fixture
def client():
    return TestClient(app)
