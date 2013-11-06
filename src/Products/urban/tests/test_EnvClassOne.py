#-*- coding: utf-8 -*-
from Products.urban.testing import URBAN_TESTS_ENVCLASSONE
from Products.urban.testing import URBAN_TESTS_INTEGRATION
from Products.urban.utils import getLicenceFolder

from plone.testing.z2 import Browser

import unittest
import urllib2


class TestEnvClassOneInstall(unittest.TestCase):

    layer = URBAN_TESTS_INTEGRATION

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

    def test_envclassone_config_folder_is_editable(self):
        msg = 'envclassone config folder is not editable properly'
        self.browserLogin('urbanmanager')
        edit_url = '%s/edit' % self.portal_urban.envclassone.absolute_url()
        self.browser.open(edit_url)
        contents = self.browser.contents
        self.assertTrue("Champs optionnels utilisés" in contents, msg)

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


class TestEnvClassOneInstance(unittest.TestCase):

    layer = URBAN_TESTS_ENVCLASSONE

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        envclassone_folder = self.urban.envclassones
        self.licence = envclassone_folder.objectValues()[0]
        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_envclassone_licence_exists(self):
        self.assertTrue(len(self.urban.envclassones.objectIds()) > 0)

    def test_envclassone_view_is_registered(self):
        msg = 'EnvClassOne view is not registered'
        try:
            self.licence.restrictedTraverse('envclassoneview')
        except AttributeError:
            self.fail(msg=msg)

    def test_envclassone_view(self):
        try:
            self.browser.open(self.licence.absolute_url())
        except urllib2.HTTPError,  e:
            self.fail(msg="Got HTTP response code:" + str(e.code))

    def test_envclassone_has_attribute_areaDescriptionText(self):
        self.assertTrue(hasattr(self.licence, 'areaDescriptionText'))

    def test_envclassone_areaDescription_is_visible(self):
        self.browser.open(self.licence.absolute_url())
        contents = self.browser.contents
        self.assertTrue("areaDescription" in contents)

    def test_envclassone_areaDescription_is_translated(self):
        self.browser.open(self.licence.absolute_url())
        contents = self.browser.contents
        self.assertTrue("Description des lieux et des abords du projet" in contents)

    def test_envclassone_edit(self):
        self.browser.open(self.licence.absolute_url() + '/edit')
        contents = self.browser.contents
        self.assertTrue('Voirie' in contents)
        self.assertTrue('Métadonnées' not in contents)
        self.assertTrue('Données' not in contents)

    def test_envclassone_has_attribute_hasConfidentialDatas(self):
        self.assertTrue(hasattr(self.licence, 'hasConfidentialDatas'))
