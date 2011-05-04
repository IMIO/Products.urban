# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component.interface import interfaceToName
from plone.app.testing import quickInstallProduct, login
from Products.CMFCore.utils import getToolByName
from Products.urban.interfaces import IUrbanEventType, IAcknoledgment
from Products.urban.testing import URBAN_WITH_PLONE


class TestInstall(unittest.TestCase):

    layer = URBAN_WITH_PLONE

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

    def testAcknoledgmentSearchByInterface(self):
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
        self.failUnless(IAcknoledgment.providedBy(urbanEvent))
        catalog = getToolByName(portal, 'portal_catalog')
        interfaceName = interfaceToName(portal, IAcknoledgment)
        eventTypes = catalog(object_provides=interfaceName,
                             sort_on='sortable_title')
        self.assertEqual(len(eventTypes), 1)

    def testAcknoledgmentEventTypeType(self):
        portal = self.layer['portal']
        urban = getToolByName(portal, 'portal_urban')
        eventTypes = urban.buildlicence.urbaneventtypes
        accuse = getattr(eventTypes, 'accuse-de-reception')
        eventTypeType = accuse.getEventTypeType()
        self.assertEqual(eventTypeType, 'Products.urban.interfaces.IAcknoledgment')
