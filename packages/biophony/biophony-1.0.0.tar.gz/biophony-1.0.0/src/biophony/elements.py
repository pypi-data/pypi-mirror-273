# pylint: disable=missing-module-docstring
import random
import typing

class Elements:
    """Elements.
    
                  {'A': 1, 'C': 1, 'T': 1, 'G': 1} will generate a sequence with
                  the same probability for all elements.
                  {'A': 1, 'C': 1, 'T': 1, 'G': 2} will generate a sequence with
                  1/5 of A, 1/5 of C, 1/5 of T and 2/5 of G.
    """

    def __init__(self, elems: str = "ACTG"):
        self._elems_str = elems
        self._elems: typing.Dict[str, int] = {}
        for e in elems:
            self._inc_weight(e)

    def __len__(self) -> int:
        return len(self._elems)

    def to_dict(self) -> typing.Dict[str, int]:
        """Exports this object as a dictionary.

        Returns:
            A dictionary whose keys are elements and values are the number of
            occurrences of each element (i.e.: its weight).
        """
        return self._elems.copy()

    def get_weight(self, elem: str) -> int:
        """Gets the weight of one particular element.

        Args:
            elem: The element.

        Returns:
            The weight of this element.
        """
        return self._elems[elem] if elem in self._elems else 0

    def _inc_weight(self, elem: str, weight: int = 1) -> None:
        if elem in self._elems:
            self._elems[elem] += weight
        else:
            self._elems[elem] = weight

    def get_rand_elem(self, exclude: str = '', length: int = 1) -> str:
        """Generates random elements.

        Using the weights of the defined elements, randomly chooses elements
        and returns them.

        Args:
            exclude: A string containing elements to ignore. Elements are
                     concatenated together without separator. Example: "AT".
            length: The number of elements to choose.

        Returns:
            A string containing the randomly selected elements, concatenated
            together without separator.
        """

        s = ''

        for i in range(length):

            # Generate an element
            elem = None
            while elem is None:
                i = random.randint(0, len(self._elems_str) - 1)
                elem = self._elems_str[i]
                if elem in exclude:
                    elem = None

            # Append the element
            s += elem

        return s
