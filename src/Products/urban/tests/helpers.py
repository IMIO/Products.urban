# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_INTEGRATION
from plone import api

import unittest


class BrowserTestCase(unittest.TestCase):
    """
    Base class for browser test cases.
    """

    def browserLogin(self, user, password=None):
        self.browser.handleErrors = False
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name="__ac_name").value = user
        self.browser.getControl(name="__ac_password").value = password or user
        self.browser.getControl(name="submit").click()


class SchemaFieldsTestCase(BrowserTestCase):
    """
    Base class for testing existence and form display of
    archetype schema fields.
    """

    layer = URBAN_TESTS_INTEGRATION

    def _is_field_visible(self, expected_fieldname, obj=None, msg=""):
        obj = obj or self.licence
        with api.env.adopt_roles(["Manager"]):
            self.browser.open(obj.absolute_url())
        contents = self.browser.contents
        self.assertTrue(expected_fieldname in contents, msg)

    def _is_field_visible_in_edit(self, expected_fieldname, obj=None, msg=""):
        obj = obj or self.licence
        edit_url = "{}/edit".format(obj.absolute_url())
        with api.env.adopt_roles(["Manager"]):
            self.browser.open(edit_url)
        contents = self.browser.contents
        self.assertTrue(expected_fieldname in contents, msg)

    def _is_field_hidden(self, expected_fieldname, obj=None, msg=""):
        obj = obj or self.licence
        with api.env.adopt_roles(["Manager"]):
            self.browser.open(obj.absolute_url())
        contents = self.browser.contents
        self.assertTrue(expected_fieldname not in contents, msg)

    def _is_field_hidden_in_edit(self, expected_fieldname, obj=None, msg=""):
        obj = obj or self.licence
        edit_url = "{}/edit".format(obj.absolute_url())
        self.browser.open(edit_url)
        contents = self.browser.contents
        self.assertTrue(expected_fieldname not in contents, msg)
