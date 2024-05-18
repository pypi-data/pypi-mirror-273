# pylint: disable=missing-module-docstring
import collections.abc
import typing
from .bio_seq import BioSeq
from .elem_seq_gen import ElemSeqGen
from .elements import Elements

class BioSeqGen(collections.abc.Iterator[BioSeq]):
    """Generator of BioSeq objects.

    Generates a series of random BioSeq objects.

    Args:
        seqlen: The length of the generated sequence.
        elements: The set of elements to use.
        seqid: Sequence ID.
        count: The number of BioSeq objects to generate.
    """

    # pylint: disable-next=too-many-arguments
    def __init__(self, elements: Elements | None = None,
                 seqlen: int = 1000, prefix_id: str = "chr",
                 desc: str = "", count: int = 1) -> None:
        self._elements = Elements() if elements is None else elements
        self._seqlen = seqlen
        self._prefix_id = prefix_id
        self._desc = desc
        self._count = count

        self._n: int = 0 # Current count

    def __iter__(self) -> typing.Self:
        """Gets the iterator on the sequences.

        Returns:
            Itself as an iterator.
        """
        return self

    def __next__(self) -> BioSeq:
        """Generates the next sequence.

        Returns:
            A BioSeq object.
        """

        if self._n < self._count:
            self._n += 1
            gen = ElemSeqGen(seq_len = self._seqlen, elements = self._elements)
            return BioSeq(seqid = f"{self._prefix_id}{self._n}",
                          desc = self._desc, seq = next(gen))

        raise StopIteration
