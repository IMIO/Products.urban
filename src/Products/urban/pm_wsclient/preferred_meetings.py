# -*- coding: utf-8 -*-

from imio.pm.wsclient.interfaces import IPreferredMeetings

from plone import api

from zope.interface import implements


class UrbanPreferredMeetings(object):
    """ """

    implements(IPreferredMeetings)

    def __init__(self, context, possible_meetings):
        self.urban_event = context
        self.licence = context.aq_parent
        self.possible_meetings = possible_meetings

    def get(self):
        """ """
        catalog = api.portal.get_tool("portal_catalog")
        licence_brain = catalog(UID=self.licence.UID())[0]
        licence_duedate = licence_brain.licence_final_duedate
        for possible_meeting in self.possible_meetings:
            meeting_date = possible_meeting["date"].date()
            date_display = meeting_date.strftime("%d/%m/%Y")
            if str(meeting_date) >= str(licence_duedate):
                licence_duedate_display = licence_duedate.strftime("%d/%m/%Y")
                date_display = (
                    u"{} !!! Séance après échéance du dossier: {} !!!".format(
                        date_display, licence_duedate_display
                    )
                )
            possible_meeting["date"] = date_display
        return self.possible_meetings
