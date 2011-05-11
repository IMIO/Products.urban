# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component import createObject
from zope.component.interface import interfaceToName
from plone.app.testing import quickInstallProduct, login
from plone.app.testing import setRoles
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.app.testing.interfaces import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from Products.urban.interfaces import IUrbanEventType, IAcknowledgment
from Products.urban.testing import URBAN_INTEGRATION
from Products.urban.testing import URBAN_TESTS_PROFILE_INTEGRATION


class TestInstall(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_INTEGRATION

    def testReinstall(self):
        portal = self.layer['portal']
        quickInstallProduct(portal, 'Products.urban')
        quickInstallProduct(portal, 'Products.urban')

    def testPresentEventTypes(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        login(portal, 'urbaneditor')
        interfaceName = interfaceToName(portal, IUrbanEventType)
        eventTypes = catalog(object_provides=interfaceName,
                             sort_on='sortable_title')
        self.failUnless(len(eventTypes) > 0)
        eventType = eventTypes[0]
        self.assertEqual(eventType.getId, 'accuse-de-reception')

    def testEventWithoutEventTypeType(self):
        portal = self.layer['portal']
        urban = portal.urban
        buildLicences = urban.buildlicences
        LICENCE_ID = 'licence1'
        login(portal, 'urbaneditor')
        buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        licence = getattr(buildLicences, LICENCE_ID)
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
        self.failUnless(IAcknowledgment.providedBy(urbanEvent))
        catalog = getToolByName(portal, 'portal_catalog')
        interfaceName = interfaceToName(portal, IAcknowledgment)
        eventTypes = catalog(object_provides=interfaceName,
                             sort_on='sortable_title')
        self.assertEqual(len(eventTypes), 1)

    def testAcknowledgmentEventTypeType(self):
        portal = self.layer['portal']
        urban = getToolByName(portal, 'portal_urban')
        eventTypes = urban.buildlicence.urbaneventtypes
        accuse = getattr(eventTypes, 'accuse-de-reception')
        eventTypeType = accuse.getEventTypeType()
        self.assertEqual(eventTypeType,
            'Products.urban.interfaces.IAcknowledgment')


class TestContact(unittest.TestCase):

    layer = URBAN_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal_urban = self.portal.portal_urban
        self.buildlicence = self.portal_urban.buildlicence
        self.foldermanagers = self.buildlicence.foldermanagers

    def test_getSignaleticIsString(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robin')
        agent.setPersonTitle(u'mister')
        self.failUnless(isinstance(agent.getSignaletic(), str))
        self.failUnless(isinstance(agent.getSignaletic(withaddress=True), str))
        self.failUnless(isinstance(agent.getSignaletic(linebyline=True), str))
        self.failUnless(isinstance(agent.getSignaletic(withaddress=True,
            linebyline=True), str))

    def test_getSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robin')
        agent.setName2(u'Hood')
        agent.setPersonTitle(u'mister')
        agent.setNumber(u'1')
        agent.setCity(u'Sherwood')
        agent.REQUEST.set('HTTP_ACCEPT_LANGUAGE', 'fr')
        self.assertEquals(agent.getSignaletic(), 'Monsieur Robin Hood')
        self.assertEquals(agent.getSignaletic(linebyline=True),
            '<p>Monsieur Robin Hood</p>')
        self.assertEquals(agent.getSignaletic(withaddress=True),
            'Monsieur Robin Hood demeurant 1, Sherwood')
        self.assertEquals(agent.getSignaletic(withaddress=True,
            linebyline=True),
            '<p>Monsieur Robin Hood<br />1, <br /> Sherwood</p>')
