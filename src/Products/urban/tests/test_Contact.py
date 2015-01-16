#-*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_LICENCES_FUNCTIONAL
from Products.urban.testing import URBAN_TESTS_INTEGRATION
from Products.urban.tests.helpers import BrowserTestCase
from Products.urban.tests.helpers import SchemaFieldsTestCase

from plone.app.testing import login
from plone.testing.z2 import Browser

import transaction
import unittest


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


class TestContactEvents(unittest.TestCase):
    """
    """

    layer = URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test BuildLicence licence for Applicant contact
        login(self.portal, 'urbaneditor')
        buildlicence_folder = self.urban.buildlicences
        testlicence_id = 'test_buildlicence'
        if testlicence_id not in buildlicence_folder.objectIds():
            buildlicence_folder.invokeFactory('BuildLicence', id=testlicence_id)
        self.applicant_licence = getattr(buildlicence_folder, testlicence_id)

        # create a test UrbanCertificateOne licence for Proprietary contact
        login(self.portal, 'urbaneditor')
        urbancertificateone_folder = self.urban.urbancertificateones
        testlicence_id = 'test_urbancertificateone'
        if testlicence_id not in urbancertificateone_folder.objectIds():
            urbancertificateone_folder.invokeFactory('UrbanCertificateOne', id=testlicence_id)
        self.proprietary_licence = getattr(urbancertificateone_folder, testlicence_id)

        # create a test EnvClassOne licence for Corporation contact
        login(self.portal, 'urbaneditor')
        envclassone_folder = self.urban.envclassones
        testlicence_id = 'test_envclassone'
        if testlicence_id not in envclassone_folder.objectIds():
            envclassone_folder.invokeFactory('EnvClassOne', id=testlicence_id)
        self.corporation_licence = getattr(envclassone_folder, testlicence_id)

    def test_licence_title_is_updated_when_contact_modified(self):
        """
        """


class TestApplicantFields(SchemaFieldsTestCase):

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

        applicant_id = 'test_applicant'
        if applicant_id not in self.licence.objectIds():
            self.licence.invokeFactory('Applicant', id=applicant_id)
            transaction.commit()
        self.applicant = getattr(self.licence, applicant_id)

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def test_applicant_has_attribute_representedBySociety(self):
        self.assertTrue(self.applicant.getField('representedBySociety'))

    def test_applicant_representedBySociety_is_visible(self):
        self._is_field_visible("Représenté par la société", obj=self.applicant)

    def test_applicant_representedBySociety_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Représenté par la société", obj=self.applicant)

    def test_applicant_has_attribute_isSameAddressAsWorks(self):
        self.assertTrue(self.applicant.getField('isSameAddressAsWorks'))

    def test_applicant_isSameAddressAsWorks_is_visible(self):
        self._is_field_visible("Adresse identique à l'adresse du bien", obj=self.applicant)

    def test_applicant_isSameAddressAsWorks_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Adresse identique à l'adresse du bien", obj=self.applicant)

    def test_applicant_has_attribute_representedBy(self):
        self.assertTrue(self.applicant.getField('representedBy'))

    def test_applicant_representedBy_is_visible(self):
        self._is_field_visible("Représenté par</span>", obj=self.applicant)

    def test_applicant_representedBy_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Représenté par", obj=self.applicant)


class TestApplicantDisplay(BrowserTestCase):

    layer = URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban

        login(self.portal, 'urbaneditor')
        self.licence = self.portal.urban.buildlicences.objectValues()[-1]
        self.applicant = self.licence.getApplicants()[0]

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def test_address_display_when_sameAddressAsWorks_is_checked(self):
        self.applicant.setStreet('Rue kikoulo')
        self.applicant.setNumber('6969')
        self.applicant.setZipcode('5000')
        self.applicant.setCity('Namur')
        transaction.commit()

        address_fields = ['street', 'number', 'zipcode', 'city']

        self.browser.open(self.applicant.absolute_url())
        contents = self.browser.contents
        for field_name in address_fields:
            field = self.applicant.getField(field_name)
            field_value = field.getAccessor(self.applicant)()
            msg = "field '{}' value '{}' should have been displayed".format(
                field_name, field_value
            )
            self.assertTrue(field_value in contents, msg)

        self.applicant.setIsSameAddressAsWorks(True)
        transaction.commit()

        self.browser.open(self.applicant.absolute_url())
        contents = self.browser.contents
        licence_address = self.licence.getWorkLocationSignaletic()
        for field_name in address_fields:
            field = self.applicant.getField(field_name)
            field_value = field.getAccessor(self.applicant)()
            self.assertTrue(field_value in licence_address)
            field_content = field.get(self.applicant)
            self.assertTrue(field_value != field_content)
            self.assertTrue(field_content not in contents)


class TestCorporationFields(SchemaFieldsTestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban

        login(self.portal, 'urbaneditor')
        envclassone_folder = self.urban.envclassones
        testlicence_id = 'test_envclassone'
        if testlicence_id not in envclassone_folder.objectIds():
            envclassone_folder.invokeFactory('EnvClassOne', id=testlicence_id)
            transaction.commit()
        self.licence = getattr(envclassone_folder, testlicence_id)

        corporation_id = 'test_corporation'
        if corporation_id not in self.licence.objectIds():
            self.licence.invokeFactory('Corporation', id=corporation_id)
            transaction.commit()
        self.corporation = getattr(self.licence, corporation_id)

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def test_corporation_has_attribute_denomination(self):
        self.assertTrue(self.corporation.getField('denomination'))

    def test_corporation_denomination_is_visible(self):
        self._is_field_visible("Dénomination ou raison sociale", obj=self.corporation)

    def test_corporation_denomination_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Dénomination ou raison sociale", obj=self.corporation)
