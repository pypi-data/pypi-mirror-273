"SQLAlchemyのメモリ生成データベース"
from typing import Any, Callable, Literal, overload
from sqlalchemy import orm
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy import Engine, create_engine
from sqlalchemy.pool import (
    ConnectionPoolEntry,
    Pool,
)
from sqlalchemy.pool.base import ResetStyle
from sqlalchemy.util import (
    immutabledict,
)
from sqlalchemy.engine.interfaces import (
    IsolationLevel,
    DBAPIConnection,
)
Base: DeclarativeMeta
"""```python

# usage:
class User(Base): ...
class Tweet(Base): ...

user = User(...)
tweet = Tweet(...)

engine = ...
Base.metadata.create_all(engine)
...
```"""

def _info[Class](cls: Class) -> Callable[[Callable[..., Any]], Class]: ...

@_info(orm.sessionmaker)
class sessionmaker: ...


@overload
def memory_engine(
    *,
    connect_args: dict[Any, Any] = ...,
    convert_unicode: bool = ...,
    creator: Callable[..., DBAPIConnection] | Callable[[ConnectionPoolEntry], DBAPIConnection] = ...,
    echo: None | bool | Literal['debug'] = ...,
    echo_pool: None | bool | Literal['debug'] = ...,
    enable_from_linting: bool = ...,
    execution_options: immutabledict[str, Any] = ...,
    future: Literal[True],
    hide_parameters: bool = ...,
    implicit_returning: Literal[True] = ...,
    insertmanyvalues_page_size: int = ...,
    isolation_level: IsolationLevel = ...,
    json_deserializer: Callable[..., Any] = ...,
    json_serializer: Callable[..., Any] = ...,
    label_length: int | None = ...,
    logging_name: str = ...,
    max_identifier_length: int | None = ...,
    max_overflow: int = ...,
    module: Any | None = ...,
    paramstyle: Literal["qmark", "numeric", "named", "format", "pyformat", "numeric_dollar"] | None = ...,
    pool: Pool | None = ...,
    poolclass: type[Pool] | None = ...,
    pool_logging_name: str = ...,
    pool_pre_ping: bool = ...,
    pool_size: int = ...,
    pool_recycle: int = ...,
    pool_reset_on_return: ResetStyle | bool | Literal['commit', 'rollback'] | None = ...,
    pool_timeout: float = ...,
    pool_use_lifo: bool = ...,
    plugins: list[str] = ...,
    query_cache_size: int = ...,
    use_insertmanyvalues: bool = ...,
    **kwargs: Any
) -> Engine:
    """```python

    # definition:
    memory_engine = partial(sqlalchemy.create_engine, 'sqlite:///:memory:')

    # usage:
    engine = memory_engine(echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    ```"""


@overload
def memory_engine(**kwargs: Any) -> Engine:
    """```python

    # definition:
    memory_engine = partial(sqlalchemy.create_engine, 'sqlite:///:memory:')

    # usage:
    engine = memory_engine(echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    ```"""


def make_meta(base: DeclarativeMeta = ..., engine: Engine = ...) -> None:
    """Base.metadata.create_all(engine)の代行サービス"""
