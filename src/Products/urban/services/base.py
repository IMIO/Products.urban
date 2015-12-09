# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _

from plone import api

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker

DB_NO_CONNECTION_ERROR = "No DB Connection"


class Tables(object):
    """
    """


class Service(object):
    """
    Helper with sqlalchemy engine, metadata and session objects.
    """

    def __init__(self, dialect, user, host, db_name, password=''):
        self.engine = self._init_engine(dialect, user, host, db_name, password)
        self.metadata = MetaData(self.engine)
        self.tables = Tables()  # use _init_table to set sqlalchemy table objects on it

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

    def _init_table(self, table_name, column_names):
        table = Table(table_name, self.metadata, autoload=True)
        for column_name in column_names:
            setattr(table, column_name, table.columns[column_name])
        setattr(self.tables, table_name, table)

    def __getattr__(self, attr_name):
        """
        Implicitely create a Session an try to delegate any query method
        call to it.
        """
        session = self.new_session()
        if hasattr(session, attr_name):
            return getattr(session, attr_name)
        return getattr(self, attr_name)

    def connect(self):
        return self.engine.connect()

    def can_connect(self):
        try:
            self.connect()
        except Exception:
            return False
        return True

    def check_connection(self):
        """
           Check if the provided parameters are OK
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
        return Session(self)


class Session(object):
    """
    Base class wrapping a sqlalchemy query session.
    Group all query methods here.
    """

    def __init__(self, service):
        self.service = service
        self.tables = service.tables
        self.session = sessionmaker(service.engine)()

    def close(self):
        self.session.close()
