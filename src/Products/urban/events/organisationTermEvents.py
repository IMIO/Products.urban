# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def createLinkedOpinionRequest(term, event):
    tool = getToolByName(term, 'portal_urban')
    foldermakers = tool.buildlicence.foldermakers
    urban_events = tool.buildlicence.urbaneventtypes
    new_id = '%s-%s' %(term.getId(),'opinion-request')
    if new_id in urban_events.objectIds():
        return
    urban_events.invokeFactory('UrbanEventType', id=new_id, title='Demande d\'avis (%s)' %term.title, activatedFields=['transmitDate', 'receiptDate', 'receivedDocumentReference', 'adviceAgreementLevel', 'externalDecision', ], deadLineDelay = 15, TALCondition = "python: here.mayAddOpinionRequestEvent('%s')" %term.getId(), eventTypeType = 'Products.urban.interfaces.IOpinionRequestEvent')
    term.setLinkedOpinionRequestEvent(getattr(urban_events, new_id))
