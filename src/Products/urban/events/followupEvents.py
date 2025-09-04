# -*- coding: utf-8 -*-


def setLinkedReport(urban_event, event):
    """
    After creation, link me to my InspectionReportEvent
    """
    if urban_event.portal_type != "UrbanEventFollowUp":
        return
    inspection = urban_event.aq_parent
    if not hasattr(inspection, "getLastReportEvent"):
        # This can happen during the creation of the content
        return
    last_report = inspection.getLastReportEvent()
    if not last_report:
        return
    urban_event.setLinkedReport(last_report)
