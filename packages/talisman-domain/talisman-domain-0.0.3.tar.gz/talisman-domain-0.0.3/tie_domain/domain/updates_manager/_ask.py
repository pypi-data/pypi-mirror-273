from gql import gql
from typing_extensions import Self

from tie_domain.talisman_api import GQLClientConfig, TalismanAPIAdapter
from ._abstract import AbstractDomainUpdatesManager


class AskKBDomainUpdatesManager(AbstractDomainUpdatesManager):
    def __init__(self, adapter: TalismanAPIAdapter):
        self._adapter = adapter

        self._timestamps: set[tuple] = set()

    async def __aenter__(self) -> Self:
        await self._adapter.__aenter__()
        self._timestamps = await self._get_timestamps()
        return self

    async def __aexit__(self, __exc_type, __exc_value, __traceback):
        self._timestamps = set()
        await self._adapter.__aexit__(__exc_type, __exc_value, __traceback)

    async def _get_timestamps(self) -> set[tuple]:
        from ._queries import domain_info_query
        res = await self._adapter.gql_call(gql(domain_info_query))
        return {(domain_part['name'], domain_part['updateDate']) for domain_part in res['domainUpdateInfo']}

    @property
    async def has_changed(self) -> bool:
        new_timestamps = await self._get_timestamps()
        return self._timestamps != new_timestamps

    async def update(self) -> None:
        self._timestamps = await self._get_timestamps()

    @classmethod
    def from_config(cls, config: dict) -> Self:
        return cls(TalismanAPIAdapter(GQLClientConfig(**config)))
