# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser

from Products.urban.config import URBAN_CFG_DIR
from Products.urban.services.cadastral import CadastreService

connection_settings = {}
try:
    parser = ConfigParser()
    parser.read('{}/database.cfg'.format(URBAN_CFG_DIR))
    connection_settings = dict(parser.items('cadastre'))
except:
    pass

cadastre = CadastreService(**connection_settings)
