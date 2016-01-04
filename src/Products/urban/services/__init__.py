# -*- coding: utf-8 -*-

from Products.urban.config import ExternalConfig
from Products.urban.services.bestaddress import BestaddressService
from Products.urban.services.cadastral import CadastreService


config = ExternalConfig('services')

cadastre = CadastreService(**config.cadastre)
bestaddress = BestaddressService(**config.bestaddress)
