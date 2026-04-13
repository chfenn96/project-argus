import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Sets environment variables before any tests start."""
    os.environ["ARGUS_LOCAL"] = "true"