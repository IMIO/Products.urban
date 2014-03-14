# -*- coding: utf-8 -*-
import unittest
from zope.component import createObject
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_INTEGRATION


class TestEventDateEvents(unittest.TestCase):
    layer = URBAN_TESTS_PROFILE_INTEGRATION

    def setUp(self):
        portal = self.layer['portal']
        urban = portal.urban
        buildLicences = urban.buildlicences
        LICENCE_ID = 'licence1'
        login(portal, 'urbaneditor')
        buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        self.buildLicence = getattr(buildLicences, LICENCE_ID)

    def testCreationDate(self):
        event = createObject('UrbanEvent', self.buildLicence, 'depot-de-la-demande')
        self.assertEqual(event.created(), event.getEventDate())
