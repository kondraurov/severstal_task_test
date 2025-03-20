import os
import pytest

os.environ["MODE"] = "TEST"

@pytest.fixture(scope="session")
def setup_database():
    pass