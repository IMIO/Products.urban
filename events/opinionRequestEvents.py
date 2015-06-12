# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def setDefaultLinkedInquiry(opinionRequest, event):
    if opinionRequest.checkCreationFlag():
        licence = opinionRequest.aq_inner.aq_parent
        inquiry = licence.getInquiries() and licence.getInquiries()[-1] or licence
        opinionRequest.setLinkedInquiry(inquiry)
