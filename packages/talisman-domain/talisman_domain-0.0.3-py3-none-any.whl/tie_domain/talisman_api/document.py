import json
import logging
import os
from contextlib import AbstractAsyncContextManager

import requests
from aiohttp_retry import ExponentialRetry, RetryClient
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from tdm import TalismanDocument, TalismanDocumentModel

from tp_interfaces.logging.time import log_time

logger = logging.getLogger(__name__)


class LoadDocumentResponse(BaseModel):
    id: str


class TalismanDocumentsAPIAdapter(AbstractAsyncContextManager):
    def __init__(self, loader_uri: str):
        self._loader_uri = loader_uri
        env_timeout = os.getenv('LOADER_TIMEOUT', None)
        self._timeout = float(env_timeout) if env_timeout is not None else None

    @log_time(logger=logger, title="Talisman documents adapter initialization")
    async def __aenter__(self):
        self._client = RetryClient(
            logger=logger,
            retry_options=ExponentialRetry(
                attempts=os.getenv('LOADER_RETRIES', 3),
                factor=os.getenv('LOADER_BACKOFF', 2)
            )
        )
        return self

    async def __aexit__(self, __exc_type, __exc_value, __traceback):
        await self._client.close()
        self._client = None

    async def _load_document(self, document_json) -> LoadDocumentResponse:
        try:
            async with self._client.post(self._loader_uri, json=document_json, timeout=self._timeout) as response:
                response.raise_for_status()
                return LoadDocumentResponse.parse_obj(await response.json())
        except requests.HTTPError as e:
            logger.error(f"Got exception loading doc", exc_info=e, extra={"serialized_doc": json.dumps(document_json)})
            raise e

    async def load_tdm(self, doc: TalismanDocument) -> LoadDocumentResponse:
        logger.info(f"Loading document {doc.id}...")
        document_json = jsonable_encoder(TalismanDocumentModel.serialize(doc), exclude_none=True)
        logger.debug(f"Document {doc.id} is prepared for loading")
        load_document = await self._load_document(document_json)
        logger.info(f"Load document {doc.id}. KB id: {load_document.id}")
        return load_document
