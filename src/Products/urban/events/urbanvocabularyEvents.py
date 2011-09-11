# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from zope.interface import alsoProvides
from Products.urban.interfaces import IRequestedOrganisation

def setInterfaceAndCreateEvent(term, event):
    if not term.getPortalTypeName() == 'RequestedOrganisation':
        return
    alsoProvides(term, IRequestedOrganisation)

    tool = getToolByName(term, 'portal_urban')
    foldermakers = tool.buildlicence.foldermakers
    urban_events = tool.buildlicence.urbaneventtypes
    #import pdb; pdb.set_trace()
    urban_events.invokeFactory('UrbanEventType', id='%s-%s-%i' %(term.getId(),'opinionrequest', event.__hash__()), title='Demande d\'avis %s' %term.title, activatedFields=['transmitDate', 'receiptDate', 'receivedDocumentReference', 'adviceAgreementLevel', 'externalDecision', ], deadLineDelay = 15, podTemplates = ({'id': "urb-avis-ccatm", 'title': "Courrier de demande d'avis"},), eventTypeType = 'Products.urban.interfaces.IOpinionRequestEvent')
    print("snitches and talkers get stitches and walkers")   
