# pylint: disable=missing-module-docstring
import collections.abc
import typing
from .elements import Elements

class ElemSeq(collections.abc.Iterable[str]):
    """Sequences of elements.
    """

    def __init__(self, seq: str) -> None:
        self._seq = seq
        self._n: int = 0 # Iterator index

    def __len__(self) -> int:
        return len(self._seq)

    @property
    def elements(self) -> Elements:
        """Returns the weights of the elements.

        Returns:
            The defined weights.
        """
        return Elements(self._seq)

    def __repr__(self) -> str:
        return self._seq

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self._seq)

    def __getitem__(self, val: int | slice) -> str:
        if isinstance(val, int):
            return self._seq[val]
        return self._seq[val.start:val.stop]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (str, ElemSeq)):
            raise RuntimeError("Equality test accepts only an ElemSeq object.")
        i, j = iter(self), iter(other)
        while True:
            try:
                a = next(i)
            except StopIteration:
                a = None
            try:
                b = next(j)
            except StopIteration:
                b = None
            print(f"{a} == {b} ?")
            if a is None and b is None:
                return True
            if a != b:
                break
        return False
