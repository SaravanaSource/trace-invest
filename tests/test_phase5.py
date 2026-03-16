from trace_invest.api.auth import _hash_password


def test_password_hash():
    h = _hash_password("abc")
    assert isinstance(h, str)
    assert len(h) >= 64
