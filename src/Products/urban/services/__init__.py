# -*- coding: utf-8 -*-

from Products.urban.config import ExternalConfig
from Products.urban.services.bestaddress import BestaddressService
from Products.urban.services.cadastral import CadastreService
from Products.urban.services.parcel_coring import ParcelCoringService

#try:
#    config = ExternalConfig('services')
#except:
config = {}

cadastre = CadastreService(**(config and config.cadastre))
bestaddress = BestaddressService(**(config and config.bestaddress))
parcel_coring = ParcelCoringService(**(config and config.parcel_coring))
