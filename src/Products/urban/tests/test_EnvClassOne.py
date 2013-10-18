#-*- coding: utf-8 -*-
import unittest
from Products.urban.testing import URBAN_TESTS_PROFILE_INTEGRATION


class TestConfig(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_INTEGRATION 

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_urban = self.portal.portal_urban

    def test_EnvCLassOne_config_folder_exists(self):
        msg = 'envclassone config folder not created'
        self.assertTrue('envclassone' in self.portal_urban.objectIds(), msg)
        envclassone = self.portal_urban.envclassone
        from Products.urban.LicenceConfig import LicenceConfig
        self.assertTrue(isinstance(envclassone, LicenceConfig))
