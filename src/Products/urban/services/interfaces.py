# -*- coding: utf-8 -*-

from zope.interface import Attribute
from zope.interface import Interface


class ISQLSession (Interface):
    """
    Base class wrapping a sqlalchemy session instance and used
    to define every query method.
    """

    session = Attribute("""sqlalchemy session object""")

    def execute(self, str_query):
        """ Execute a string representing a sql query. """

    def close(self):
        """ Close the sqlalchemy session. """
