# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _

from plone import api

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker

DB_NO_CONNECTION_ERROR = "No DB Connection"


class Service(object):
    """
    Helper with sqlalchemy engine , metadata and session objects.
    """

    def __init__(self, dialect, user, host, db_name, password=''):
        self.engine = self._init_engine(dialect, user, host, db_name, password)
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

    def get_table(self, table_name):
        table = Table(table_name, self.metadata, autoload=True)
        return table

    def new_session(self):
        return self.session()
