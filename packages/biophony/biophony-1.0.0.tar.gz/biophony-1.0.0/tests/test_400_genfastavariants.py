# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import biophony

def test_variantmaker_default():
    orig_seq = biophony.ElemSeq('ACTG')
    var_maker = biophony.VariantMaker()
    var_seq = var_maker.make_elem_seq_var(orig_seq)
    assert len(var_seq) == len(orig_seq)
    assert var_seq == orig_seq

def test_variantmaker_deletion():
    orig_seq = biophony.ElemSeq('ACTG')
    var_maker = biophony.VariantMaker(del_rate = 1.0)
    var_seq = var_maker.make_elem_seq_var(orig_seq)
    assert len(var_seq) == 0
    assert var_seq == ''

def test_variantmaker_mutation():
    orig_seq = biophony.ElemSeq('ACTG')
    var_maker = biophony.VariantMaker(mut_rate = 1.0)
    var_seq = var_maker.make_elem_seq_var(orig_seq)
    assert len(var_seq) == len(orig_seq)
    for a, b in zip(var_seq, orig_seq):
        assert a != b

def test_variantmaker_insertion():
    orig_seq = biophony.ElemSeq('ACTG')
    var_maker = biophony.VariantMaker(ins_rate = 1.0)
    var_seq = var_maker.make_elem_seq_var(orig_seq)
    assert len(var_seq) == 2 * len(orig_seq)

    # The variant has one element inserted before each original element
    i = iter(var_seq)
    for orig_elem in orig_seq:
        _, var_elem2 = next(i), next(i)
        assert var_elem2 == orig_elem

def test_bioseqvargen_default():
    orig_seq = biophony.ElemSeq('ACTG')
    vargen = biophony.BioSeqVarGen(orig_seq, biophony.VariantMaker())
    i_vargen = 0
    for var in vargen:
        i_vargen += 1
        assert var.seq == orig_seq
        assert var.seqid == 'seq_var1'
    assert i_vargen == 1
