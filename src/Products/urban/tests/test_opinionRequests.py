# -*- coding: utf-8 -*-
import unittest
from time import sleep
from zope.component import createObject
from zope import event
from zope.interface import alsoProvides
from Products.Archetypes.event import ObjectInitializedEvent
from Products.Archetypes.event import EditBegunEvent
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL


class TestOpinionRequest (unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        urban = portal.urban
        self.buildLicences = urban.buildlicences
        LICENCE_ID = 'licence1'
        login(portal, 'urbanmanager')
        self.buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        self.buildLicence = getattr(self.buildLicences, LICENCE_ID)
    
    def testCreateOrganisationTerm(self):
        term_id = self.portal_urban.buildlicence.foldermakers.invokeFactory('OrganisationTerm', id='voodoo', title='Vood00', description='gni')
        term = getattr(self.portal_urban.buildlicence.foldermakers, term_id, 'NOT FOUND RHAAAAAAAAAAAAAAAAAAAAAA!!!!')
        self.failUnless(term in self.portal_urban.buildlicence.foldermakers.objectValues())

    def testCreateLinkedUrbanEventType(self):
        #when adding a new OrganisationTerm, a corresponding UrbanEventType 'opinion request' should be created as well 
        #and linked to it
        term_id = self.portal_urban.buildlicence.foldermakers.invokeFactory('OrganisationTerm', id='voodoo', title='Vood00', description='gni')
        term = getattr(self.portal_urban.buildlicence.foldermakers, term_id)
        event.notify(ObjectInitializedEvent(term))
        self.failUnless(term.getLinkedOpinionRequestEvent() in self.portal_urban.buildlicence.urbaneventtypes.objectValues())

    def testCreatedLinkedUrbanEventTypeIsWellOrdered(self):
        #when a linked UrbanEventType 'opinion request' is created, it should be positioned right after
        #the last UrbanEventType 'opinion request' previously added

        #create an OrganisationTerm and notify it to automatically create a linked UrbanEventType 'opinion request'
        term_id = self.portal_urban.buildlicence.foldermakers.invokeFactory('OrganisationTerm', id='voodoo', title='Vood00', description='gni')
        term = getattr(self.portal_urban.buildlicence.foldermakers, term_id)
        event.notify(ObjectInitializedEvent(term))

        urbaneventtypes = self.portal_urban.buildlicence.urbaneventtypes
        created_urbaneventtype = term.getLinkedOpinionRequestEvent()
        position = created_urbaneventtype.getObjectPosition(created_urbaneventtype.id)
        self.failUnless(urbaneventtypes.objectValues()[position-1].getEventTypeType() == created_urbaneventtype.getEventTypeType())
        if len(urbaneventtypes.objectValues()) > position+1:
            self.failUnless(urbaneventtypes.objectValues()[position+1].getEventTypeType() != created_urbaneventtype.getEventTypeType()) 

    def testInquiryWithOpinionRequestIsLinkedToItsUrbanEventOpinionRequest(self):
        #if there is an inquiry with an opinion request and that its corresponding UrbanEventOpinionRequest 
        #is added, a link should be created between this inquiry and this UrbanEventOpinionRequest

        #set an investigation start date to activate the inquiry
        self.buildLicence.setInvestigationStart('18/09/86')
        self.buildLicence.setSolicitOpinionsTo('sncb')
        self.portal_urban.createUrbanEvent(self.buildLicence.UID(), 
                  getattr(self.portal_urban.buildlicence.urbaneventtypes, 'sncb-opinion-request').UID())
        UrbanEventOpinionRequest_sncb = None
        for content in self.buildLicence.objectValues():
            if content.portal_type == 'UrbanEventOpinionRequest':
                UrbanEventOpinionRequest_sncb = content
                break
        event.notify(EditBegunEvent(UrbanEventOpinionRequest_sncb))
        self.failUnless(self.buildLicence.getLinkedUrbanEventOpinionRequest('sncb') == UrbanEventOpinionRequest_sncb)
