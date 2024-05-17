"SQLAlchemyのメモリ生成データベース"
from functools import partial
from sqlalchemy import Boolean, Engine, LargeBinary, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Mapped, backref, session as _session
from sqlalchemy.orm.decl_api import DeclarativeMeta

Base = declarative_base()
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

memory_engine = partial(create_engine, 'sqlite:///:memory:')
"""```python

# definition:
memory_engine = partial(sqlalchemy.create_engine, 'sqlite:///:memory:')

# usage:
engine = memory_engine(echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
```"""


def make_meta(base, engine):
    """Base.metadata.create_all(engine)の代行サービス"""
    base.metadata.create_all(engine)
