# -*- coding: utf-8 -*-

from plone import api


def update_tasks():
    site = api.portal.get()    
    site.restrictedTraverse('@@update_licences_open_tasks')()
