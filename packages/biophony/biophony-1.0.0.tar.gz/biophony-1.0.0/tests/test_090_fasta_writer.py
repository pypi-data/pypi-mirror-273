# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import io
import re
import biophony

def test_line_sizes():
    seq = biophony.BioSeq(biophony.ElemSeq("ACTG"))

    output = io.StringIO()
    writer = biophony.FastaWriter(output, header = False)
    writer.write_bio_seq(seq)
    assert output.getvalue() == ">\nACTG\n"

    output = io.StringIO()
    writer = biophony.FastaWriter(output, header = False, seq_line_len = 1)
    writer.write_bio_seq(seq)
    assert output.getvalue() == ">\nA\nC\nT\nG\n"

    output = io.StringIO()
    writer = biophony.FastaWriter(output, header = False, seq_line_len = 2)
    writer.write_bio_seq(seq)
    assert output.getvalue() == ">\nAC\nTG\n"

    output = io.StringIO()
    writer = biophony.FastaWriter(output, header = False, seq_line_len = 3)
    writer.write_bio_seq(seq)
    assert output.getvalue() == ">\nACT\nG\n"

    output = io.StringIO()
    writer = biophony.FastaWriter(output, header = False, seq_line_len = 4)
    writer.write_bio_seq(seq)
    assert output.getvalue() == ">\nACTG\n"

def test_header():
    seq = biophony.BioSeq(biophony.ElemSeq("ACTG"))
    output = io.StringIO()
    writer = biophony.FastaWriter(output, header = True)
    writer.write_bio_seq(seq)
    assert re.match(";.*\n>\nACTG\n", output.getvalue())

def test_seqid():
    seqid = "foo12"
    seq = biophony.BioSeq(biophony.ElemSeq("ACTG"), seqid = seqid)
    output = io.StringIO()
    writer = biophony.FastaWriter(output, header = False)
    writer.write_bio_seq(seq)
    assert f">{seqid}\nACTG\n" == output.getvalue()

def test_description():
    seqid, desc = "foo12", "blabla"
    seq = biophony.BioSeq(biophony.ElemSeq("ACTG"), seqid = seqid, desc = desc)
    output = io.StringIO()
    writer = biophony.FastaWriter(output, header = False)
    writer.write_bio_seq(seq)
    assert f">{seqid} {desc}\nACTG\n" == output.getvalue()
