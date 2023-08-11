# -*- coding: utf-8 -*-

from Products.urban.config import ExternalConfig
from Products.urban.services.cadastral import CadastreService
from Products.urban.services.parcel_coring import ParcelCoringService
from Products.urban.services.gig import GigService


try:
    config_cadastre = ExternalConfig('cadastre')
    config_parcel_coring = ExternalConfig('parcel_coring')
    config_gig = ExternalConfig('gig')
except Exception:
    config = {}
    config_gig = {}


cadastre = CadastreService(**(config_cadastre and config_cadastre.cadastre))
parcel_coring = ParcelCoringService(**(config_parcel_coring and config_parcel_coring.parcel_coring))
gig = GigService(**(config_gig and config_gig.gig))
# NOTICe = NOTICeService(**(config_NOTICe and config_NOTICe.NOTICe))
