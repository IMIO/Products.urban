# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def setDefaultLinkedInquiry(opinionRequest, event):
    if opinionRequest.checkCreationFlag():
        opinionRequest.setLinkedInquiry(opinionRequest.aq_inner.aq_parent.getInquiries()[-1])

def setDefaultRequestedOrganisation(opinionRequest, event):
    if opinionRequest.checkCreationFlag():
        tool = getToolByName(opinionRequest, 'portal_urban')
        foldermakers = tool.buildlicence.foldermakers
        for term in foldermakers.objectValues():
            if term.getLinkedOpinionRequestEvent() == opinionRequest.getUrbaneventtypes():
                opinionRequest.setRequestedOrganisation(term.id)
                return
        opinionRequest.setRequestedOrganisation('NO VALUE FOUND')
