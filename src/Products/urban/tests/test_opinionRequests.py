# -*- coding: utf-8 -*-
import unittest
from zope import event
from Products.Archetypes.event import ObjectInitializedEvent
from Products.Archetypes.event import EditBegunEvent
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL, URBAN_TESTS_LICENCES


class TestOpinionRequest (unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        login(portal, 'urbanmanager')

    def testCreateOrganisationTerm(self):
        tool = self.portal_urban
        foldermakers_folder = tool.buildlicence.foldermakers
        term_id = foldermakers_folder.invokeFactory('OrganisationTerm', id='voodoo', title='Vood00', description='gni')
        term = getattr(foldermakers_folder, term_id, 'NOT FOUND RHAAAAAAAAAAAAAAAAAAAAAA!!!!')
        self.failUnless(term in foldermakers_folder.objectValues())

    def testCreateLinkedUrbanEventType(self):
        #when adding a new OrganisationTerm, a corresponding UrbanEventType 'opinion request' should be created as well
        #and linked to it
        tool = self.portal_urban
        foldermakers_folder = tool.buildlicence.foldermakers
        term_id = foldermakers_folder.invokeFactory('OrganisationTerm', id='voodoo', title='Vood00', description='gni')
        term = getattr(tool.buildlicence.foldermakers, term_id)
        event.notify(ObjectInitializedEvent(term))
        self.failUnless(term.getLinkedOpinionRequestEvent() in tool.buildlicence.urbaneventtypes.objectValues())

    def testCreatedLinkedUrbanEventTypeIsWellOrdered(self):
        #when a linked UrbanEventType 'opinion request' is created, it should be positioned right after
        #the last UrbanEventType 'opinion request' previously added

        tool = self.portal_urban
        foldermakers_folder = tool.buildlicence.foldermakers
        #create an OrganisationTerm and notify it to automatically create a linked UrbanEventType 'opinion request'
        term_id = foldermakers_folder.invokeFactory('OrganisationTerm', id='voodoo', title='Vood00', description='gni')
        term = getattr(tool.buildlicence.foldermakers, term_id)
        event.notify(ObjectInitializedEvent(term))

        urbaneventtypes = tool.buildlicence.urbaneventtypes
        created_urbaneventtype = term.getLinkedOpinionRequestEvent()
        position = urbaneventtypes.getObjectPosition(created_urbaneventtype.id)
        self.failUnless(urbaneventtypes.objectValues()[position - 1].getEventTypeType() == created_urbaneventtype.getEventTypeType())
        if len(urbaneventtypes.objectValues()) > position + 1:
            self.failUnless(urbaneventtypes.objectValues()[position + 1].getEventTypeType() != created_urbaneventtype.getEventTypeType())


class TestOpinionRequestOnLicence (unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.licence = portal.urban.buildlicences.objectValues()[0]
        login(portal, 'urbanmanager')

    def testInquiryWithOpinionRequestIsLinkedToItsUrbanEventOpinionRequest(self):
        #if there is an inquiry with an opinion request and that its corresponding UrbanEventOpinionRequest
        #is added, a link should be created between this inquiry and this UrbanEventOpinionRequest

        licence = self.licence
        UrbanEventOpinionRequest = None
        for content in licence.objectValues():
            if content.portal_type == 'UrbanEventOpinionRequest':
                UrbanEventOpinionRequest = content
                break
        event.notify(EditBegunEvent(UrbanEventOpinionRequest))
        self.failUnless(licence.getLinkedUrbanEventOpinionRequest('belgacom') == UrbanEventOpinionRequest)
