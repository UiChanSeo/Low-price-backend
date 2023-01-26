from sqlalchemy import create_engine, event, exc
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlalchemy.orm import scoped_session, sessionmaker
from app.model import Base

from app.config import active_conf


class DatabaseFactory(object):

    database_engine = None
    session = None

    @classmethod
    def initialize(cls, app, auto_commit: bool = False):
        cls._create_engine(active_conf.db_url)
        cls.session = cls._create_session(auto_commit=auto_commit)
        Base.metadata.create_all(cls.database_engine, checkfirst=True)

    @classmethod
    def _create_engine(cls, uri):
        cls.database_engine = create_engine(uri, encoding="UTF-8")

    @classmethod
    def _create_session(cls, auto_commit: bool = False):
        with cls.database_engine.connect() as conn:
            session = scoped_session(sessionmaker(
                autocommit=auto_commit, bind=cls.database_engine))
        return session

    @classmethod
    def _has_schema(cls, name):
        return cls.database_engine.dialect.has_schema(cls.database_engine, name)

    @classmethod
    def _create_schema(cls, name):
        cls.database_engine.execute(CreateSchema(name))

    @classmethod
    def _drop_schema(cls, name, cascade=False):
        cls.database_engine.execute(DropSchema(name, cascade=cascade))
