# -*- coding: utf-8 -*-
import unittest
from zope.component import createObject


class TestEventDateEvents(unittest.TestCase):
    # layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        pass
        # portal = self.layer['portal']
        # urban = portal.urban
        # buildLicences = urban.buildlicences
        # LICENCE_ID = 'licence1'
        # default_user = self.layer.default_user
        # login(portal, default_user)
        # buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        # self.buildLicence = getattr(buildLicences, LICENCE_ID)

    def testfoo(self):
        self.assertTrue(True)
        # event = createObject('UrbanEvent', self.buildLicence, 'depot-de-la-demande')
        # self.assertEqual(event.created(), event.getEventDate())
