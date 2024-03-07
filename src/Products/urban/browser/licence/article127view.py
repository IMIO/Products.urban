# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.urban.browser.licence.licenceview import LicenceView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _


class Article127View(LicenceView):
    """
    This manage the view of Article127
    """

    def __init__(self, context, request):
        super(Article127View, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets on licences
        self.request.set("disable_plone.rightcolumn", 1)
        self.request.set("disable_plone.leftcolumn", 1)
        plone_utils = getToolByName(context, "plone_utils")
        if not self.context.getApplicants():
            plone_utils.addPortalMessage(_("warning_add_an_applicant"), type="warning")

    def getInquiriesForDisplay(self):
        """
        Returns the inquiries to display on the article127_view
        """
        context = aq_inner(self.context)
        inquiries = context.getInquiries()
        if not inquiries:
            # we want to display at least the informations about the inquiry
            # defined on the licence even if no data have been entered
            inquiries.append(context)
        return inquiries

    def getMacroViewName(self):
        return "article127-macros"

    def getPebFields(self):
        return self.getSchemataFields(schemata="urban_peb")
