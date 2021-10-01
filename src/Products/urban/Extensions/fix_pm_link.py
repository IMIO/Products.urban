# -*- coding: utf-8 -*-

from plone import api
from Products.urban.interfaces import ISimpleCollegeEvent
from Products.urban.interfaces import ICollegeEvent
from zope.annotation import interfaces


def fix_pm_link():
    portal = api.portal.get()
    request = portal.REQUEST
    context = request['PARENTS'][0]
    if ISimpleCollegeEvent.providedBy(context) or ICollegeEvent.providedBy(context):
        interfaces.IAnnotations(context)['imio.pm.wsclient-sent_to'] = ['meeting-config-college']

