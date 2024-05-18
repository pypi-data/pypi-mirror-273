# pylint: disable=missing-module-docstring
import argparse
import sys
from .bio_seq_gen import BioSeqGen
from .elements import Elements
from .fasta_writer import FastaWriter

def read_args() -> argparse.Namespace:
    # pylint: disable=missing-function-docstring
    parser = argparse.ArgumentParser(description = 'Generates FASTA files.',
        formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', '--length', dest='length', default=1000, type=int,
        help='The length of the generated sequence.')
    parser.add_argument('--line-size', dest='line_size', default=80, type=int,
        help='Maximum number of characters on each line.')
    parser.add_argument('-e', '--elements', dest='elements', default='ACTG',
        help='The set of elements to use.')
    parser.add_argument('-s', '--seqid', dest='seqid', default='chr',
        help='SeqID.')
    args = parser.parse_args()
    return args

def fastagen_cli() -> None:
    """FASTA generation CLI.
    """

    args = read_args()

    gen = BioSeqGen(elements = Elements(args.elements),
                    seqlen = args.length, prefix_id = args.seqid)
    writer = FastaWriter(output = sys.stdout, seq_line_len = args.line_size)
    for seq in gen:
        writer.write_bio_seq(seq)

    sys.exit(0)

if __name__ == '__main__':
    fastagen_cli()
