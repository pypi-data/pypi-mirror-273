# MODULES
import logging
import time
from typing import Any, Tuple

# SQLALCHEMY
from sqlalchemy import Engine, event
from sqlalchemy.engine import Connection, ExecutionContext
from sqlalchemy.engine.interfaces import DBAPICursor

# PYSQL_REPO
from pysql_repo._database import DataBase as DataBase
from pysql_repo._decorators import with_session as with_session
from pysql_repo._repository import Repository as Repository
from pysql_repo._service import Service as Service
from pysql_repo._utils import (
    RelationshipOption as RelationshipOption,
    FilterType as FilterType,
)
from pysql_repo._constants.enum import (
    Operators as Operators,
    LoadingTechnique as LoadingTechnique,
)


logging.basicConfig()
_logger = logging.getLogger("pysql_repo.cursor")
_logger.setLevel(logging.INFO)


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(
    conn: Connection,
    cursor: DBAPICursor,
    statement: str,
    parameters: Tuple[Any],
    context: ExecutionContext,
    executemany: bool,
) -> None:
    conn.info.setdefault("query_start_time", []).append(time.perf_counter())
    _logger.debug("Start Query: %s, {%s}", statement, parameters)


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(
    conn: Connection,
    cursor: DBAPICursor,
    statement: str,
    parameters: Tuple[Any],
    context: ExecutionContext,
    executemany: bool,
) -> None:
    total = time.perf_counter() - conn.info["query_start_time"].pop(-1)
    _logger.debug("Query completed in %fs", total)
