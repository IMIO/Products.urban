# -*- coding: utf-8 -*-

from plone import api

from Products.Five import BrowserView

from Products.urban.interfaces import ICODT_UniqueLicence

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class UpdateCollegeEventDoneTasks(BrowserView):
    """
    Touch incomplete unique licences once a day to trigger
    incompletion tasks.
    """

    def __call__(self):
        """ """

        catalog = api.portal.get_tool('portal_catalog')

        college_events_brains = catalog(
            object_provides=ICODT_UniqueLicence.__identifier__,
            review_state='incomplete'
        )
        for brain in college_events_brains:
            uniquelicence = brain.getObject()
            notify(ObjectModifiedEvent(uniquelicence))
