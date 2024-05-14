import sqlalchemy as sa

from devtools.attrs import define


@define
class MockTable:
    c: sa.ColumnCollection
