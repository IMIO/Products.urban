# -*- coding: utf-8 -*-
import unittest2 as unittest
from DateTime import DateTime
from zope.component import createObject
from zope.component.interface import interfaceToName
from plone.app.testing import quickInstallProduct, login
from plone.app.testing import setRoles
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.app.testing.interfaces import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from Products.urban.interfaces import (IUrbanEventType, IAcknowledgmentEvent,
        IOpinionRequestEvent, IInquiryEvent)
from Products.urban.testing import URBAN_INTEGRATION
from Products.urban.testing import URBAN_TESTS_PROFILE_INTEGRATION


class TestInstall(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_INTEGRATION

    def testReinstall(self):
        portal = self.layer['portal']
        quickInstallProduct(portal, 'Products.urban')
        quickInstallProduct(portal, 'Products.urban')

    def testEventTypesCreated(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        login(portal, 'urbaneditor')
        interfaceName = interfaceToName(portal, IUrbanEventType)
        eventTypes = catalog(object_provides=interfaceName,
                             sort_on='sortable_title')
        self.failUnless(len(eventTypes) > 0)

    def testEventWithoutEventTypeType(self):
        portal = self.layer['portal']
        urban = portal.urban
        buildLicences = urban.buildlicences
        LICENCE_ID = 'licence1'
        login(portal, 'urbaneditor')
        buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        licence = getattr(buildLicences, LICENCE_ID)
        #'avis-etude-incidence' can only be added if it is defined on the licence
        licence.setImpactStudy(True)
        createObject('UrbanEvent', 'avis-etude-incidence', licence)

    def testAcknowledgmentSearchByInterface(self):
        portal = self.layer['portal']
        urbanTool = getToolByName(portal, 'portal_urban')
        urban = portal.urban
        buildLicences = urban.buildlicences
        urbanConfig = urbanTool.buildlicence
        LICENCE_ID = 'licence1'
        login(portal, 'urbaneditor')
        buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        licence = getattr(buildLicences, LICENCE_ID)
        eventTypes = urbanConfig.urbaneventtypes
        self.assertEqual(len(licence.objectValues('UrbanEvent')), 0)
        urbanEvent = createObject('UrbanEvent', 'accuse-de-reception', licence)
        self.assertEqual(len(licence.objectValues('UrbanEvent')), 1)
        self.failUnless(IAcknowledgmentEvent.providedBy(urbanEvent))
        catalog = getToolByName(portal, 'portal_catalog')
        interfaceName = interfaceToName(portal, IAcknowledgmentEvent)
        eventTypes = catalog(object_provides=interfaceName,
                             sort_on='sortable_title')
        self.assertEqual(len(eventTypes), 1)

    def testInquirySearchByInterface(self):
        portal = self.layer['portal']
        urban = portal.urban
        buildLicences = urban.buildlicences
        LICENCE_ID = 'licence1'
        login(portal, 'urbaneditor')
        buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        licence = getattr(buildLicences, LICENCE_ID)
        self.assertEqual(len(licence.objectValues('UrbanEvent')), 0)
        #we can add an 'enquete-publique' UrbanEventInquiry if an Inquiry is defined
        #so define an investigationStart date on the licence, this correspond to a first
        #available inquiry
        date = DateTime()
        licence.setInvestigationStart(date)
        urbanEvent = createObject('UrbanEventInquiry', 'enquete-publique', licence)
        self.failUnless(IInquiryEvent.providedBy(urbanEvent))

    def testOpinionRequestSearchByInterface(self):
        portal = self.layer['portal']
        urban = portal.urban
        buildLicences = urban.buildlicences
        LICENCE_ID = 'licence1'
        login(portal, 'urbaneditor')
        buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        licence = getattr(buildLicences, LICENCE_ID)
        self.assertEqual(len(licence.objectValues('UrbanEvent')), 0)
        #we can add a 'demande-avis-swde' UrbanEvent if 'swde' is selected
        #in the list solicitOpinionsTo
        opinionsToSolicit = licence.getSolicitOpinionsTo()
        extraOpinion = ('swde',)
        licence.setSolicitOpinionsTo(opinionsToSolicit+extraOpinion)
        urbanEvent = createObject('UrbanEvent', 'demande-avis-swde', licence)
        self.failUnless(IOpinionRequestEvent.providedBy(urbanEvent))

    def testAcknowledgmentEventTypeType(self):
        portal = self.layer['portal']
        urban = getToolByName(portal, 'portal_urban')
        eventTypes = urban.buildlicence.urbaneventtypes
        accuse = getattr(eventTypes, 'accuse-de-reception')
        eventTypeType = accuse.getEventTypeType()
        self.assertEqual(eventTypeType,
            'Products.urban.interfaces.IAcknowledgmentEvent')


class TestContact(unittest.TestCase):

    layer = URBAN_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal_urban = self.portal.portal_urban
        self.buildlicence = self.portal_urban.buildlicence
        self.foldermanagers = self.buildlicence.foldermanagers
        self.folderBuildLicences = self.portal.urban.buildlicences

    def test_getSignaleticIsString(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robin')
        agent.setPersonTitle(u'mister')
        self.failUnless(isinstance(agent.getSignaletic(), str))
        self.failUnless(isinstance(agent.getSignaletic(withaddress=True),
            str))
        self.failUnless(isinstance(agent.getSignaletic(linebyline=True),
            str))
        self.failUnless(isinstance(agent.getSignaletic(withaddress=True,
            linebyline=True), str))

    def test_name1GetSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robiné')
        agent.setName2(u'Hood')
        agent.setPersonTitle(u'mister')
        agent.setNumber(u'1')
        agent.setCity(u'Sherwood')
        agent.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'fr')
        self.assertEquals(agent.getSignaletic(),
            u'Monsieur Robiné Hood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(linebyline=True),
            u'<p>Monsieur Robiné Hood</p>'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True),
            u'Monsieur Robiné Hood demeurant 1, Sherwood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True,
            linebyline=True),
            u'<p>Monsieur Robiné Hood<br />1, <br /> Sherwood</p>'
            .encode('utf8'))

    def test_name2GetSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robin')
        agent.setName2(u'Hoodé')
        agent.setPersonTitle(u'mister')
        agent.setNumber(u'1')
        agent.setCity(u'Sherwood')
        agent.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'fr')
        self.assertEquals(agent.getSignaletic(),
            u'Monsieur Robin Hoodé'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(linebyline=True),
            u'<p>Monsieur Robin Hoodé</p>'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True),
            u'Monsieur Robin Hoodé demeurant 1, Sherwood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True,
            linebyline=True),
            u'<p>Monsieur Robin Hoodé<br />1, <br /> Sherwood</p>'
            .encode('utf8'))

    def test_personTitleGetSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robin')
        agent.setName2(u'Hood')
        agent.setPersonTitle(u'master')
        agent.setNumber(u'1')
        agent.setCity(u'Sherwood')
        agent.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'fr')
        self.assertEquals(agent.getSignaletic(),
            u'Maître Robin Hood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(linebyline=True),
            u'<p>Maître Robin Hood</p>'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True),
            u'Maître Robin Hood demeurant 1, Sherwood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True,
            linebyline=True),
            u'<p>Maître Robin Hood<br />1, <br /> Sherwood</p>'.encode('utf8'))

    def test_cityGetSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robin')
        agent.setName2(u'Hood')
        agent.setPersonTitle(u'mister')
        agent.setNumber(u'1')
        agent.setCity(u'Sherwoodé')
        agent.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'fr')
        self.assertEquals(agent.getSignaletic(),
            u'Monsieur Robin Hood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(linebyline=True),
            u'<p>Monsieur Robin Hood</p>'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True),
            u'Monsieur Robin Hood demeurant 1, Sherwoodé'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True,
            linebyline=True),
            u'<p>Monsieur Robin Hood<br />1, <br /> Sherwoodé</p>'
            .encode('utf8'))

    def test_getApplicantsSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.folderBuildLicences.invokeFactory('BuildLicence', 'buildLicence')
        buildLicence = self.folderBuildLicences.buildLicence
        buildLicence.invokeFactory('Applicant', 'applicant')
        applicant = buildLicence.applicant
        applicant.setName1(u'Robiné')
        applicant.setName2(u'Hoodé')
        applicant.setPersonTitle(u'master')
        applicant.setNumber(u'1')
        applicant.setCity(u'Sherwoodé')
        buildLicence.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'fr')

        self.assertEquals(buildLicence.getApplicantsSignaletic(),
            u'Maître Robiné Hoodé'.encode('utf8'))
        self.assertEquals(buildLicence.getApplicantsSignaletic(
            withaddress=True),
            u'Maître Robiné Hoodé demeurant 1, Sherwoodé'.encode('utf8'))
