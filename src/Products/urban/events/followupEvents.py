# -*- coding: utf-8 -*-


def setLinkedReport(urban_event, event):
    """
    After creation, link me to my InspectionReportEvent
    """
    if urban_event.portal_type != "UrbanEventFollowUp":
        return
    last_report = urban_event.aq_parent.getLastReportEvent()
    urban_event.setLinkedReport(last_report)
