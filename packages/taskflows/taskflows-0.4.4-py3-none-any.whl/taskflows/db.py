import os
import re
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

import sqlalchemy as sa

from taskflows.utils import logger


@lru_cache
def task_flows_db():
    return TaskflowsDB()


class TaskflowsDB:
    def __init__(self) -> None:
        db_url = os.getenv("TASKFLOWS_DB_URL")
        if not db_url:
            db_dir = os.path.expanduser("~/.taskflows")
            db_url = f"sqlite:///{db_dir}/taskflows.sqlite"
            dialect = "sqlite"
        else:
            dialect = re.search(r"^[a-z]+", db_url).group()
            if dialect == "sqlite":
                db_dir = Path(db_url.replace("sqlite:///", "")).parent
        Path(db_dir).mkdir(parents=True, exist_ok=True)
        schema_name = os.getenv("TASKFLOWS_DB_SCHEMA")
        if dialect == "sqlite":
            if schema_name:
                logger.warning(
                    "Schemas are not supported by SQLite. Will not use provided schema: %s",
                    schema_name,
                )
            schema_name = None
            from sqlalchemy.dialects.sqlite import JSON, insert
        elif dialect == "postgresql":
            from sqlalchemy.dialects.postgresql import JSON, insert
            if not schema_name:
                schema_name = "taskflows"
        else:
            raise ValueError(f"Unsupported database dialect: {dialect}")
        logger.info("Using database: %s", db_url)
        sa_meta = sa.MetaData(schema=schema_name)
        engine = sa.create_engine(db_url)
        if schema_name:
            with engine.begin() as conn:
                if not conn.dialect.has_schema(conn, schema_name):
                    logger.info("Creating schema '%s'", schema_name)
                    conn.execute(sa.schema.CreateSchema(schema_name))
        self.task_runs_table = sa.Table(
            "task_runs",
            sa_meta,
            sa.Column("task_name", sa.String, primary_key=True),
            sa.Column(
                "started",
                sa.DateTime(timezone=True),
                default=lambda: datetime.now(timezone.utc),
                primary_key=True,
            ),
            sa.Column("finished", sa.DateTime(timezone=True)),
            sa.Column("retries", sa.Integer, default=0),
            sa.Column("status", sa.String),
        )
        self.task_errors_table = sa.Table(
            "task_errors",
            sa_meta,
            sa.Column("task_name", sa.String, primary_key=True),
            sa.Column(
                "time",
                sa.DateTime(timezone=True),
                default=lambda: datetime.now(timezone.utc),
                primary_key=True,
            ),
            sa.Column("type", sa.String),
            sa.Column("message", sa.String),
        )
        for table in (
            self.task_runs_table,
            self.task_errors_table,
        ):
            with engine.begin() as conn:
                table.create(conn, checkfirst=True)

        def upsert(table: sa.Table, **values):
            statement = insert(table).values(**values)
            on_conf_set = {c.name: c for c in statement.excluded}
            statement = statement.on_conflict_do_update(
                index_elements=table.primary_key.columns, set_=on_conf_set
            )
            with engine.begin() as conn:
                conn.execute(statement)

        self.upsert = upsert
        self.engine = engine
