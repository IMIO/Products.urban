# -*- coding: utf-8 -*-

from Products.urban.services.base import PostgresService

from plone import api


class UrbanToolNotInitialised(Exception):
    """ """


class CadastreService(PostgresService):
    """
    """

    def __init__(self):
        connection_infos = self._get_connection_infos()
        super(CadastreService, self).__init__(**connection_infos)

        if self.can_connect():
            self.da = self._init_table('da', column_names=['da', 'divname'])

    def _get_connection_infos(self):
        portal_urban = api.portal.get_tool('portal_urban')

        connection_infos = {
            'username': portal_urban.getSqlUser(),
            'host': portal_urban.getSqlHost(),
            'db_name': portal_urban.getSqlName(),
            'password': portal_urban.getSqlPassword()
        }
        return connection_infos

    def _init_table(self, table_name, column_names):
        table = self.get_table(table_name)
        for column_name in column_names:
            setattr(table, column_name, table.columns[column_name])

        return table

    def get_all_divisions(self):
        session = self.session()
        query = session.query(self.da.da, self.da.divname)
        result = query.all()

        return result
