# MODULES
import logging
import time

# SQLALCHEMY
from sqlalchemy import Engine, event

# PYSQL_REPO
from pysql_repo._database import DataBase
from pysql_repo._decorators import with_session
from pysql_repo._repository import Repository
from pysql_repo._service import Service
from pysql_repo._utils import RelationshipOption, FilterType
from pysql_repo._constants.enum import Operators, LoadingTechnique


logging.basicConfig()
_logger = logging.getLogger("pysql_repo.cursor")
_logger.setLevel(logging.INFO)


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.perf_counter())
    _logger.debug("Start Query: %s, {%s}", statement, parameters)


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.perf_counter() - conn.info["query_start_time"].pop(-1)
    _logger.debug("Query completed in %fs", total)
