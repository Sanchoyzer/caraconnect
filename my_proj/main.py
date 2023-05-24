from bisect import bisect
from secrets import SystemRandom
from typing import TypeVar

from my_proj.helpers import is_float_equal


T = TypeVar('T')
TypeValues = list[T]
TypeProbabilities = list[float]


class RandomGen:
    _random: SystemRandom
    __values: TypeValues
    __probabilities: TypeProbabilities
    __probabilities_accumulated: TypeProbabilities

    @staticmethod
    def _check(values: TypeValues, probabilities: TypeProbabilities) -> None:
        if (l_val := len(values)) != (l_prob := len(probabilities)):
            raise ValueError(f'Different lens: {l_val} != {l_prob}')
        if not l_val:
            raise ValueError('Zero length')
        if l_val != len(set(values)):
            raise ValueError('Non uniq values')
        if invalid_values := [p for p in probabilities if p < 0 or p > 1]:
            raise ValueError(f'Incorrect values of probabilities: {invalid_values}')
        if not is_float_equal(s := sum(probabilities), 1):
            raise ValueError(f'Sum of probabilities = {s}, instead of 1')

    def __init__(self, values: TypeValues, probabilities: list[float]) -> None:
        self._check(values, probabilities)
        self.__values = values
        self.__probabilities = probabilities
        self._random = SystemRandom()

        self.__probabilities_accumulated = []
        prev_items_sum = 0.0
        for p in self.__probabilities:
            prev_items_sum += p
            self.__probabilities_accumulated.append(prev_items_sum)
        self.__probabilities_accumulated[-1] = 1.0

    def __str__(self) -> str:
        return f'{self.__values} {self.__probabilities}'

    @property
    def values(self) -> TypeValues:
        return self.__values

    @property
    def probabilities(self) -> TypeProbabilities:
        return self.__probabilities

    def next_num(self) -> type[T]:
        """Return an item from given values using given probabilities."""
        return self.__values[bisect(self.__probabilities_accumulated, self._random.random())]
