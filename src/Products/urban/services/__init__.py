# -*- coding: utf-8 -*-

from Products.urban.config import ExternalConfig
from Products.urban.services.cadastral import CadastreService


cadastre = CadastreService(**(config_cadastre and config_cadastre.cadastre))
# NOTICe = NOTICeService(**(config_NOTICe and config_NOTICe.NOTICe))
