# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest
import biophony

def test_empty_seq():
    gen = biophony.ElemSeqGen(seq_len = 0)
    assert gen.elements.to_dict() == {"A": 1, "C": 1, "T": 1, "G": 1}
    for n, seq in enumerate(gen):
        assert len(seq) == 0
        assert seq.elements.to_dict() == {}
        i = iter(seq)
        with pytest.raises(StopIteration):
            next(i) # The sequence is empty => no iteration
    assert n + 1 == 1 # pylint: disable=undefined-loop-variable

def test_non_empty_seq():
    for seqlen in [5, 10, 11]:
        gen = biophony.ElemSeqGen(seq_len = seqlen)
        for n, seq in enumerate(gen):
            assert len(seq) == seqlen
            for i, elem in enumerate(seq):
                assert elem in ["A", "C", "T", "G"]
            assert i == seqlen - 1 # pylint: disable=undefined-loop-variable
        assert n + 1 == 1 # pylint: disable=undefined-loop-variable
