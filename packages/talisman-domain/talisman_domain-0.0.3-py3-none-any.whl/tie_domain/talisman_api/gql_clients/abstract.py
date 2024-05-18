import logging
from abc import ABCMeta
from asyncio import Semaphore
from contextlib import AbstractAsyncContextManager
from typing import Optional

from aiorwlock import RWLock
from gql import Client
from gql.client import AsyncClientSession
from gql.transport.aiohttp import AIOHTTPTransport, log as aiohttp_logger
from gql.transport.requests import log as requests_logger

from tp_interfaces.logging.time import AsyncTimeMeasurer

requests_logger.setLevel(logging.WARNING)
aiohttp_logger.setLevel(logging.ERROR)

logger = logging.getLogger(__name__)


class AsyncAbstractGQLClient(AbstractAsyncContextManager, metaclass=ABCMeta):

    def __init__(self, gql_uri: str, timeout: int = 60, concurrency_limit: int = 10):
        self._gql_uri = gql_uri
        self._timeout = timeout
        self._client: Optional[Client] = None
        self._session: Optional[AsyncClientSession] = None

        self._sema = Semaphore(concurrency_limit)
        self._rw_lock = RWLock()

    async def execute(self, query, variables=None, operation_name=None, extra_headers=None, timeout=None):
        async with self._sema, self._rw_lock.reader_lock:
            async with AsyncTimeMeasurer(
                    f"query {id(query)}", inline_time=True, logger=logger, extra={"query_id": id(query)}, warning_threshold=5000
            ):
                return await self._session.execute(query, variables, operation_name)

    async def _configure_session(self, headers: dict = None):
        async with self._rw_lock.writer_lock:
            await self._close_session()

            transport = AIOHTTPTransport(url=self._gql_uri, headers=headers)
            self._client = Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=self._timeout)

            # here we could change default behaviour of query retrying: just change retry_execute to backoff decorator
            self._session = await self._client.connect_async(reconnecting=True, retry_execute=True)

    async def _close_session(self):
        if self._session is not None:
            await self._client.close_async()
        self._session = None
        self._client = None
