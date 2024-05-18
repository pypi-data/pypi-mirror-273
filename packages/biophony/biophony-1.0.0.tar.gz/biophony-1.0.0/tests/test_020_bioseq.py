# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest
import biophony

def test_empty():
    seq = biophony.BioSeq(biophony.ElemSeq(""))
    assert seq.seqid == ""
    assert seq.desc == ""
    assert seq.seq == biophony.ElemSeq("")

def test_properties():
    seq = biophony.BioSeq(biophony.ElemSeq(""), seqid = "myseq", desc = "blabla")
    assert seq.seqid == "myseq"
    assert seq.desc == "blabla"
    seq.seqid = "id2"
    assert seq.seqid == "id2"
    seq.desc = "mydesc"
    assert seq.desc == "mydesc"

def test_with_seq():
    seq = biophony.BioSeq(biophony.ElemSeq("ACTG"))
    assert seq.seqid == ""
    assert seq.desc == ""
    assert seq.seq == biophony.ElemSeq("ACTG")

def test_with_split_seq():
    seq = biophony.BioSeq(biophony.ElemSeq("ACTG"))
    assert seq.seqid == ""
    assert seq.desc == ""
    assert str(seq.seq) == "ACTG"

def test_with_big_seq():
    s = ''.join(["ACTG"] * 20) # 80 characters
    seq = biophony.BioSeq(biophony.ElemSeq(s))
    assert seq.seqid == ""
    assert seq.desc == ""
    assert str(seq.seq) == s
    seq = biophony.BioSeq(biophony.ElemSeq(s + "T"))
    assert seq.seqid == ""
    assert seq.desc == ""
    assert str(seq.seq) == s + "T"

def test_eq():
    seq = biophony.ElemSeq("ACTG")
    with pytest.raises(RuntimeError):
        seq == 2 # pylint: disable=pointless-statement
    assert seq == "ACTG"
    assert seq != "AAAA"
