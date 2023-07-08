from abc import abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel
from pydantic_settings import BaseSettings


T = TypeVar('T', bound=BaseModel)


class BaseRepositoryRouter:
    def __init__(self, conf: BaseSettings) -> None:
        self.conf = conf
        self.startup_repositories()

    def startup_repositories(self) -> None:
        for name, repo_ in self.__annotations__.items():
            if not issubclass(repo_, BaseRepository):
                continue
            setattr(self, name, repo_(self))


class BaseRepository(Generic[T]):
    class Meta:
        response_model = BaseModel

    def __init__(self, repo: BaseRepositoryRouter) -> None:
        self.repo = repo
        self.conf = repo.conf

    @abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def get(self, uid: UUID) -> T:
        raise NotImplementedError
