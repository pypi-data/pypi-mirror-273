# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import biophony

def test_default():
    gen = biophony.BioSeqGen()
    for seq in gen:
        assert isinstance(seq, biophony.BioSeq)
