# -*- coding: utf-8 -*-

from Products.urban.config import ExternalConfig
from Products.urban.services.cadastral import CadastreService
from Products.urban.services.NOTICe import NOTICeService
from Products.urban.services.parcel_coring import ParcelCoringService

try:
    config_cadastre = ExternalConfig('cadastre')
    config_bestaddress = ExternalConfig('bestaddress')
    config_parcel_coring = ExternalConfig('parcel_coring')
    config_NOTICe = ExternalConfig('NOTICe')
except:
    config = {}

cadastre = CadastreService(**(config_cadastre and config_cadastre.cadastre))
parcel_coring = ParcelCoringService(**(config_parcel_coring and config_parcel_coring.parcel_coring))
# NOTICe = NOTICeService(**(config_NOTICe and config_NOTICe.NOTICe))
