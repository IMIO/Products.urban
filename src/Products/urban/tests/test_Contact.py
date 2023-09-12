#-*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_INTEGRATION
from Products.urban.testing import URBAN_TESTS_LICENCES_FUNCTIONAL
from Products.urban.tests.helpers import BrowserTestCase
from Products.urban.tests.helpers import SchemaFieldsTestCase
from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser
from zope.event import notify
from zope.globalrequest import getRequest
from zope.globalrequest import setRequest
from zope.lifecycleevent import ObjectModifiedEvent

import transaction
import unittest


class TestContactFields(SchemaFieldsTestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban

        default_user = self.layer.default_user
        default_password = self.layer.default_password
        login(self.portal, default_user)
        buildlicence_folder = self.urban.buildlicences
        testlicence_id = 'test_buildlicence'
        buildlicence_folder.invokeFactory('BuildLicence', id=testlicence_id)
        self.licence = getattr(buildlicence_folder, testlicence_id)

        contact_id = 'test_contact'
        self.licence.invokeFactory('Applicant', id=contact_id)
        transaction.commit()
        self.contact = getattr(self.licence, contact_id)

        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)

        if getRequest() is None:
            setRequest(self.portal.REQUEST)

    def tearDown(self):
        with api.env.adopt_roles(['Manager']):
            if getRequest() is None:
                setRequest(self.portal.REQUEST)
            api.content.delete(self.licence)
        transaction.commit()

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

        if getRequest() is None:
            setRequest(self.portal.REQUEST)

    def test_licence_title_is_updated_when_applicant_modified(self):
        """
        """


class TestApplicantFields(SchemaFieldsTestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban

        default_user = self.layer.default_user
        default_password = self.layer.default_password
        login(self.portal, default_user)
        buildlicence_folder = self.urban.buildlicences
        testlicence_id = 'test_buildlicence'
        buildlicence_folder.invokeFactory('BuildLicence', id=testlicence_id)
        self.licence = getattr(buildlicence_folder, testlicence_id)

        applicant_id = 'test_applicant'
        self.licence.invokeFactory('Applicant', id=applicant_id)
        transaction.commit()
        self.applicant = getattr(self.licence, applicant_id)

        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)

        if getRequest() is None:
            setRequest(self.portal.REQUEST)

    def tearDown(self):
        with api.env.adopt_roles(['Manager']):
            if getRequest() is None:
                setRequest(self.portal.REQUEST)
            api.content.delete(self.licence)
        transaction.commit()

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


class TestApplicant(BrowserTestCase):

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

        if getRequest() is None:
            setRequest(self.portal.REQUEST)

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

    def test_applicant_Title(self):
        self.applicant.setName1('Alastair')
        self.applicant.setName2('Ballcocke')
        self.assertTrue(self.applicant.Title() == 'Mes Alastair Ballcocke')

        self.applicant.setRepresentedBySociety(True)
        self.applicant.setSociety('Fletcher, Fletcher & Fletcher')
        self.assertTrue(self.applicant.Title() == 'Mes Alastair Ballcocke repr. par Fletcher, Fletcher & Fletcher')

    def test_licence_title_update_when_applicant_modified(self):
        name_1 = 'Alastair'
        name_2 = 'Ballcocke'

        self.assertTrue(name_1 not in self.licence.Title())
        self.assertTrue(name_2 not in self.licence.Title())

        self.applicant.setName1(name_1)
        self.applicant.setName2(name_2)
        zopeevent = ObjectModifiedEvent(self.applicant)
        notify(zopeevent)

        self.assertTrue(name_1 in self.licence.Title())
        self.assertTrue(name_2 in self.licence.Title())


class TestCorporationFields(SchemaFieldsTestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban

        default_user = self.layer.environment_default_user
        default_password = self.layer.environment_default_password
        login(self.portal, default_user)
        envclassone_folder = self.urban.envclassones
        testlicence_id = 'test_envclassone'
        envclassone_folder.invokeFactory('EnvClassOne', id=testlicence_id)
        self.licence = getattr(envclassone_folder, testlicence_id)

        corporation_id = 'test_corporation'
        self.licence.invokeFactory('Corporation', id=corporation_id)
        transaction.commit()
        self.corporation = getattr(self.licence, corporation_id)

        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)

        if getRequest() is None:
            setRequest(self.portal.REQUEST)

    def tearDown(self):
        with api.env.adopt_roles(['Manager']):
            if getRequest() is None:
                setRequest(self.portal.REQUEST)
            api.content.delete(self.licence)
        transaction.commit()

    def test_corporation_has_attribute_denomination(self):
        self.assertTrue(self.corporation.getField('denomination'))

    def test_corporation_denomination_is_visible(self):
        self._is_field_visible("Dénomination ou raison sociale", obj=self.corporation)

    def test_corporation_denomination_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Dénomination ou raison sociale", obj=self.corporation)

    def test_corporation_has_attribute_personRole(self):
        self.assertTrue(self.corporation.getField('personRole'))

    def test_corporation_personRole_is_visible(self):
        self._is_field_visible("Qualité", obj=self.corporation)

    def test_corporation_personRole_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Qualité", obj=self.corporation)

    def test_corporation_has_attribute_tvaNumber(self):
        self.assertTrue(self.corporation.getField('tvaNumber'))

    def test_corporation_tvaNumber_is_visible(self):
        self._is_field_visible("N° TVA", obj=self.corporation)

    def test_corporation_tvaNumber_is_visible_in_edit(self):
        self._is_field_visible_in_edit("N° TVA", obj=self.corporation)

    def test_corporation_has_attribute_bceNumber(self):
        self.assertTrue(self.corporation.getField('bceNumber'))

    def test_corporation_bceNumber_is_visible(self):
        self._is_field_visible("N° BCE", obj=self.corporation)

    def test_corporation_bceNumber_is_visible_in_edit(self):
        self._is_field_visible_in_edit("N° BCE", obj=self.corporation)

    def test_corporation_representedBy_is_hidden(self):
        self._is_field_hidden("Représenté par", obj=self.corporation)

    def test_corporation_representedBy_is_hidden_in_edit(self):
        self._is_field_hidden_in_edit("Représenté par", obj=self.corporation)

    def test_corporation_society_is_hidden(self):
        self._is_field_hidden("Société", obj=self.corporation)

    def test_corporation_society_is_hidden_in_edit(self):
        self._is_field_hidden_in_edit("Société", obj=self.corporation)

    def test_corporation_representedBySociety_is_hidden(self):
        self._is_field_hidden("Représenté par la société", obj=self.corporation)

    def test_corporation_representedBySociety_is_hidden_in_edit(self):
        self._is_field_hidden_in_edit("Représenté par la société", obj=self.corporation)


class TestCorporation(BrowserTestCase):

    layer = URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban
        default_user = self.layer.environment_default_user
        default_password = self.layer.environment_default_password

        login(self.portal, 'environmenteditor')
        self.licence = self.portal.urban.envclassones.objectValues()[-1]
        self.corporation = self.licence.getCorporations()[0]

        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)

        if getRequest() is None:
            setRequest(self.portal.REQUEST)

    def test_address_display_when_sameAddressAsWorks_is_checked(self):
        self.corporation.setStreet('Rue kikoulo')
        self.corporation.setNumber('6969')
        self.corporation.setZipcode('5000')
        self.corporation.setCity('Namur')
        transaction.commit()

        address_fields = ['street', 'number', 'zipcode', 'city']

        self.browser.open(self.corporation.absolute_url())
        contents = self.browser.contents
        for field_name in address_fields:
            field = self.corporation.getField(field_name)
            field_value = field.getAccessor(self.corporation)()
            msg = "field '{}' value '{}' should have been displayed".format(
                field_name, field_value
            )
            self.assertTrue(field_value in contents, msg)

        self.corporation.setIsSameAddressAsWorks(True)
        transaction.commit()

        self.browser.open(self.corporation.absolute_url())
        contents = self.browser.contents
        licence_address = self.licence.getWorkLocationSignaletic()
        for field_name in address_fields:
            field = self.corporation.getField(field_name)
            field_value = field.getAccessor(self.corporation)()
            self.assertTrue(field_value in licence_address)
            field_content = field.get(self.corporation)
            self.assertTrue(field_value != field_content)
            self.assertTrue(field_content not in contents)

    def test_corporation_Title(self):
        self.corporation.setDenomination('Hyperion')
        self.assertTrue(self.corporation.Title() == 'Hyperion')

    def test_licence_title_update_when_corporation_modified(self):
        company_name = 'Hyperion'

        self.assertTrue(company_name not in self.licence.Title())

        self.corporation.setDenomination(company_name)
        zopeevent = ObjectModifiedEvent(self.corporation)
        notify(zopeevent)

        self.assertTrue(company_name in self.licence.Title())
