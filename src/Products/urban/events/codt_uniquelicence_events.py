# -*- coding: utf-8 -*-

from plone import api

from Products.urban.events.licenceEvents import postCreationActions


def UniqueLicencePostCreationActions(licence, event):
    _checkNumerotationSPE(licence)
    # update the licence title
    postCreationActions(licence, event)


def _checkNumerotationSPE(licence):
    registry = api.portal.get_tool("portal_registry")
    if licence.getDefaultSPEReference() == licence.getReferenceSPE():
        value = registry[
            "Products.urban.interfaces.ICODT_UniqueLicence_spe_reference_config.numerotation"
        ]
        value = value + 1
        registry[
            "Products.urban.interfaces.ICODT_UniqueLicence_spe_reference_config.numerotation"
        ] = value
