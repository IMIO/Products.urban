# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def setDefaultLinkedInquiry(opinionRequest, event):
    if opinionRequest.checkCreationFlag():
        opinionRequest.setLinkedInquiry(opinionRequest.aq_inner.aq_parent.getInquiries()[-1])
