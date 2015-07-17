# -*- coding: utf-8 -*-
import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from Products.urban.interfaces import (IUrbanEventType, IAcknowledgmentEvent, IOpinionRequestEvent, IInquiryEvent)
from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.testing import URBAN_TESTS_LICENCES

from plone import api
from plone.app.testing import quickInstallProduct, login
from plone.app.testing import setRoles
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.app.testing.interfaces import TEST_USER_ID

from zope.component.interface import interfaceToName


class TestInstall(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        login(portal, 'urbaneditor')
        self.licence = portal.urban.buildlicences.objectValues()[-1]

    def testReinstall(self):
        quickInstallProduct(self.portal, 'Products.urban')
        quickInstallProduct(self.portal, 'Products.urban')

    def testEventTypesCreated(self):
        catalog = getToolByName(self.portal, 'portal_catalog')
        interfaceName = interfaceToName(self.portal, IUrbanEventType)
        eventTypes = catalog(object_provides=interfaceName, sort_on='sortable_title')
        self.failUnless(len(eventTypes) > 0)

    def testEventWithoutEventTypeType(self):
        #'avis-etude-incidence' can only be added if it is defined on the licence
        self.licence.setImpactStudy(True)
        self.licence.createUrbanEvent('avis-etude-incidence')

    def testAcknowledgmentSearchByInterface(self):
        urbanTool = getToolByName(self.portal, 'portal_urban')
        urbanConfig = urbanTool.buildlicence
        licence = self.licence
        eventTypes = urbanConfig.urbaneventtypes
        # there is already 10 events created on the licence
        self.assertEqual(len(licence.objectValues('UrbanEvent')), 10)
        urbanEvent = licence.createUrbanEvent('accuse-de-reception')
        self.assertEqual(len(licence.objectValues('UrbanEvent')), 11)
        self.failUnless(IAcknowledgmentEvent.providedBy(urbanEvent))
        catalog = getToolByName(self.portal, 'portal_catalog')
        interfaceName = interfaceToName(self.portal, IAcknowledgmentEvent)
        eventTypes = catalog(object_provides=interfaceName,
                             sort_on='sortable_title')
        # == 2 because there was an existing event 'accusé de réception' on the
        # licence
        self.assertEqual(len(eventTypes), 2)

    def testInquirySearchByInterface(self):
        licence = self.licence
        self.assertEqual(len(licence.objectValues('UrbanEvent')), 10)
        # no need to create an inquiry event, its already existing in the test
        #licence
        urbanEvent = licence.objectValues('UrbanEventInquiry')[0]
        self.failUnless(IInquiryEvent.providedBy(urbanEvent))

    def testOpinionRequestMarkerInterface(self):
        licence = self.licence
        self.assertEqual(len(licence.objectValues('UrbanEvent')), 10)
        # no need to create an opinion request event, its already existing in
        # the test licence
        urbanEvent = licence.objectValues('UrbanEventOpinionRequest')[0]
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

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal_urban = self.portal.portal_urban
        self.buildlicence = self.portal_urban.buildlicence
        self.foldermanagers = self.buildlicence.foldermanagers
        self.folderBuildLicences = self.portal.urban.buildlicences
        #set language to 'fr' as we do some translations above
        ltool = self.portal.portal_languages
        defaultLanguage = 'fr'
        supportedLanguages = ['en', 'fr']
        ltool.manage_setLanguageSettings(defaultLanguage, supportedLanguages, setUseCombinedLanguageCodes=False)
        #this needs to be done in tests for the language to be taken into account...
        ltool.setLanguageBindings()

    def test_getSignaleticIsString(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robin')
        agent.setPersonTitle(u'master')
        self.failUnless(isinstance(agent.getSignaletic(), str))
        self.failUnless(isinstance(agent.getSignaletic(withaddress=True), str))
        self.failUnless(isinstance(agent.getSignaletic(linebyline=True), str))
        self.failUnless(isinstance(agent.getSignaletic(withaddress=True, linebyline=True), str))

    def test_name1GetSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robiné')
        agent.setName2(u'Hood')
        agent.setPersonTitle(u'master')
        agent.setNumber(u'1')
        agent.setCity(u'Sherwood')
        agent.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'fr')
        self.assertEquals(agent.getSignaletic(), u'Maître Robiné Hood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(linebyline=True),
                          u'<p>Maître Robiné Hood</p>'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True),
                          u'Maître Robiné Hood domicilié à 1, Sherwood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True, linebyline=True),
                          u'<p>Maître Robiné Hood<br />1, <br /> Sherwood</p>'.encode('utf8'))

    def test_name2GetSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robin')
        agent.setName2(u'Hoodé')
        agent.setPersonTitle(u'master')
        agent.setNumber(u'1')
        agent.setCity(u'Sherwood')
        agent.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'fr')
        self.assertEquals(agent.getSignaletic(), u'Maître Robin Hoodé'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(linebyline=True),
                          u'<p>Maître Robin Hoodé</p>'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True),
                          u'Maître Robin Hoodé domicilié à 1, Sherwood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True, linebyline=True),
                          u'<p>Maître Robin Hoodé<br />1, <br /> Sherwood</p>'.encode('utf8'))

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
        self.assertEquals(agent.getSignaletic(), u'Maître Robin Hood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(linebyline=True),
                          u'<p>Maître Robin Hood</p>'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True),
                          u'Maître Robin Hood domicilié à 1, Sherwood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True, linebyline=True),
                          u'<p>Maître Robin Hood<br />1, <br /> Sherwood</p>'.encode('utf8'))

    def test_cityGetSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robin')
        agent.setName2(u'Hood')
        agent.setPersonTitle(u'master')
        agent.setNumber(u'1')
        agent.setCity(u'Sherwoodé')
        agent.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'fr')
        self.assertEquals(agent.getSignaletic(), u'Maître Robin Hood'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(linebyline=True),
                          u'<p>Maître Robin Hood</p>'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True),
                          u'Maître Robin Hood domicilié à 1, Sherwoodé'.encode('utf8'))
        self.assertEquals(agent.getSignaletic(withaddress=True, linebyline=True),
                          u'<p>Maître Robin Hood<br />1, <br /> Sherwoodé</p>'.encode('utf8'))

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
        self.assertEquals(buildLicence.getApplicantsSignaletic(), u'Maître Robiné Hoodé'.encode('utf8'))
        self.assertEquals(buildLicence.getApplicantsSignaletic(withaddress=True),
                          u'Maître Robiné Hoodé domicilié à 1, Sherwoodé'.encode('utf8'))
        api.content.delete(buildLicence)
