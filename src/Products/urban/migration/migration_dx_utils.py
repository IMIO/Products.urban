# -*- coding: utf-8 -*-
from datetime import datetime
from plone import api


def purge_obsolete_content(portal_type=None):

    catalog = api.portal.get_tool('portal_catalog')
    items = [brain.getObject() for brain in catalog(portal_type=portal_type)]
    print("Found {} items to be purged".format(len(items)))
    count = 0
    for obj in items:
        count += 1
        print("Deleting: {} {}".format(obj.absolute_url(),str(obj.created())))
        obj.aq_parent.manage_delObjects([obj.getId()])
