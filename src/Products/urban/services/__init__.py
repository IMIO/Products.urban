# -*- coding: utf-8 -*-

from Products.urban.config import ExternalConfig
from Products.urban.services.bestaddress import BestaddressService
from Products.urban.services.cadastral import CadastreService


try:
    config = ExternalConfig('services')
except:
    config = {}

cadastre = CadastreService(**(config and config.cadastre))
bestaddress = BestaddressService(**(config and config.bestaddress))
