from bisect import bisect
from secrets import SystemRandom
from typing import TypeVar
from uuid import UUID

from app.models.rand_gen import (
    GetValuesResponse,
    SetParamsRequest,
    SetParamsResponse,
)
from app.repositories.rand_gen import repo
from app.services.helpers import is_float_equal


T = TypeVar('T')
TypeValues = list[T]
TypeProbabilities = list[float]


class RandomGen:
    __slots__ = (
        '_random',
        '__values',
        '__probabilities',
        '__probabilities_accumulated',
    )

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
        self.__values: TypeValues = values
        self.__probabilities: TypeProbabilities = probabilities
        self._random: SystemRandom = SystemRandom()

        self.__probabilities_accumulated: TypeProbabilities = []
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

    def next_val(self) -> type[T]:
        """Return an item from given values using given probabilities."""
        return self.__values[bisect(self.__probabilities_accumulated, self._random.random())]


class RandGenService:
    @classmethod
    async def set_params(
        cls: type['RandGenService'],
        params: SetParamsRequest,
    ) -> SetParamsResponse:
        source = repo.rand_gen.create(params=params)
        return SetParamsResponse(
            uid=source.uid,
            values=source.values,
            probabilities=source.probabilities,
        )

    @classmethod
    async def get_values(cls: type['RandGenService'], uid: UUID, amount: int) -> GetValuesResponse:
        source = repo.rand_gen.get(uid=uid)
        rand_gen = RandomGen(values=source.values, probabilities=source.probabilities)
        return GetValuesResponse(values=[rand_gen.next_val() for _ in range(amount)])
