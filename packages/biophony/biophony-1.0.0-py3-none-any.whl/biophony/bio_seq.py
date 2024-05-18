# pylint: disable=missing-module-docstring
from .elem_seq import ElemSeq

class BioSeq():
    """Describes a biological sequence: ID, sequence, description.
    
    The class contains a BioSeq object that contains the sequence, but also the
    sequence ID, if any, and an eventual description.
    
    Args:
        seq: contains the elements of the sequence.
        seqid: the identifier.  
        desc: a description.
    """

    def __init__(self, seq: ElemSeq, seqid: str = '', desc: str = '') -> None:
        self._seq = seq
        self._seqid = seqid
        self._desc = desc

    @property
    def seqid(self) -> str:
        """Returns the sequence ID.

        Returns:
            The ID.
        """
        return self._seqid

    @seqid.setter
    def seqid(self, value: str) -> None:
        self._seqid = value

    @property
    def desc(self) -> str:
        """Returns the description.

        Returns:
            The description.
        """
        return self._desc

    @desc.setter
    def desc(self, value: str) -> None:
        self._desc = value

    @property
    def seq(self) -> ElemSeq:
        """Gets the sequence.

        Returns:
            The sequence.
        """
        return self._seq
