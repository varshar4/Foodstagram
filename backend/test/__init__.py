import pytest

from app import app
"""Initialize the testing environment

Creates an app for testing that has the configuration flag ``TESTING`` set to
``True``.

"""

@pytest.fixture
def client():

    with app.test_client() as client:
        yield client