from src.chat_app.utils.hash import get_password_hash, verify_password


def test_password_hash():
    hashed_password = get_password_hash("test")
    assert "test" != hashed_password


def test_verify_password_hash():
    result = verify_password(
        "test", "$2b$12$ND7Ar1qoQvG7WGkEDhqR2.ZmAGzQODflP9MohdsRjTAxxUbOk7i1a"
    )
    assert result is True
