# -*- coding: utf-8 -*-
import unittest2 as unittest
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
        urbanTool = getToolByName(portal, 'portal_urban')
        urban = portal.urban
        buildLicences = urban.buildlicences
        urbanConfig = urbanTool.buildlicence
        LICENCE_ID = 'licence1'
        login(portal, 'urbaneditor')
        buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        licence = getattr(buildLicences, LICENCE_ID)
        eventTypes = urbanConfig.urbaneventtypes
        etudeIncidence = getattr(eventTypes, 'avis-etude-incidence')
        urbanEventId = urbanTool.generateUniqueId('UrbanEvent')
        licence.invokeFactory("UrbanEvent",
                              id=urbanEventId,
                              title=etudeIncidence.Title(),
                              urbaneventtypes=(etudeIncidence,))
        urbanEvent = getattr(licence, urbanEventId)
        urbanEvent._at_rename_after_creation = False
        urbanEvent.processForm()

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
        accuse = getattr(eventTypes, 'accuse-de-reception')
        urbanEventId = urbanTool.generateUniqueId('UrbanEvent')
        self.assertEqual(len(licence.objectValues('UrbanEvent')), 0)
        licence.invokeFactory("UrbanEvent",
                              id=urbanEventId,
                              title=accuse.Title(),
                              urbaneventtypes=(accuse,))
        urbanEvent = getattr(licence, urbanEventId)
        urbanEvent._at_rename_after_creation = False
        urbanEvent.processForm()
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

    def testSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory('FolderManager', 'agent')
        agent = self.foldermanagers.agent
        agent.setName1(u'Robin')
        agent.setPersonTitle(u'mister')
        self.failUnless(isinstance(agent.getSignaletic(), unicode))
        agent.setName1('Robin')
        self.failUnless(isinstance(agent.getSignaletic(), unicode))
