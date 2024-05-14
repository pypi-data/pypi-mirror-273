from typing import Protocol

from devtools.database.typedef import Driver


class Dialect(Protocol):
    default_port: int
    driver: Driver
    dialect_name: str
    async_driver: str
    sync_driver: str
    only_host: bool