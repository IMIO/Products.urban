#-*- coding: utf-8 -*-
from Products.urban.testing import URBAN_TESTS_PROFILE_INTEGRATION
from Products.urban.tests.helpers import BrowserTestCase
from Products.urban.config import ORDERED_URBAN_TYPES
from Products.urban import utils
from plone.testing.z2 import Browser


class TestConfig(BrowserTestCase):

    layer = URBAN_TESTS_PROFILE_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_urban = self.portal.portal_urban
        self.urban = self.portal.urban
        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def test_urban_root_view_is_default_view(self):
        self.browser.open(self.urban.absolute_url())
        self.assertTrue('content-shortcuts' in self.browser.contents)
        for licencetype in ORDERED_URBAN_TYPES:
            folder_url = utils.getLicenceFolder(licencetype).absolute_url()
            self.assertTrue(folder_url in self.browser.contents)

    def test_site_view_redirects_to_urban_root(self):
        self.assertTrue(self.portal.layout == 'redirectto_urban_root_view')
