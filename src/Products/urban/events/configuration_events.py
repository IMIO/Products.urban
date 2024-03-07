# -*- coding: utf-8 -*-

from plone import api
from zope.globalrequest import getRequest
from zope.i18n import translate
from OFS.ObjectManager import BeforeDeleteException
from Products.urban.interfaces import IGenericLicence
from Products.urban import UrbanMessage as _


def activate_optional_fields(portal_urban, event):
    if portal_urban.getUsedAttributes():
        for cfg in portal_urban.get_all_licence_configs():
            for field_name in portal_urban.getUsedAttributes():
                to_activate = []
                if field_name in cfg.listUsedAttributes():
                    if field_name not in cfg.getUsedAttributes():
                        to_activate.append(field_name)
            cfg.setUsedAttributes(cfg.getUsedAttributes() + tuple(to_activate))
    portal_urban.setUsedAttributes([])


def update_vocabulary_term_cache(config_obj, event):
    portal_urban = api.portal.get_tool("portal_urban")
    voc_folder = config_obj.aq_parent
    config_folder = voc_folder.aq_parent
    if config_folder.getId() != "portal_factory":
        with api.env.adopt_roles(["Manager"]):
            cache_view = portal_urban.restrictedTraverse("urban_vocabulary_cache")
            cache_view.update_procedure_vocabulary_cache(config_folder, voc_folder)


def update_vocabulary_folder_cache(voc_folder, event):
    portal_urban = api.portal.get_tool("portal_urban")
    config_folder = voc_folder.aq_parent
    if config_folder.getId() != "portal_factory":
        with api.env.adopt_roles(["Manager"]):
            cache_view = portal_urban.restrictedTraverse("urban_vocabulary_cache")
            cache_view.update_procedure_vocabulary_cache(config_folder, voc_folder)


def before_street_delete(current_street, event):
    """
    Checks if the street can be deleted
    """

    if event.object.meta_type == "Plone Site":
        return

    street_uid = current_street.UID()
    request = getRequest()
    catalog = api.portal.get_tool("portal_catalog")
    licence_brains = catalog(object_provides=IGenericLicence.__identifier__)
    licences = [
        l.getObject()
        for l in licence_brains
        if IGenericLicence.providedBy(l.getObject())
    ]
    for licence in licences:
        address = licence.getWorkLocations()
        for wl in address:
            if wl["street"] == street_uid:
                raise BeforeDeleteException(
                    u"{} {}".format(
                        translate(
                            _(u"can_not_delete_street_in_config"),
                            domain="urban",
                            context=request,
                        ),
                        " : {}".format(licence.reference),
                    )
                )
