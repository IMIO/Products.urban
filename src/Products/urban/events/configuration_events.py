# -*- coding: utf-8 -*-

from plone import api


def update_vocabulary_term_cache(config_obj, event):
    portal_urban = api.portal.get_tool('portal_urban')
    cache_view = portal_urban.restrictedTraverse('urban_vocabulary_cache')
    voc_folder = config_obj.aq_parent
    config_folder = voc_folder.aq_parent
    cache_view.update_procedure_vocabulary_cache(config_folder, voc_folder)


def update_vocabulary_folder_cache(voc_folder, event):
    portal_urban = api.portal.get_tool('portal_urban')
    cache_view = portal_urban.restrictedTraverse('urban_vocabulary_cache')
    config_folder = voc_folder.aq_parent
    cache_view.update_procedure_vocabulary_cache(config_folder, voc_folder)
