# -*- coding: utf-8 -*-

from plone import api

from Products.Five import BrowserView

import transaction


class InquiryRadiusSearch(BrowserView):
    """
    Browser view to call with cron to automatically
    execute all inquiry radius registered.
    """

    def __call__(self):
        """
        """
        catalog = api.portal.get_tool('portal_catalog')
        planned_inquiries = api.portal.get_registry_record(
            'Products.urban.interfaces.IAsyncInquiryRadius.inquiries_to_do'
        ) or {}

        for inquiry_UID in planned_inquiries.keys():
            radius = planned_inquiries.pop(inquiry_UID)
            inquiry = catalog.unrestrictedSearchResults(UID=inquiry_UID)[0].getObject()
            inquiry_view = inquiry.restrictedTraverse('@@urbaneventinquiryview')
            inquiry_view.getInvestigationPOs(radius=radius, force=True)
            transaction.commit()
