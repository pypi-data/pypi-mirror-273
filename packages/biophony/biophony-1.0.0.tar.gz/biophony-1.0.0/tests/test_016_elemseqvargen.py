# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import biophony

def test_default():
    gen = biophony.ElemSeqVarGen(biophony.ElemSeq("ACTG"))
    assert isinstance(gen.elements, biophony.Elements)
    for var in gen:
        assert isinstance(var, biophony.ElemSeq)
