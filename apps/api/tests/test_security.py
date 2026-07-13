import pytest
from argon2.exceptions import InvalidHashError

from app.core.security import generate_csrf_token, hash_password, verify_password


def test_hash_password_returns_argon2_encoded_hash() -> None:
    password_hash = hash_password("correct horse battery staple")
    assert password_hash.startswith("$argon2id$")


def test_hash_password_uses_a_random_salt() -> None:
    assert hash_password("same-password") != hash_password("same-password")


def test_verify_password_accepts_the_correct_password() -> None:
    password_hash = hash_password("correct horse battery staple")
    assert verify_password("correct horse battery staple", password_hash) is True


def test_verify_password_rejects_the_wrong_password() -> None:
    password_hash = hash_password("correct horse battery staple")
    assert verify_password("wrong password", password_hash) is False


def test_verify_password_raises_on_a_malformed_hash() -> None:
    with pytest.raises(InvalidHashError):
        verify_password("anything", "not-a-real-argon2-hash")


def test_generate_csrf_token_returns_a_nonempty_string() -> None:
    token = generate_csrf_token()
    assert isinstance(token, str)
    assert len(token) > 0


def test_generate_csrf_token_is_unique_per_call() -> None:
    assert generate_csrf_token() != generate_csrf_token()
