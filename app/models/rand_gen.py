from typing import Annotated, Any
from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, root_validator, validator

from app.services.helpers import is_float_equal


class SetParamsRequest(BaseModel):
    values: Annotated[list[Any], Body(min_items=1)]
    probabilities: Annotated[list[float], Body(min_items=1)]

    @validator('values')
    def check_values(cls, v: list[Any]) -> list[Any]:  # noqa: N805
        if len(v) != len(set(v)):
            raise ValueError('Non uniq values')
        return v

    @validator('probabilities')
    def check_probabilities(cls, v: list[float]) -> list[float]:  # noqa: N805
        if invalid_values := [p for p in v if p < 0 or p > 1]:
            raise ValueError(f'Incorrect values of probabilities: {invalid_values}')
        if not is_float_equal(s := sum(v), 1):
            raise ValueError(f'Sum of probabilities = {s}, instead of 1')
        return v

    @root_validator
    def check_lengths(cls, v: dict[str, Any]) -> dict[str, Any]:  # noqa: N805
        values, probs = v.get('values', []), v.get('probabilities', [])
        if (l_val := len(values)) != (l_prob := len(probs)):
            raise ValueError(f'Different lens: {l_val} != {l_prob}')
        return v


class SetParamsResponse(SetParamsRequest):
    uid: UUID


class GetValuesResponse(BaseModel):
    values: list
