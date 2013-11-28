#-*- coding: utf-8 -*-
from Products.urban.config import URBAN_TYPES
from Products.urban.testing import URBAN_TESTS_INTEGRATION
from Products.urban.utils import getLicenceFolder

from plone.app.testing import login
from plone.testing.z2 import Browser

import transaction
import unittest


class TestGenericLicenceFields(unittest.TestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test EnvClassOne licence
        login(self.portal, 'urbaneditor')
        self.licences = []
        for content_type in URBAN_TYPES:
            licence_folder = getLicenceFolder(self.urban, content_type)
            testlicence_id = 'test_{}'.format(content_type)
            if testlicence_id not in licence_folder.objectIds():
                licence_folder.invokeFactory(content_type, id=testlicence_id)
                transaction.commit()
            test_licence = getattr(licence_folder, testlicence_id)
            self.licences.append(test_licence)

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_has_attribute_licenceSubject(self):
        for licence in self.licences:
            self.assertTrue(hasattr(licence, 'licenceSubject'))

    def test_licenceSubject_is_visible(self):
        for licence in self.licences:
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Objet</span>:" in contents)
