# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser

from Products.urban.config import URBAN_CFG_DIR
from Products.urban.services.bestaddress import BestaddressService
from Products.urban.services.cadastral import CadastreService


parser = None
try:
    parser = ConfigParser()
    parser.read('{}/services.cfg'.format(URBAN_CFG_DIR))
except:
    pass


def get_connection_settings(service_name):
    settings = {}
    try:
        settings = dict(parser.items(service_name))
    except:
        pass
    return settings

cadastre = CadastreService(**get_connection_settings('cadastre'))
bestaddress = BestaddressService(**get_connection_settings('bestaddress'))
