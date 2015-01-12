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

    def test_contact_has_attribute_personTitle(self):
        self.assertTrue(self.contact.getField('personTitle'))

    def test_contact_personTitle_is_visible(self):
        self._is_field_visible("Titre", obj=self.contact)

    def test_contact_personTitle_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Titre", obj=self.contact)

    def test_contact_has_attribute_name1(self):
        self.assertTrue(self.contact.getField('name1'))

    def test_contact_name1_is_visible(self):
        self._is_field_visible("Nom", obj=self.contact)

    def test_contact_name1_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Nom", obj=self.contact)

    def test_contact_has_attribute_name2(self):
        self.assertTrue(self.contact.getField('name2'))

    def test_contact_name2_is_visible(self):
        self._is_field_visible("Prénom", obj=self.contact)

    def test_contact_name2_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Prénom", obj=self.contact)

    def test_contact_has_attribute_society(self):
        self.assertTrue(self.contact.getField('society'))

    def test_contact_society_is_visible(self):
        self._is_field_visible("Société", obj=self.contact)

    def test_contact_scoiety_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Société", obj=self.contact)

    def test_contact_has_attribute_representedBySociety(self):
        self.assertTrue(self.contact.getField('representedBySociety'))

    def test_contact_representedBySociety_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Représenté par la société", obj=self.contact)

    def test_contact_has_attribute_isSameAddressAsWorks(self):
        self.assertTrue(self.contact.getField('isSameAddressAsWorks'))

    def test_contact_isSameAddressAsWorks_is_visible(self):
        self._is_field_visible("Adresse identique à l'adresse du bien", obj=self.contact)

    def test_contact_isSameAddressAsWorks_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Adresse identique à l'adresse du bien", obj=self.contact)

    def test_contact_has_attribute_street(self):
        self.assertTrue(self.contact.getField('street'))

    def test_contact_street_is_visible(self):
        self._is_field_visible("Rue", obj=self.contact)

    def test_contact_street_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Rue", obj=self.contact)

    def test_contact_has_attribute_number(self):
        self.assertTrue(self.contact.getField('number'))

    def test_contact_number_is_visible(self):
        self._is_field_visible("Numéro", obj=self.contact)

    def test_contact_number_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Numéro", obj=self.contact)

    def test_contact_has_attribute_zipcode(self):
        self.assertTrue(self.contact.getField('zipcode'))

    def test_contact_zipcode_is_visible(self):
        self._is_field_visible("Code Postal", obj=self.contact)

    def test_contact_zipcode_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Code Postal", obj=self.contact)

    def test_contact_has_attribute_city(self):
        self.assertTrue(self.contact.getField('city'))

    def test_contact_city_is_visible(self):
        self._is_field_visible("Localité", obj=self.contact)

    def test_contact_city_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Localité", obj=self.contact)

    def test_contact_has_attribute_country(self):
        self.assertTrue(self.contact.getField('country'))

    def test_contact_country_is_visible(self):
        self._is_field_visible("Pays", obj=self.contact)

    def test_contact_country_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Pays", obj=self.contact)

    def test_contact_has_attribute_email(self):
        self.assertTrue(self.contact.getField('email'))

    def test_contact_email_is_visible(self):
        self._is_field_visible("E-mail", obj=self.contact)

    def test_contact_email_is_visible_in_edit(self):
        self._is_field_visible_in_edit("E-mail", obj=self.contact)

    def test_contact_has_attribute_phone(self):
        self.assertTrue(self.contact.getField('phone'))

    def test_contact_phone_is_visible(self):
        self._is_field_visible("Téléphone", obj=self.contact)

    def test_contact_phone_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Téléphone", obj=self.contact)

    def test_contact_has_attribute_fax(self):
        self.assertTrue(self.contact.getField('fax'))

    def test_contact_fax_is_visible(self):
        self._is_field_visible("Fax", obj=self.contact)

    def test_contact_fax_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Fax", obj=self.contact)

    def test_contact_has_attribute_registrationNumber(self):
        self.assertTrue(self.contact.getField('registrationNumber'))

    def test_contact_registrationNumber_is_visible(self):
        self._is_field_visible("de registre national", obj=self.contact)

    def test_contact_registrationNumber_is_visible_in_edit(self):
        self._is_field_visible_in_edit("de registre national", obj=self.contact)

    def test_contact_has_attribute_representedBy(self):
        self.assertTrue(self.contact.getField('representedBy'))
