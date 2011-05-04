# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component.interface import interfaceToName
from plone.app.testing import quickInstallProduct, login
from Products.CMFCore.utils import getToolByName
from Products.urban.interfaces import IUrbanEventType
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
