# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def updateKeyEvent(urbanEventType, event):
    catalog = getToolByName(urbanEventType, 'portal_catalog')
    uet_path = urbanEventType.absolute_url_path().split('/')
    licence_path = uet_path[:2]
    licence_path.extend(['urban', '%ss' % uet_path[3]])
    licence_path = '/'.join(licence_path)
    for brain in catalog(path=licence_path, Title=urbanEventType.Title().split('(')[0]):
        urban_event = brain.getObject()
        licence = urban_event.aq_parent
        licence.reindexObject(['last_key_event'])
