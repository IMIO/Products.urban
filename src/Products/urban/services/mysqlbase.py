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
from sqlalchemy.pool import NullPool

from zope.component import getAdapter
from zope.interface import implements
from zope.sqlalchemy import ZopeTransactionExtension

DB_NO_CONNECTION_ERROR = "No DB Connection"


class MySQLService(object):
    """
    Helper with sql alchemy engine, metadata and session object for mysql connections.
    """

    def __init__(
        self,
        dialect="mysql+pymysql",
        user="",
        host="",
        db_name="",
        password="",
        timeout="120000",
    ):
        self.engine = self._init_engine(dialect, user, host, db_name, password, timeout)

    def _init_engine(
        self, dialect="", username="", host="", db_name="", password="", timeout=""
    ):
        """
        Initialize the connection.
        """
        engine = create_engine(
            "{dialect}://{username}{password}@{host}/{db_name}".format(
                dialect=dialect,
                username=username,
                password=password and ":{}".format(password) or "",
                host=host,
                db_name=db_name,
            ),
            echo=True,
            poolclass=NullPool,
        )

        return engine

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

    def dispose_engine(self):
        """
        to dispose the create engine
        """
        return self.engine.dispose()


class MySQLSession(object):
    """
    Base class wrapping a sqlalchemy query session.
    Group all query methods here.
    """

    implements(ISQLSession)

    def __init__(self, service):
        print "ENGINE {}".format(service.engine)
        self.service = service
        factory = sessionmaker(bind=service.engine)
        self.session = factory()

    def execute(self, str_query):
        """
        Execute a raw query string.
        """
        return self.session.execute(str_query)

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()
