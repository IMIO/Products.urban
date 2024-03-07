# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _

from Products.urban.services.interfaces import ISQLSession

from plone import api

from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from zope.component import getAdapter
from zope.interface import implements
from zope.sqlalchemy import ZopeTransactionExtension

DB_NO_CONNECTION_ERROR = "No DB Connection"


class WebService(object):
    """ """

    def __init__(self, url, user="", password=""):
        self.url = url
        self.user = user
        self.password = password


class SQLTables(object):
    """ """


class UnknownSQLTable(object):
    """ """

    def __init__(self, name):
        self.name = name

    def __getattr__(self, name):
        raise NoSuchTableError(self.name)


class SQLService(object):
    """
    Helper with sqlalchemy engine, metadata and session objects.
    """

    def __init__(
        self,
        dialect="postgresql+psycopg2",
        user="",
        host="",
        port="",
        db_name="",
        password="",
        timeout="0",
    ):
        self.engine = self._init_engine(
            dialect, user, host, port, db_name, password, timeout
        )
        self.metadata = MetaData(self.engine)
        self.tables = (
            SQLTables()
        )  # use _init_table to set sqlalchemy table objects on it

    def _init_engine(
        self,
        dialect="",
        username="",
        host="",
        port="",
        db_name="",
        password="",
        timeout="",
    ):
        """
        Initialize the connection.
        """
        connect_args = (
            timeout and {"options": "-c statement_timeout={t}".format(t=timeout)} or {}
        )
        engine = create_engine(
            "{dialect}://{username}{password}@{host}:{port}/{db_name}".format(
                dialect=dialect,
                username=username,
                password=password and ":{}".format(password) or "",
                host=host,
                port=port or "5432",
                db_name=db_name,
            ),
            echo=False,
            connect_args=connect_args,
            poolclass=QueuePool,
        )

        return engine

    def _init_table(self, table_name, column_names=[]):
        """
        You have to explicitely declare tables (and columns) that will
        be queried, do it with this method.
        Each table is set as an attribute of self.tables .
        """
        try:
            table = Table(table_name, self.metadata, autoload=True)
            for column_name in column_names:
                setattr(table, column_name, table.columns[column_name])
        except NoSuchTableError:
            table = UnknownSQLTable(table_name)
        setattr(self.tables, table_name, table)

    def connect(self):
        return self.engine.connect()

    def can_connect(self):
        """
        Check wheter connection is possible or not.
        """
        try:
            self.connect()
        except Exception:
            return False
        return True

    def check_connection(self):
        """
        Check if the provided parameters are OK and set warning
        messages on the site depending on the result.
        """
        plone_utils = api.portal.get_tool("plone_utils")
        try:
            self.connect()
            plone_utils.addPortalMessage(_(u"db_connection_successfull"), type="info")
        except Exception, e:
            plone_utils.addPortalMessage(
                _(
                    u"db_connection_error",
                    mapping={u"error": unicode(e.__str__(), "utf-8")},
                ),
                type="error",
            )
            return False
        return True

    def new_session(self):
        """
        Return a new query session.
        To use when doing several queries to not waste the
        sessions pool.
        """
        return getAdapter(self, ISQLSession)


class SQLSession(object):
    """
    Base class wrapping a sqlalchemy query session.
    Group all query methods here.
    """

    implements(ISQLSession)

    def __init__(self, service):
        self.service = service
        self.tables = service.tables
        self.session = scoped_session(
            sessionmaker(
                bind=service.engine,
                extension=ZopeTransactionExtension(),
            )
        )

    def execute(self, str_query):
        """
        Execute a raw query string.
        """
        return self.service.engine.execute(str_query)

    def close(self):
        self.session.close()
