# pylint: disable=missing-module-docstring
import collections.abc
import random
import typing
from .elem_seq import ElemSeq
from .elements import Elements

class ElemSeqVarGen(collections.abc.Iterator[ElemSeq]):
    """Variants generator.

    Args:
        seq: The original sequence.
        count: The number of variants to generate.
        ins_rate: The insertion rate.
        del_rate: The deletion rate.
        mut_rate: The mutation rate.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, seq: ElemSeq, count: int = 1, ins_rate: float = 0.0,
                 del_rate: float = 0.0, mut_rate: float = 0.0) -> None:
        self._orig_seq = seq
        self._count = count
        self._del_rate = del_rate
        self._ins_rate = ins_rate
        self._mut_rate = mut_rate
        self._n = 0 # Number of sequences already generated.

    @property
    def elements(self) -> Elements:
        """The frequency of the elements.

        This is the probability of generation of elements, expressed as weights.
        The probabilities are the exact same values as the submitted sequence.

        Returns:
            The frequency of the elements.
        """
        return self._orig_seq.elements

    def __iter__(self) -> typing.Self:
        """Gets the iterator on the sequence.

        Returns:
            An iterator on the sequence.
        """
        return self

    def _gen_var(self) -> str:

        var = ''

        for elem in self._orig_seq:

            # Get random number in [0.0, 1.0)
            x = random.random()

            # Insertion
            if x < self._ins_rate:
                ins_elem = self._orig_seq.elements.get_rand_elem()
                var += ins_elem + elem

            # Deletion
            elif x < self._ins_rate + self._del_rate:
                continue

            # Mutation
            elif x < self._ins_rate + self._del_rate + self._mut_rate:
                var += self._orig_seq.elements.get_rand_elem(exclude = elem)

            # No change
            else:
                var += elem

        return var

    def __next__(self) -> ElemSeq:
        """Generates a series of sequences.

        Returns:
            A fully generated sequence variant.
        """

        if self._n >= self._count:
            raise StopIteration

        # Count generated sequences
        self._n += 1

        return ElemSeq(self._gen_var())
