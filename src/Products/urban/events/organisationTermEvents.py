# -*- coding: utf-8 -*-
from Products.urban.utils import moveElementAfter

def createLinkedOpinionRequest(term, event):
    parentfolder = term.aq_parent
    urban_event_types = parentfolder.urbaneventtypes
    new_id = '%s-%s' %(term.getId(),'opinion-request')
    if new_id in urban_event_types.objectIds():
        return
    urbaneventtype_id = urban_event_types.invokeFactory('UrbanEventType', id=new_id, title='Demande d\'avis (%s)' %term.title, activatedFields=['transmitDate', 'receiptDate', 'receivedDocumentReference', 'adviceAgreementLevel', 'externalDecision', ], deadLineDelay = 15, TALCondition = "python: here.mayAddOpinionRequestEvent('%s')" %term.getId(), eventTypeType = 'Products.urban.interfaces.IOpinionRequestEvent')
    term.setLinkedOpinionRequestEvent(getattr(urban_event_types, new_id))
    urban_event_type = getattr(urban_event_types, urbaneventtype_id)
    moveElementAfter(urban_event_type, urban_event_types, 'eventTypeType', 'Products.urban.interfaces.IOpinionRequestEvent')
