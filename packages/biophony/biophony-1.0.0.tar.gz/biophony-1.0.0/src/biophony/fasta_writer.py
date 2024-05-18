# pylint: disable=missing-module-docstring
import datetime
import typing
from .bio_seq import BioSeq

class FastaWriter:
    # pylint: disable=too-few-public-methods
    """FASTA file writer.

    Args:
        output: An output stream.
        seq_line_len: The max length of sequence lines.
        header: If enable, writes a header at start of file (i.e.: lines
                starting with a semi-colon).
    """

    def __init__(self, output: typing.TextIO,
                 seq_line_len: int = 80, header: bool = True) -> None:
        self._output = output
        self._seq_line_len = seq_line_len
        if header:
            self._write_header()

    def _write_header(self) -> None:
        date = datetime.datetime.now()
        print(f"; Generated on {date} by biophony package.", file = self._output)

    def write_bio_seq(self, seq: BioSeq) -> None:
        """Writes a sequence to the file.

        Args:
            seq: The sequence to write.
        """

        # ID/Description line
        s = f">{seq.seqid}"
        if seq.desc != '':
            s += f" {seq.desc}"
        fasta = [s]

        # Sequence lines
        i = 0
        while i < len(seq.seq):
            end = min(i + self._seq_line_len, len(seq.seq))
            fasta.append(seq.seq[i:end])
            i = end

        print("\n".join(fasta), file = self._output)
