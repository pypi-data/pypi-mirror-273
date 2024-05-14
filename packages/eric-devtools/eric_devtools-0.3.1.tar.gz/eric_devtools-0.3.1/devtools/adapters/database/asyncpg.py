from typing import Optional, Sequence, TypeVar

import asyncpg
from asyncpg.connection import Connection
from asyncpg.pool import Pool
from asyncpg.protocol import Record
from asyncpg.transaction import Transaction

from devtools.attrs import define, info
from devtools.context import AsyncContext, AtomicAsyncAdapter, atomic
from devtools.utils import lazyfield

from .config import DatabaseConfig, db_config_factory, make_uri

RecordT = TypeVar("RecordT", bound=Record)

DEFAULT_PORT = 5432


@define
class ConnectionProxy:
    """
    A proxy class that provides a simple interface for managing transactions and
    executing SQL queries on a database connection.

    :param conn: the underlying `asyncpg.Connection` object to proxy.

    :ivar conn: the underlying `asyncpg.Connection` object that is being proxied.
    :ivar transaction_stack: a list of `asyncpg.Transaction` that have been
    started on the underlying `asyncpg.Connection`.
    """

    conn: Connection
    transaction_stack: list[Transaction]

    def __init__(self, conn: Connection) -> None:
        self.__dattrs_init__(conn, [])  # type: ignore

    @lazyfield
    def _is_closed(self):
        return False

    def closed(self):
        """
        Determines whether the underlying `Connection` is closed.

        :return: `True` if the underlying `Connection` is closed; otherwise, `False`.
        """
        return self._is_closed

    async def close(self):
        """
        Closes the underlying `Connection` and rolls back any outstanding transactions.
        """
        if self.transaction_stack:
            for trx in reversed(self.transaction_stack):
                await trx.rollback()
            self.transaction_stack.clear()
        await self.conn.close()
        ConnectionProxy._is_closed.manual_set(self, True)

    async def transaction(self):
        """
        Starts a new transaction on the underlying `Connection`.
        """
        trx = self.conn.transaction()
        await trx.start()
        self.transaction_stack.append(trx)

    async def commit(self):
        """
        Commits the topmost transaction on the `transaction_stack`.
        """
        if not self.transaction_stack:
            raise RuntimeError("No transaction found in stack")
        trx = self.transaction_stack.pop()
        await trx.commit()

    async def rollback(self):
        """
        Rolls back the topmost transaction on the `transaction_stack`.
        """
        if not self.transaction_stack:
            raise RuntimeError("No transaction found in stack")
        trx = self.transaction_stack.pop()
        await trx.rollback()

    def in_atomic(self):
        """
        Determines whether the `ConnectionProxy` is currently inside a transaction.

        :return: `True` if the `ConnectionProxy` is currently inside a transaction;
        otherwise, `False`.
        """
        return bool(self.transaction_stack)

    def cursor(
        self,
        query: str,
        *args,
        prefetch: Optional[int] = None,
        timeout: Optional[float] = None,
        record_class: Optional[type[Record]] = None,
    ):
        """
        Creates a cursor object that can be used to iterate over the rows of the result.

        :param query: the SQL query to execute.
        :param args: the parameters to pass to the SQL query.
        :param prefetch: the number of rows to prefetch from the database.
        :param timeout: the number of seconds to wait before timing out the SQL query.
        :param record_class: the record class to use for the results of the SQL query.
        :return: a new cursor object that can be used to iterate over the rows of the result.
        """
        return self.conn.cursor(
            query,
            *args,
            prefetch=prefetch,
            timeout=timeout,
            record_class=record_class,
        )

    async def execute(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ):
        """
        Executes an SQL query and returns the result status.

        :param query: the SQL query to execute.
        :param args: the parameters to pass to the SQL query.
        :param timeout: the number of seconds to wait before timing out the SQL query.
        :return: the result status of the SQL query.
        """
        return await self.conn.execute(
            query, *args, timeout=timeout  # type:ignore
        )

    async def executemany(
        self,
        command: str,
        args: Sequence[Sequence],
        *,
        timeout: Optional[float] = None,
    ):
        """
        Executes an SQL query and returns the result status.

        :param query: the SQL query to execute.
        :param args: the parameters to pass to the SQL query.
        :param timeout: the number of seconds to wait before timing out the SQL query.
        :return: the result status of the SQL query.
        """
        return await self.conn.executemany(
            command, args, timeout=timeout  # type:ignore
        )

    async def fetch(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
        record_class: type[RecordT] = None,
    ) -> list[RecordT]:
        """
        Executes an SQL query and returns the rows fetched as a list of records.

        :param query: the SQL query to execute.
        :param args: the parameters to pass to the SQL query.
        :param timeout: the number of seconds to wait before timing out the SQL query.
        :param record_class: the class to be used on the record.
        :return: a list of instances of `record_class`.
        """
        return await self.conn.fetch(
            query, *args, timeout=timeout, record_class=record_class
        )

    async def fetchrow(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
        record_class: type[RecordT] = None,
    ) -> Optional[RecordT]:
        """
        Executes an SQL query and returns the first row fetched as a record or None.

        :param query: the SQL query to execute.
        :param args: the parameters to pass to the SQL query.
        :param timeout: the number of seconds to wait before timing out the SQL query.
        :param record_class: the class to be used on the record.
        :return: an instance `record_class`.
        """
        return await self.conn.fetchrow(
            query, *args, timeout=timeout, record_class=record_class
        )


AsyncpgContext = AsyncContext[ConnectionProxy]


@define
class AsyncpgAdapter(AtomicAsyncAdapter[ConnectionProxy]):
    """An adapter for connecting to a PostgreSQL database using asyncpg."""

    config: DatabaseConfig = info(default=db_config_factory)

    @lazyfield
    def uri(self):
        """The URI for the database connection."""
        return make_uri(
            self.config,
            self.config.port if self.config.port != -1 else DEFAULT_PORT,
            "postgres",
        )

    async def init(self):
        """Initialize the adapter by creating a connection pool."""
        pool = asyncpg.create_pool(
            self.uri,
            max_size=self.config.pool_size + self.config.max_overflow,
            max_inactive_connection_lifetime=self.config.pool_recycle,
        )
        await pool  # pool._async_init can return none
        AsyncpgAdapter.pool.manual_set(self, pool)
        AsyncpgAdapter.initialized.manual_set(self, True)

    @lazyfield
    def pool(self) -> Pool:
        """The connection pool used by the adapter."""
        raise RuntimeError("Pool is not initialized yet")

    @lazyfield
    def initialized(self):
        """Whether the adapter has been initialized."""
        return False

    async def is_closed(self, client: ConnectionProxy) -> bool:
        """Check if a database connection is closed."""
        return client.closed()

    async def new(self) -> ConnectionProxy:
        """Create a new database connection."""
        if not self.initialized:
            await self.init()
        return ConnectionProxy(await self.pool.acquire())

    async def release(self, client: ConnectionProxy) -> None:
        """Release a database connection."""
        await client.close()

    async def begin(self, client: ConnectionProxy) -> None:
        """Begin a new transaction."""
        await client.transaction()

    async def commit(self, client: ConnectionProxy) -> None:
        """Commit the current transaction."""
        await client.commit()

    async def rollback(self, client: ConnectionProxy) -> None:
        """Rollback the current transaction."""
        await client.rollback()

    async def in_atomic(self, client: ConnectionProxy) -> bool:
        """Check if a transaction is currently active."""
        return client.in_atomic()

    def context(self):
        """Create a new context for using the adapter."""

        ctx = AsyncpgContext(self)
        return atomic(ctx) if self.config.autotransaction else ctx

    async def dispose(self):
        """
        Shuts down the connection pool and resets the adapter state.

        This method should be called when the application is shutting down or
        when the adapter is no longer needed.

        Raises:
            RuntimeError: If the adapter is not initialized yet.
        """
        if not self.initialized:
            raise RuntimeError("Adapter is not initialized")

        pool = self.pool
        await pool.close()
        AsyncpgAdapter.pool.cleanup(self)
        AsyncpgAdapter.initialized.manual_set(self, False)
