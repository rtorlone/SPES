"""Database module."""

from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging

import sqlalchemy
from anyio.streams import file
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:

    def __init__(self, db_url: str, drop_on_startup: bool, startup_sql_path: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )
        self.drop_on_startup = drop_on_startup
        self.startup_sql_path = startup_sql_path

    def create_database(self) -> None:
        print(type(self.drop_on_startup))
        if self.drop_on_startup:
            Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    def startup(self) -> None:
        if self.startup_sql_path:
            with open(self.startup_sql_path) as f:
                escaped_sql = sqlalchemy.text(f.read())
                self._engine.execute(escaped_sql)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
