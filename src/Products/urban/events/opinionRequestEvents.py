# -*- coding: utf-8 -*-

from Products.urban.interfaces import ICODT_Inquiry

def setDefaultLinkedInquiry(opinionRequest, event):
    if opinionRequest.checkCreationFlag():
        licence = opinionRequest.aq_inner.aq_parent
        if ICODT_Inquiry.providedBy(licence):
            inquiries = licence.getInquiriesAndAnnouncements()
        else:
            inquiries = licence.getInquiries()
        inquiry = inquiries and inquiries[-1] or licence
        opinionRequest.setLinkedInquiry(inquiry)
