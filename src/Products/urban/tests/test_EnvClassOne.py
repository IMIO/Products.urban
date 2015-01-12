#-*- coding: utf-8 -*-

from DateTime import DateTime

from Products.urban.testing import URBAN_TESTS_INTEGRATION
from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban import utils

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import transaction
import unittest
import urllib2


class TestEnvClassOneInstall(unittest.TestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban
        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_envclassone_config_folder_exists(self):
        msg = 'envclassone config folder not created'
        self.assertTrue('envclassone' in self.portal_urban.objectIds(), msg)
        envclassone = self.portal_urban.envclassone
        from Products.urban.LicenceConfig import LicenceConfig
        self.assertTrue(isinstance(envclassone, LicenceConfig))

    def test_envclassone_config_folder_is_visible(self):
        msg = 'envclassone config folder is not visible in urban config'
        self.browser.open(self.portal_urban.absolute_url())
        contents = self.browser.contents
        self.assertTrue("Permis d'environnement classe 1" in contents, msg)

    def test_envclassone_config_folder_is_editable(self):
        self.browserLogin('urbanmanager')
        try:
            edit_url = self.portal_urban.envclassone.absolute_url() + '/edit'
            self.browser.open(edit_url)
        except urllib2.HTTPError, e:
            self.fail(msg="Got HTTP response code:" + str(e.code))

    def test_envclassone_folder_exist(self):
        msg = 'envclassones folder not created'
        self.assertTrue('envclassones' in self.urban.objectIds(), msg)

    def test_envclassone_addable_types(self):
        msg = 'cannot create EnvClassOne in licence folder'
        addable_types = self.urban.envclassones.immediatelyAddableTypes
        self.assertTrue('EnvClassOne' in addable_types, msg)
        msg = 'can create an other content type in licence folder'
        self.assertEqual(len(addable_types), 1, msg)

    def test_envclassone_licence_folder_link_in_urban_default_view(self):
        self.browser.open(self.urban.absolute_url())
        folder_url = utils.getLicenceFolder('EnvClassOne').absolute_url()
        link = self.browser.getLink(url=folder_url)
        self.assertEqual(link.text, "Permis d'environnement classe 1")
        link.click()
        contents = self.browser.contents
        self.assertTrue("Permis d'environnement classe 1" in contents)

    def test_add_envclassone_in_urban_default_view(self):
        self.browser.open(self.urban.absolute_url())
        contents = self.browser.contents
        self.assertTrue("create-EnvClassOne-link" in contents)
        link = self.browser.getLink(id="create-EnvClassOne-link")
        link.click()
        contents = self.browser.contents
        self.assertTrue("Ajouter Permis d'environnement classe 1" in contents)

    def test_EnvClassOne_is_under_licence_workflow(self):
        workflow_tool = api.portal.get_tool('portal_workflow')
        envclassone_workflow = workflow_tool.getChainForPortalType('EnvClassOne')
        self.assertTrue('urban_licence_workflow' in envclassone_workflow)


class TestEnvClassOneInstance(unittest.TestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test EnvClassOne licence
        login(self.portal, 'urbaneditor')
        envclassone_folder = self.urban.envclassones
        testlicence_id = 'test_envclassone'
        if testlicence_id not in envclassone_folder.objectIds():
            envclassone_folder.invokeFactory('EnvClassOne', id=testlicence_id)
            transaction.commit()
        self.licence = getattr(envclassone_folder, testlicence_id)

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_envclassone_licence_exists(self):
        self.assertTrue(len(self.urban.envclassones.objectIds()) > 0)

    def test_envclassone_view_is_registered(self):
        msg = 'EnvClassOne view is not registered'
        login(self.portal, 'urbaneditor')
        try:
            self.licence.restrictedTraverse('envclassoneview')
        except AttributeError:
            self.fail(msg=msg)

    def test_envclassone_view(self):
        try:
            self.browser.open(self.licence.absolute_url())
        except urllib2.HTTPError,  e:
            self.fail(msg="Got HTTP response code:" + str(e.code))

    def test_envclassone_edit(self):
        self.browser.open(self.licence.absolute_url() + '/edit')
        contents = self.browser.contents
        self.assertTrue('Voirie' in contents)
        self.assertTrue('Métadonnées' not in contents)
        self.assertTrue('Données' not in contents)

    def _is_field_visible(self, expected_fieldname):
        self.browser.open(self.licence.absolute_url())
        contents = self.browser.contents
        self.assertTrue(expected_fieldname in contents)

    def _is_field_visible_in_edit(self, expected_fieldname):
        edit_url = '{}/edit'.format(self.licence.absolute_url())
        self.browser.open(edit_url)
        contents = self.browser.contents
        self.assertTrue(expected_fieldname in contents)

    def test_envclassone_has_attribute_hasEnvironmentImpactStudy(self):
        self.assertTrue(self.licence.getField('hasEnvironmentImpactStudy'))

    def test_envclassone_hasEnvironmentImpactStudy_is_visible(self):
        self._is_field_visible("Étude d'incidences sur l'environnement")

    def test_envclassone_hasEnvironmentImpactStudy_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Étude d'incidences sur l'environnement")

    def test_envclassone_has_attribute_isSeveso(self):
        self.assertTrue(self.licence.getField('isSeveso'))

    def test_envclassone_isSeveso_is_visible(self):
        self._is_field_visible("Établissement SEVESO")

    def test_envclassone_isSeveso_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Établissement SEVESO")

    def test_envclassone_has_attribute_publicRoadModifications(self):
        self.assertTrue(self.licence.getField('publicRoadModifications'))

    def test_envclassone_publicRoadModifications_is_visible(self):
        self._is_field_visible("Modifications souhaitées au tracé et à l'équipement des voiries publiques")

    def test_envclassone_publicRoadModifications_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Modifications souhaitées au tracé et à l'équipement des voiries publiques")

    def test_envclassone_has_attribute_previousLicences(self):
        self.assertTrue(self.licence.getField('previousLicences'))

    def test_envclassone_previousLicences_is_visible(self):
        self._is_field_visible("Permissions, enregistrements et déclarations existantes")

    def test_envclassone_has_attribute_validityDelay(self):
        self.assertTrue(self.licence.getField('validityDelay'))

    def test_envclassone_validityDelay_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Durée de validité du permis")

    def test_envclassone_validityDelay_is_visible(self):
        self._is_field_visible("Durée de validité du permis")

    def test_envclassone_has_attribute_authority(self):
        self.assertTrue(self.licence.getField('authority'))

    def test_envclassone_authority_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Autorité compétente")

    def test_envclassone_authority_is_visible(self):
        self._is_field_visible("Autorité compétente")

    def test_envclassone_referenceDGATLP_translation(self):
        """
        Field referenceDGATLP should be translated as 'reference DGO3'
        """
        self._is_field_visible("Référence DGO3")
        self._is_field_visible_in_edit("Référence DGO3")

    def test_envclassone_workLocation_translation(self):
        """
        Field referenceDGATLP should be translated as 'reference DGO3'
        """
        self._is_field_visible("Situation")
        self._is_field_visible_in_edit("Situation")


class TestEnvClassOneEvents(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test EnvClassOne licence
        login(self.portal, 'urbaneditor')
        envclassone_folder = self.urban.envclassones
        testlicence_id = 'test_envclassone'
        if testlicence_id not in envclassone_folder.objectIds():
            envclassone_folder.invokeFactory('EnvClassOne', id=testlicence_id)
        self.licence = getattr(envclassone_folder, testlicence_id)

    def tearDown(self):
        for event in self.licence.objectValues('UrbanEvent'):
            api.content.delete(event)

    def test_create_ExpirationEvent_when_notificationDate_is_set(self):
        """
         When the notification date of the decision event is set,
         an ExpirationEvent should be created automatically
        """
        from Products.urban.interfaces import ILicenceDeliveryEvent
        from Products.urban.interfaces import ILicenceExpirationEvent
        licence = self.licence

        # so far no event created
        self.assertEqual(licence.objectValues('UrbanEvent'), [])

        config = self.licence.getUrbanConfig()
        decision_eventtype = config.getEventTypesByInterface(ILicenceDeliveryEvent)[0]

        decision_event = licence.createUrbanEvent(decision_eventtype)
        decision_event.processForm()
        zopeevent = ObjectModifiedEvent(decision_event)
        notify(zopeevent)

        # an event providing ILicenceExpirationEvent should be created
        expiration_event = licence._getLastEvent(ILicenceExpirationEvent)
        self.assertTrue(expiration_event)

    def test_expirationDate_is_computed_correctly(self):
        """
         Expiration date = notification date + validity delay (in years).
        """
        from Products.urban.interfaces import ILicenceDeliveryEvent
        from Products.urban.interfaces import ILicenceExpirationEvent
        licence = self.licence
        validity_delay = 15
        licence.setValidityDelay(validity_delay)

        config = self.licence.getUrbanConfig()
        decision_eventtype = config.getEventTypesByInterface(ILicenceDeliveryEvent)[0]
        decision_event = licence.createUrbanEvent(decision_eventtype)
        decision_event.processForm()
        zopeevent = ObjectModifiedEvent(decision_event)
        notify(zopeevent)

        notification_date = decision_event.getEventDate()
        expected_expiration_year = validity_delay + notification_date.year()
        expiration_event = licence._getLastEvent(ILicenceExpirationEvent)
        expiration_date = expiration_event.getEventDate()

        self.assertEqual(expiration_date.year(), expected_expiration_year)
        self.assertEqual(expiration_date.month(), notification_date.month())
        self.assertEqual(expiration_date.day(), notification_date.day())

    def test_expirationDate_is_updated_when_notification_date_change(self):
        """
         When the notification date of the decision event is set,
         an ExpirationEvent should be created automatically
        """
        from Products.urban.interfaces import ILicenceDeliveryEvent
        from Products.urban.interfaces import ILicenceExpirationEvent
        licence = self.licence
        licence.setValidityDelay(0)

        config = self.licence.getUrbanConfig()
        decision_eventtype = config.getEventTypesByInterface(ILicenceDeliveryEvent)[0]

        decision_event = licence.createUrbanEvent(decision_eventtype)
        decision_event.processForm()
        zopeevent = ObjectModifiedEvent(decision_event)
        notify(zopeevent)
        notification_date = decision_event.getEventDate()

        expiration_event = licence._getLastEvent(ILicenceExpirationEvent)
        expiration_date = expiration_event.getEventDate()

        self.assertEqual(expiration_date.year(), notification_date.year())
        self.assertEqual(expiration_date.month(), notification_date.month())
        self.assertEqual(expiration_date.day(), notification_date.day())

        # change the notification date
        new_notification_date = DateTime() + 4242
        decision_event.setEventDate(new_notification_date)
        zopeevent = ObjectModifiedEvent(decision_event)
        notify(zopeevent)

        expiration_date = expiration_event.getEventDate()
        # the expiration date should have changed accordingly
        self.assertEqual(expiration_date.year(), new_notification_date.year())
        self.assertEqual(expiration_date.month(), new_notification_date.month())
        self.assertEqual(expiration_date.day(), new_notification_date.day())
