# -*- coding: utf-8 -*-

from plone import api


def update_vocabulary_term_cache(config_obj, event):
    portal_urban = api.portal.get_tool("portal_urban")
    voc_folder = config_obj.aq_parent
    config_folder = voc_folder.aq_parent
    with api.env.adopt_roles(["Manager"]):
        cache_view = portal_urban.restrictedTraverse("urban_vocabulary_cache")
        cache_view.update_procedure_vocabulary_cache(config_folder, voc_folder)


def update_vocabulary_folder_cache(voc_folder, event):
    portal_urban = api.portal.get_tool("portal_urban")
    config_folder = voc_folder.aq_parent
    with api.env.adopt_roles(["Manager"]):
        cache_view = portal_urban.restrictedTraverse("urban_vocabulary_cache")
        cache_view.update_procedure_vocabulary_cache(config_folder, voc_folder)
