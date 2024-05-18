# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import biophony

def test_default():
    cov = biophony.CovGen()
    n = 0
    for x in cov:
        n += 1
        assert isinstance(x, biophony.CovItem)
    assert n == 10001
