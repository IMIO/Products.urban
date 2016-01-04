# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _

from Products.urban.services.interfaces import ISQLSession

from plone import api

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker

from zope.component import getAdapter
from zope.interface import implements

DB_NO_CONNECTION_ERROR = "No DB Connection"


class SQLTables(object):
    """
    """


class SQLService(object):
    """
    Helper with sqlalchemy engine, metadata and session objects.
    """

    def __init__(self, dialect, user, host, db_name, password=''):
        self.engine = self._init_engine(dialect, user, host, db_name, password)
        self.metadata = MetaData(self.engine)
        self.tables = SQLTables()  # use _init_table to set sqlalchemy table objects on it

    def _init_engine(self, dialect, username, host, db_name, password=''):
        """
        Initialize the connection.
        """
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

    def _init_table(self, table_name, column_names=[]):
        """
        You have to explicitely declare tables (and columns) that will
        be queried, do it with this method.
        Each table is set as an attribute of self.tables .
        """
        table = Table(table_name, self.metadata, autoload=True)
        for column_name in column_names:
            setattr(table, column_name, table.columns[column_name])
        setattr(self.tables, table_name, table)

    def __getattr__(self, attr_name):
        """
        Try to delegate any query method to an implicetely created
        session.
        """
        session = self.new_session()
        if hasattr(session, attr_name):
            return getattr(session, attr_name)
        raise AttributeError

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
        plone_utils = api.portal.get_tool('plone_utils')
        try:
            self.connect()
            plone_utils.addPortalMessage(
                _(u"db_connection_successfull"),
                type='info'
            )
        except Exception, e:
            plone_utils.addPortalMessage(
                _(
                    u"db_connection_error",
                    mapping={u'error': unicode(e.__str__(), 'utf-8')}
                ),
                type='error'
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
        self.session = sessionmaker(service.engine)()

    def execute(self, str_query):
        """
        Execute a raw query string.
        """
        return self.service.engine.execute(str_query)

    def close(self):
        self.session.close()
