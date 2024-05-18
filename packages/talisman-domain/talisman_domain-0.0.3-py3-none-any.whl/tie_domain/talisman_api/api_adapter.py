import logging
from contextlib import AbstractAsyncContextManager
from enum import Enum
from typing import Dict, NamedTuple, Optional

from gql import gql
from graphql import DocumentNode, print_ast
from requests import Timeout

from tp_interfaces.logging.time import AsyncTimeMeasurer, log_time
from ._queries import get_pagination_query
from .gql_clients import AsyncAbstractGQLClient, AsyncKeycloakAwareGQLClient, AsyncNoAuthGQLClient

logger = logging.getLogger(__name__)


class APISchema(str, Enum):
    PUBLIC = "public"
    KB_UTILS = "kbutils"


class GQLClientConfig(NamedTuple):
    uri: str
    auth: bool = False
    timeout: int = 60
    concurrency_limit: int = 30

    def configure(self) -> AsyncAbstractGQLClient:
        if self.auth:
            return AsyncKeycloakAwareGQLClient(self.uri, self.timeout, self.concurrency_limit)
        return AsyncNoAuthGQLClient(self.uri, self.timeout, self.concurrency_limit)


class TalismanAPIAdapter(AbstractAsyncContextManager):

    def __init__(self, gql_uri: GQLClientConfig):
        self._gql_uri = gql_uri
        self._gql_client: Optional[AsyncAbstractGQLClient] = None

    async def __aenter__(self):
        self._gql_client = self._gql_uri.configure()
        await self._gql_client.__aenter__()
        return self

    async def __aexit__(self, exc_type=None, exc_val=None, exc_tb=None):
        await self._gql_client.__aexit__(exc_type, exc_val, exc_tb)

        self._gql_client = None

    @log_time(logger=logger)
    async def pagination_query(self, pagination: str, list_query: str) -> Dict:
        query = gql(get_pagination_query(pagination, list_query, 0))
        async with AsyncTimeMeasurer(
                f"{pagination} total query {id(query)}", inline_time=True, logger=logger, warning_threshold=1, extra={"query_id": id(query)}
        ):
            ret = await self.gql_call(query)
        total = list(ret.values())[0]['total']
        query = gql(get_pagination_query(pagination, list_query, total))
        async with AsyncTimeMeasurer(
                f"{pagination} {total} items query {id(query)}", inline_time=True, logger=logger, extra={"query_id": id(query)}
        ):
            return await self.gql_call(query)

    async def gql_call(self, gql_operation: DocumentNode, variables: Optional[dict] = None, raise_on_timeout: bool = True):
        try:
            return await self._gql_client.execute(gql_operation, variables=variables)

        except Timeout as e:
            logger.error('Timeout while query processing', exc_info=e,
                         extra={'query': print_ast(gql_operation), 'variables': str(variables)})
            if raise_on_timeout:
                raise e
        except Exception as e:
            logger.error('Some exception was occured during query processing.', exc_info=e,
                         extra={'query': print_ast(gql_operation), 'variables': str(variables)})
            raise e


class CompositeAdapter(AbstractAsyncContextManager):
    def __init__(self, gql_uris: Dict[str, GQLClientConfig]):
        self._gql_uris = {APISchema(key): TalismanAPIAdapter(value) for key, value in gql_uris.items()}
        self._gql_clients: Optional[Dict[APISchema, TalismanAPIAdapter]] = None

    async def __aenter__(self):
        self._gql_clients = {schema: await adapter.__aenter__() for schema, adapter in self._gql_uris.items()}

        return self

    def __getitem__(self, item: APISchema) -> TalismanAPIAdapter:
        return self._gql_clients.get(item)

    async def __aexit__(self, exc_type=None, exc_val=None, exc_tb=None):
        for gql_client in reversed(tuple(self._gql_clients.values())):
            gql_client: TalismanAPIAdapter
            await gql_client.__aexit__(exc_type, exc_val, exc_tb)
        self._gql_clients = None
