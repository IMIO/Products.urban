# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker

DB_NO_CONNECTION_ERROR = "No DB Connection"


class Service(object):
    """
    Helper with sqlalchemy engine , metadata and session objects.
    """

    def __init__(self, dialect, username, host, db_name, password=''):
        self.engine = self._init_engine(dialect, username, host, db_name, password)
        self.metadata = MetaData(self.engine)
        self.session = sessionmaker(self.engine)

    def _init_engine(self, dialect, username, host, db_name, password=''):
        engine = create_engine(
            '{dialect}://{username}{password}@{host}/{db_name}'.format(
                dialect=dialect,
                username=username,
                password=password and ':{}'.format(password) or '',
                host=host,
                db_name=db_name,
            ),
            echo=True
        )

        return engine

    def connect(self):
        return self.engine.connect()

    def can_connect(self):
        try:
            self.connect()
        except Exception:
            return False
        return True

    def get_table(self, table_name):
        table = Table(table_name, self.metadata, autoload=True)
        return table

    def new_session(self):
        return self.session()


class PostgresService(Service):

    def __init__(self, username, host, db_name, password=''):
        super(PostgresService, self).__init__(
            'postgresql+psycopg2',
            username,
            host,
            db_name,
            password
        )
