# -*- coding: utf-8 -*-

from zope.interface import Attribute
from zope.interface import Interface


class ISession (Interface):
    """
    Base class wrapping a sqlalchemy session instance and used
    to define every query method.
    """

    session = Attribute("""sqlalchemy session object""")

    def close(self):
        """ Close the sqlalchemy session. """
