# -*- coding: utf-8 -*-

from Products.urban import config
from Products.urban.services.bestaddress import BestaddressService
from Products.urban.services.cadastral import CadastreService


cadastre = CadastreService(**config.SERVICES.cadastre)
bestaddress = BestaddressService(**config.SERVICES.bestaddress)
