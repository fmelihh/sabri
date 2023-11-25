import pytest
from backend.src.utils.hash import get_password_hash, verify_password


@pytest.fixture
def hashed_password():
    return "$2b$12$ND7Ar1qoQvG7WGkEDhqR2.ZmAGzQODflP9MohdsRjTAxxUbOk7i1a"


@pytest.fixture
def non_hashed_password():
    return "test"


def test_password_hash(non_hashed_password):
    hashed_password = get_password_hash(non_hashed_password)
    assert non_hashed_password != hashed_password


def test_verify_password_hash(non_hashed_password, hashed_password):
    result = verify_password(non_hashed_password, hashed_password)
    assert result is True
