"""
SQL databases controler
"""
from sqlalchemy import BinaryExpression, ColumnElement, Engine as _Engine
from sqlalchemy.orm import Session as _Session
from typing import TYPE_CHECKING as _TC
if _TC:
    from sqlalchemy.inspection import Inspectable
    from sqlalchemy.orm.util import AliasedClass, AliasedInsp, Mapper
    from sqlalchemy.sql.elements import SQLCoreOperations
    from sqlalchemy.sql.roles import TypedColumnsClauseRole, ColumnsClauseRole, ExpressionElementRole
    from typing import Any, Generator, Literal, Protocol
    class HasClauseElement[TYPE](Protocol):
        """indicates a class that has a __clause_element__() method"""

        def __clause_element__(self) -> ExpressionElementRole[TYPE]:
            ...
    type EntityType[TYPE] = type[TYPE] | AliasedClass[TYPE] | Mapper[TYPE] | AliasedInsp[TYPE]
    type TypedColumnClauseArgument[TYPE] = TypedColumnsClauseRole[TYPE] | SQLCoreOperations[TYPE] | type[TYPE]
    type ColumnsClauseArgument[TYPE] = (TypedColumnsClauseRole[TYPE]
                                        | ColumnsClauseRole
                                        | SQLCoreOperations[TYPE]
                                        | Literal["*", 1]
                                        | type[TYPE]
                                        | Inspectable[HasClauseElement[TYPE]]
                                        | HasClauseElement[TYPE])


def items(url_or_engine: str | _Engine = 'sqlite:///:memory:', *, print_to_console: bool = True, **kw: Any) -> dict[str, list[Any]] | dict[None, None]: ...

def query_gen[TYPE](session: _Session,
                    table: (EntityType[TYPE]
                            | TypedColumnsClauseRole[TYPE]
                            | TypedColumnClauseArgument[TYPE]
                            | ColumnsClauseArgument[TYPE]
                            | None) = None,
                    *filters: ColumnElement[bool] | BinaryExpression[bool],
                    delete: bool = False, commit: bool = False) -> Generator[TYPE, None, None]: ...
