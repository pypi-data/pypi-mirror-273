# pylint: disable=missing-module-docstring
import argparse
import random
import re
import sys
import typing

def parse_range(s: str) -> typing.Tuple[int, int]:
    # pylint: disable=missing-function-docstring

    m = re.search(r'^(?P<begin>[0-9]+)(-(?P<end>[0-9]+))?$', s)
    if m:
        begin = int(m.group('begin'))
        if m.group('end') is None:
            end = begin
        else:
            end = int(m.group('end'))
    else:
        raise ValueError(f"Wrong range \"{s}\"pos.")

    return (begin, end)

def read_args() -> argparse.Namespace:
    # pylint: disable=missing-function-docstring

    parser = argparse.ArgumentParser(
        description='Generates BED files.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-c', '--chrom', dest='chrom', type=str, default='1',
                        help='The chromosome for which to generate a BED file.')
    parser.add_argument('-p', '--pos', dest='pos', type=str, default='0-10000',
                        help=('The positions to generate.'
                              + ' Either a single value or a range begin-end'
                              + ', where end is included.'))
    parser.add_argument('-d', '--depth', dest='depth', type=str, default='0',
        help=('The depth to generate. A single value or a range start-stop'
              +', stop included.'))
    parser.add_argument('-r', '--depth-change-rate', dest='depth_change_rate',
                        type=float, default=0.0,
        help='Set depth change rate.')
    parser.add_argument('-s', '--depth-start', dest='depth_start', type=int,
                        default='0',
        help=('The starting position from which depth will be generated.'
              +' Any position before this one will get a depth of 0.'))
    args = parser.parse_args()

    return args

class CovItem:
    """A coverage item.

    Corresponds to a line in the BED file.

    Args:
        chrom: The chromosome.
        pos:   The position.
        depth: The coverage depth.
    """

    def __init__(self, chrom: str, pos: int, depth: int) -> None:
        self._chrom = chrom
        self._pos = pos
        self._depth = depth

    def __repr__(self) -> str:
        return f"chr{self._chrom},pos={self._pos},depth={self._depth}"

    def to_bed_line(self) -> str:
        """Exports this item as BED file line.
        """
        return f"chr{self._chrom}\t{self._pos}\t{self._depth}"

# pylint: disable-next=too-many-instance-attributes
class CovGen:
    """Generator of coverage items.
    
    Generates coverage items for writing into a coverage BED file.

    Args:
        chrom: 
        min_pos:
        max_pos:
        min_depth:
        max_depth:
        depth_offset:
        depth_change_rate:
    """

    # pylint: disable-next=too-many-arguments
    def __init__(self, chrom: str='1', min_pos: int=0, max_pos: int=10000,
                 min_depth: int=0, max_depth: int=0, depth_offset: int=0,
                 depth_change_rate: float=0.0) -> None:
        self._chrom = chrom
        self._min_pos = min_pos
        self._max_pos = max_pos
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._depth_offset = depth_offset
        self._depth_change_rate = depth_change_rate

        self._pos = -1
        self._depth: typing.Optional[int] = None

    def __iter__(self) -> 'CovGen':
        """Gets the iterator on the coverage items.

        Returns:
            Itself as an iterator.
        """
        return self

    def __next__(self) -> CovItem:
        """Generates a coverage item.
        
        Returns:
            A coverage item
        """

        # Increase position
        if self._pos < 0:
            self._pos = self._min_pos
        else:
            self._pos += 1

        # Done
        if self._pos > self._max_pos:
            raise StopIteration

        # Update depth
        if self._depth is None:
            if self._pos >= self._depth_offset:
                self._depth = random.randint(self._min_depth, self._max_depth)
        elif self._depth_change_rate > 0.0:
            if random.random() <= self._depth_change_rate:
                self._depth += -1 if random.randint(0, 1) == 0 else +1
                self._depth = min(self._depth, self._max_depth)
                self._depth = max(self._depth, self._min_depth)

        # Generate a new item
        item = CovItem(self._chrom, self._pos,
                       0 if self._depth is None else self._depth)

        return item

def covgen_cli() -> None:
    """Coverage generation CLI.
    """
    args = read_args()
    pos_range = parse_range(args.pos)
    depth_range = parse_range(args.depth)
    gen = CovGen(
        chrom=args.chrom,
        min_pos = pos_range[0],
        max_pos = pos_range[1],
        min_depth = depth_range[0],
        max_depth = depth_range[1],
        depth_offset=args.depth_start,
        depth_change_rate=args.depth_change_rate
    )
    for item in gen:
        print(item.to_bed_line())
    sys.exit(0)

if __name__ == '__main__':
    covgen_cli()
