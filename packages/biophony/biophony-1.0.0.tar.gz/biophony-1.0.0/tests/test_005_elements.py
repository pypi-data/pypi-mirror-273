# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import biophony

def test_default():
    _ = biophony.Elements()

def test_custom():
    elems = biophony.Elements("AAAACCTGGG")
    assert elems.get_weight("A") == 4
    assert elems.get_weight("C") == 2
    assert elems.get_weight("T") == 1
    assert elems.get_weight("G") == 3

def test_get_random_with_exclude():
    elems = biophony.Elements("ACCCCCCCCC")
    for _ in range(22):
        assert elems.get_rand_elem(exclude = "C") == "A"
