from uuid import UUID, uuid4

from app.exceptions.rand_gen import RandGenNotFoundError
from app.models.rand_gen import RandGenSource, SetParamsRequest
from app.repositories.base import BaseRepository, BaseRepositoryRouter
from app.settings import conf


class RandGenRepository(BaseRepository[RandGenSource]):
    repo: 'RandGenRepoRouter'

    def __init__(self, repo: BaseRepositoryRouter) -> None:
        super().__init__(repo)
        self.storage: dict[UUID, tuple] = {}

    class Meta:
        response_model = RandGenSource

    def create(self, params: SetParamsRequest) -> RandGenSource:
        uid = uuid4()
        self.storage[uid] = (params.values, params.probabilities)
        return self.Meta.response_model(
            uid=uid,
            values=self.storage[uid][0],
            probabilities=self.storage[uid][1],
        )

    def get_all(self) -> list[RandGenSource]:
        return [
            self.Meta.response_model(uid=uid, values=v[0], probabilities=v[1])
            for uid, v in self.storage.items()
        ]

    def get(self, uid: UUID) -> RandGenSource:
        if not (r := self.storage.get(uid)):
            raise RandGenNotFoundError(f'uid = "{uid}" not found')
        return self.Meta.response_model(uid=uid, values=r[0], probabilities=r[1])


class RandGenRepoRouter(BaseRepositoryRouter):
    rand_gen: RandGenRepository


repo = RandGenRepoRouter(conf)
