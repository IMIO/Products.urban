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
        field_name = 'licenceSubject'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_licenceSubject_is_visible(self):
        for licence in self.licences:
            msg = "field 'object' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Objet</span>:" in contents, msg)

    def test_has_attribute_reference(self):
        field_name = 'reference'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_reference_is_visible(self):
        for licence in self.licences:
            msg = "field 'reference' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Référence</span>:" in contents, msg)

    def test_has_attribute_referenceDGATLP(self):
        field_name = 'referenceDGATLP'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_referenceDGATLP_is_visible(self):
        for licence in self.licences:
            msg = "field 'referenceDGATLP' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Référence DGO4</span>:" in contents, msg)

    def test_has_attribute_workLocations(self):
        field_name = 'workLocations'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_workLocations_is_visible(self):
        for licence in self.licences:
            msg = "field 'workLocations' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            worklocation_is_visible = \
                "Adresse(s) des travaux" in contents \
                or \
                "Adresse de l'exploitation" in contents

            self.assertTrue(worklocation_is_visible, msg)

    def test_has_attribute_folderCategory(self):
        field_name = 'folderCategory'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_folderCategory_is_visible(self):
        for licence in self.licences:
            msg = "field 'folderCategory' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Catégorie du dossier RW</span>:" in contents, msg)

    def test_has_attribute_missingParts(self):
        field_name = 'missingParts'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_missingParts(self):
        for licence in self.licences:
            msg = "field 'missingParts' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Pièces manquantes</span>:" in contents, msg)

    def test_has_attribute_missingPartsDetails(self):
        field_name = 'missingPartsDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_missingPartsDetails(self):
        for licence in self.licences:
            msg = "field 'missingPartsDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant les pièces manquantes</span>:" in contents, msg)

    def test_has_attribute_description(self):
        field_name = 'description'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_description(self):
        for licence in self.licences:
            msg = "field 'description' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Observations</span>:" in contents, msg)
