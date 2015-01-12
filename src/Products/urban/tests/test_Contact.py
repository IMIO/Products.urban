#-*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_INTEGRATION
from Products.urban.tests.helpers import SchemaFieldsTestCase

from plone.app.testing import login
from plone.testing.z2 import Browser

import transaction


class TestContactFields(SchemaFieldsTestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban

        login(self.portal, 'urbaneditor')
        buildlicence_folder = self.urban.buildlicences
        testlicence_id = 'test_buildlicence'
        if testlicence_id not in buildlicence_folder.objectIds():
            buildlicence_folder.invokeFactory('BuildLicence', id=testlicence_id)
            transaction.commit()
        self.licence = getattr(buildlicence_folder, testlicence_id)

        contact_id = 'test_contact'
        if contact_id not in self.licence.objectIds():
            self.licence.invokeFactory('Applicant', id=contact_id)
            transaction.commit()
        self.contact = getattr(self.licence, contact_id)

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def test_contact_has_attribute_personTitle_field(self):
        self.assertTrue(self.contact.getField('personTitle'))

    def test_contact_personTitle_is_visible(self):
        self._is_field_visible("Titre", obj=self.contact)

    def test_contact_personTitle_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Titre", obj=self.contact)
