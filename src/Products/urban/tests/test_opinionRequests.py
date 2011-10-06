# -*- coding: utf-8 -*-
import unittest
from time import sleep
from zope.component import createObject
from zope import event
from Products.Archetypes.event import ObjectInitializedEvent
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
        #when adding a new OrganisationTerm, a corresponding UrbanEvent opinion request should be created as well 
        #and linked to it
        term_id = self.portal_urban.buildlicence.foldermakers.invokeFactory('OrganisationTerm', id='voodoo', title='Vood00', description='gni')
        term = getattr(self.portal_urban.buildlicence.foldermakers, term_id)
        event.notify(ObjectInitializedEvent(term))
        self.failUnless(term.getLinkedOpinionRequestEvent() in self.portal_urban.buildlicence.urbaneventtypes.objectValues()) 
