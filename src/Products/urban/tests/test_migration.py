# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import login

from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.migration.utils import disable_licence_default_values
from Products.urban.migration.utils import restore_licence_default_values


class TestDefaultValues(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer["portal"]
        self.portal_urban = portal.portal_urban
        self.site = portal
        self.buildlicences = portal.urban.codt_buildlicences
        login(portal, self.layer.default_user)

    def createNewLicence(self, id="newlicence"):
        buildlicences = self.buildlicences
        buildlicences.invokeFactory("CODT_BuildLicence", id=id, title="blabla")
        newlicence = getattr(buildlicences, id)
        return newlicence

    def test_disabling_default_values(self):
        # disable default values
        disable_licence_default_values()
        licence_config = self.site.portal_urban.codt_buildlicence
        # set the default text value fotr the fdescription field
        default_text = "<p>Bla bla</p>"
        licence_config.textDefaultValues = (
            {"text": default_text, "fieldname": "description"},
        )
        # any new licence should have this text as value for the description field
        newlicence = self.createNewLicence()
        self.assertEquals(newlicence.Description(), "")
        # re-enable default values
        restore_licence_default_values()
        newlicence = self.createNewLicence(id="newlicence-2")
        self.assertEquals(newlicence.Description(), default_text)
