from devtools.attrs import define

from devtools.database.typedef import Driver


@define
class DialectInfo:
    default_port: int
    driver: Driver
    dialect_name: str
    async_driver: str
    sync_driver: str
    only_host: bool