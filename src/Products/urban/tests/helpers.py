#-*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_INTEGRATION

import unittest


class BrowserTestCase(unittest.TestCase):
    """
    Base class for browser test cases.
    """

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()


class SchemaFieldsTestCase(BrowserTestCase):
    """
    Base class for testing existence and form display of
    archetype schema fields.
    """

    layer = URBAN_TESTS_INTEGRATION

    def _is_field_visible(self, expected_fieldname, licence=None, msg=''):
        licence = licence or self.licence
        self.browser.open(licence.absolute_url())
        contents = self.browser.contents
        self.assertTrue(expected_fieldname in contents, msg)

    def _is_field_visible_in_edit(self, expected_fieldname, licence=None, msg=''):
        licence = licence or self.licence
        edit_url = '{}/edit'.format(licence.absolute_url())
        self.browser.open(edit_url)
        contents = self.browser.contents
        self.assertTrue(expected_fieldname in contents, msg)
