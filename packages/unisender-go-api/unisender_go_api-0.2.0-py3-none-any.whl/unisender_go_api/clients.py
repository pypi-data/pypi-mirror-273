from contextlib import asynccontextmanager, contextmanager, AsyncExitStack  # noqa F401
from contextvars import ContextVar, Token
from dataclasses import dataclass, KW_ONLY, field
from typing import AsyncGenerator, ClassVar, Generator, Type, TypeVar  # noqa F401

import httpx

DEFAULT_UNISENDER_GO_API_ROOT_URL = 'https://go1.unisender.ru/ru/transactional/api/'

SyncClientType = TypeVar('SyncClientType', bound='SyncClient')


@dataclass(frozen=True)
class SyncClient:
    token: str
    _: KW_ONLY
    session: httpx.Client = field(default_factory=httpx.Client)
    unisender_go_api_root_url: str = DEFAULT_UNISENDER_GO_API_ROOT_URL

    default_client: ClassVar[ContextVar['SyncClient']] = ContextVar('default_client')

    @classmethod
    @contextmanager
    def setup(
        cls: Type[SyncClientType],
        token: str,
        *,
        session: httpx.Client | None = None,
        unisender_go_api_root_url: str = DEFAULT_UNISENDER_GO_API_ROOT_URL,
    ) -> Generator[SyncClientType, None, None]:
        if not token.strip():
            # Safety check for empty string or None to avoid confusing HTTP errors
            raise ValueError(f'Unisender Go token is empty: {token!r}')

        if not session:
            session = httpx.Client()

        client = cls(token=token, session=session, unisender_go_api_root_url=unisender_go_api_root_url)
        with client.set_as_default():
            yield client

    @contextmanager
    def set_as_default(self) -> Generator[None, None, None]:
        default_client_token: Token = self.default_client.set(self)
        try:
            yield
        finally:
            self.default_client.reset(default_client_token)
