# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_CONFIG

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent import ObjectRemovedEvent

import transaction
import unittest


class TestKeyEvent(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test BuildLicence
        login(self.portal, 'urbaneditor')
        buildlicence_folder = self.urban.buildlicences
        testlicence_id = 'test_buildlicence'
        if testlicence_id not in buildlicence_folder.objectIds():
            buildlicence_folder.invokeFactory('BuildLicence', id=testlicence_id)
        self.licence = getattr(buildlicence_folder, testlicence_id)
        # create a test UrbanEvent in test_buildlicence
        self.catalog = api.portal.get_tool('portal_catalog')
        event_type_brain = self.catalog(portal_type='UrbanEventType', id='accuse-de-reception')[0]
        self.event_type = event_type_brain.getObject()
        self.urban_event = self.licence.createUrbanEvent(self.event_type)
        transaction.commit()

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def tearDown(self):
        ids_to_delete = [event.id for event in self.licence.objectValues()]
        self.licence.manage_delObjects(ids_to_delete)
        transaction.commit()

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def testCreateKeyEvent(self):
        catalog = self.catalog
        buildlicence = self.licence

        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        urban_event_type = urban_event.getUrbaneventtypes()

        #we delete the urban event from the buildlicence and set the urbanEventType UET as a key event
        buildlicence.manage_delObjects(urban_event.id)
        urban_event_type.setIsKeyEvent(True)

        #we add an urbanEvent of type UET, the index last_key_event of the licence should be updated
        buildlicence.createUrbanEvent(urban_event_type)
        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        event = ObjectModifiedEvent(urban_event)
        notify(event)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]

        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], urban_event_type.Title())

    def testDeleteKeyEvent(self):
        buildlicence = self.licence
        catalog = self.catalog

        old_index_value = catalog(portal_type='BuildLicence')[0].last_key_event
        event_type = self.catalog(portal_type='UrbanEventType', id='depot-de-la-demande')[0].getObject()
        buildlicence.createUrbanEvent(event_type)
        urban_event = buildlicence.objectValues()[1]
        event = ObjectModifiedEvent(urban_event)
        notify(event)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]

        self.assertTrue(buildlicence_brain.last_key_event != old_index_value)

        #we remove the key event, the index last_key_event of the licence should be back to its original value
        buildlicence.manage_delObjects(urban_event.id)
        event = ObjectRemovedEvent(urban_event)
        notify(event)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]

        self.assertEqual(buildlicence_brain.last_key_event, old_index_value)

    def testEventDateAsKeyDate(self):
        """
        Check if a key eventDate appears correctly on the licenceview
        """
        buildlicence = self.licence
        date = '18/09/1986'
        # so far the date shoud not appear
        self.browser.open(buildlicence.absolute_url())
        self.assertTrue(date not in self.browser.contents)

        self.urban_event.setEventDate(date)
        transaction.commit()

        self.browser.open(buildlicence.absolute_url())

        self.assertTrue(date in self.browser.contents)

    def testOptionalDateAsKeyDate(self):
        """
        Check if and optionnal date set as key date appears correctly on the licenceview
        """
        buildlicence = self.licence
        date = '18/09/1986'
        # so far the date shoud not appear
        self.browser.open(buildlicence.absolute_url())
        self.assertTrue(date not in self.browser.contents)

        self.event_type.setKeyDates(('decisionDate',))
        self.urban_event.setDecisionDate(date)
        transaction.commit()

        self.browser.open(buildlicence.absolute_url())

        self.assertTrue(date in self.browser.contents)

    def testMultipleKeyDatesDisplay(self):
        """
        If a a key event is created several time, each key date should appears on the
        description tab
        """
        buildlicence = self.licence
        date_1 = '18/09/1986'
        date_2 = '18/09/2006'

        self.browser.open(buildlicence.absolute_url())
        #so far the dates shouldnt appears
        self.assertTrue(date_1 not in self.browser.contents)
        self.assertTrue(date_2 not in self.browser.contents)

        buildlicence.createUrbanEvent(self.event_type)
        urban_event = buildlicence.objectValues()[-1]
        urban_event.setEventDate(date_1)

        buildlicence.createUrbanEvent(self.event_type)
        urban_event = buildlicence.objectValues()[-1]
        urban_event.setEventDate(date_2)

        transaction.commit()

        self.browser.open(buildlicence.absolute_url())

        self.assertTrue(date_1 in self.browser.contents)
        self.assertTrue(date_2 in self.browser.contents)
