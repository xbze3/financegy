from financegy import get_securities

def test_get_securities():
    securities = get_securities()
    assert isinstance(securities, list)