# pylint: disable=missing-module-docstring
import collections.abc
import typing
from .bio_seq import BioSeq
from .elem_seq import ElemSeq
from .variant_maker import VariantMaker

class BioSeqVarGen(collections.abc.Iterator[BioSeq]):
    """Generator of sequence variants.

    Generates variants of a sequence, as BioSeq objects.

    Args:
        seq: The original sequence for which to generate variants.
        var_maker: The VariantMaker instance used to generate variants.
        count: The number of variants to generate.
        seqid_prefix: The prefix to use when naming the variants.
    """

    def __init__(self, seq: ElemSeq, var_maker: VariantMaker, count: int = 1,
                 seqid_prefix: str = 'seq') -> None:
        self._seq = seq
        self._count = count
        self._var_maker = var_maker
        self._seqid_prefix = seqid_prefix

        self._n: int = 0

    def __iter__(self) -> typing.Self:
        """Gets the iterator on the variants.

        Returns:
            Itself as an iterator.
        """
        return self

    def __next__(self) -> BioSeq:
        """Generates the next variant.

        Returns:
            A BioSeq object.
        """

        self._n += 1

        if self._n > self._count:
            raise StopIteration

        var_seq = self._var_maker.make_elem_seq_var(self._seq)
        var_seqid = self._seqid_prefix + f"_var{self._n}"
        var_desc = f"Variant built, using f{self._var_maker}"
        return BioSeq(seq = var_seq, seqid = var_seqid, desc = var_desc)
