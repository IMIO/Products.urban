#-*- coding: utf-8 -*-
import unittest
from Products.urban.testing import URBAN_TESTS_PROFILE_INTEGRATION
from Products.urban.utils import getLicenceFolder
from plone.testing.z2 import Browser


class TestEnvClassOne(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban
        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_envclassone_config_folder_exists(self):
        msg = 'envclassone config folder not created'
        self.assertTrue('envclassone' in self.portal_urban.objectIds(), msg)
        envclassone = self.portal_urban.envclassone
        from Products.urban.LicenceConfig import LicenceConfig
        self.assertTrue(isinstance(envclassone, LicenceConfig))

    def test_envclassone_config_folder_is_visible(self):
        msg = 'envclassone config folder is not visible in urban config'
        self.browser.open(self.portal_urban.absolute_url())
        contents = self.browser.contents
        self.assertTrue("Permis d'environnement classe 1" in contents, msg)

    def test_envclassone_folder_exist(self):
        msg = 'envclassones folder not created'
        self.assertTrue('envclassones' in self.urban.objectIds(), msg)

    def test_envclassone_addable_types(self):
        msg = 'cannot create EnvClassOne in licence folder'
        addable_types = self.urban.envclassones.immediatelyAddableTypes
        self.assertTrue('EnvClassOne' in addable_types, msg)
        msg = 'can create an other content type in licence folder'
        self.assertEqual(len(addable_types), 1, msg)

    def test_envclassone_licence_folder_link_in_urban_default_view(self):
        self.browser.open(self.urban.absolute_url())
        folder_url = getLicenceFolder(self.urban, 'EnvClassOne').absolute_url()
        link = self.browser.getLink(url=folder_url)
        self.assertEqual(link.text, "Permis d'environnement classe 1")
        link.click()
        contents = self.browser.contents
        self.assertTrue("Ajouter un permis d'environnement classe 1" in contents)

    def test_add_envclassone_in_urban_default_view(self):
        self.browser.open(self.urban.absolute_url())
        contents = self.browser.contents
        self.assertTrue("create-EnvClassOne-link" in contents)
        link = self.browser.getLink(id="create-EnvClassOne-link")
        link.click()
        contents = self.browser.contents
        self.assertTrue("Ajouter Permis d'environnement classe 1" in contents)
