# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest
import biophony

def test_empty():
    seq = biophony.ElemSeq("")
    assert len(seq) == 0
    assert len(seq.elements) == 0
    i = iter(seq)
    with pytest.raises(StopIteration):
        next(i) # The sequence is empty => no iteration

def test_single_elem():
    seq = biophony.ElemSeq("A")
    assert len(seq) == 1
    assert seq[0] == "A"
    assert len(seq.elements) == 1
    assert seq.elements.get_weight("A") == 1
    for i, elem in enumerate(seq):
        assert elem == "A"
    assert i == 0 # pylint: disable=undefined-loop-variable
    assert list(iter(seq)) == ["A"]

def test_small_seq():
    s = "ACTG"
    seq = biophony.ElemSeq(s)
    assert len(seq) == 4
    assert seq.elements.to_dict() == {"A": 1, "C": 1, "T": 1, "G": 1}
    for i, elem in enumerate(seq):
        assert elem == s[i]
    assert i == 3 # pylint: disable=undefined-loop-variable
    assert list(iter(seq)) == ["A", "C", "T", "G"]
