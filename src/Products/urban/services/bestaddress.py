# -*- coding: utf-8 -*-

from Products.urban.services.base import Service
from Products.urban.services.base import Session


class BestaddressService(Service):
    """
    """

    def __init__(self, dialect, user, host, db_name, password=''):
        super(BestaddressService, self).__init__(dialect, user, host, db_name, password)

        if self.can_connect():
            self._init_table('urban_addresses')


class BestaddressSession(Session):
    """
    Implements all the sql queries of bestaddress DB with sqlalchemy methods
    """

    def query_streets(self, city_name=''):
        """
        SELECT * from urban_addresses WHERE commune='%s' order by short_entity
        """
        query = self.session.query(self.tables.urban_addresses)
        query = query.filter_by(commune=city_name)
        query = query.order_by(self.tables.urban_addresses.c.short_entity)
        result = query.all()
        return result
