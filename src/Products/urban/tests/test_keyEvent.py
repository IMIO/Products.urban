# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.tests.helpers import BrowserTestCase
from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent import ObjectRemovedEvent
from zope.globalrequest import getRequest
from zope.globalrequest import setRequest

import transaction


class TestKeyEvent(BrowserTestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test BuildLicence
        default_user = self.layer.default_user
        default_password = self.layer.default_password
        login(self.portal, self.layer.default_user)
        buildlicence_folder = self.urban.buildlicences
        testlicence_id = 'test_buildlicence'
        buildlicence_folder.invokeFactory('BuildLicence', id=testlicence_id)
        self.licence = getattr(buildlicence_folder, testlicence_id)
        # create a test UrbanEvent in test_buildlicence
        self.catalog = api.portal.get_tool('portal_catalog')
        event_type_brain = self.catalog(portal_type='EventConfig', id='accuse-de-reception')[0]
        self.event_type = event_type_brain.getObject()
        self.urban_event = self.licence.createUrbanEvent(self.event_type)
        transaction.commit()

        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)
        if not getRequest():
            setRequest(self.portal.REQUEST)

    def tearDown(self):
        with api.env.adopt_roles(['Manager']):
            if not getRequest():
                setRequest(self.portal.REQUEST)
            api.content.delete(self.licence)
        transaction.commit()

    def testCreateKeyEvent(self):
        catalog = self.catalog
        buildlicence = self.licence

        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        urban_event_type = urban_event.getUrbaneventtypes()

        # we delete the urban event from the buildlicence and set the urbanEventType UET as a key event
        buildlicence.manage_delObjects(urban_event.id)
        urban_event_type.isKeyEvent = True

        # we add an urbanEvent of type UET, the index last_key_event of the licence should be updated
        buildlicence.createUrbanEvent(urban_event_type)
        urban_event = buildlicence.objectValues('UrbanEvent')[-1]
        event = ObjectModifiedEvent(urban_event)
        notify(event)
        buildlicence_brain = catalog(portal_type='BuildLicence', id=buildlicence.id)[0]

        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], urban_event_type.Title())

    def testDeleteKeyEvent(self):
        buildlicence = self.licence
        catalog = self.catalog

        old_index_value = catalog(portal_type='BuildLicence')[0].last_key_event
        event_type = self.catalog(portal_type='EventConfig', id='depot-de-la-demande')[0].getObject()
        buildlicence.createUrbanEvent(event_type)
        urban_event = buildlicence.objectValues()[1]
        event = ObjectModifiedEvent(urban_event)
        notify(event)
        buildlicence_brain = catalog(portal_type='BuildLicence', id=buildlicence.id)[0]

        self.assertTrue(buildlicence_brain.last_key_event != old_index_value)

        # we remove the key event, the index last_key_event of the licence should be back to its original value
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

        old_fields = self.event_type.getActivatedFields()
        self.event_type.activatedFields = old_fields + ('decisionDate',)
        self.event_type.keyDates = ('decisionDate',)
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
        # so far the dates shouldnt appears
        self.assertTrue(date_1 not in self.browser.contents)
        self.assertTrue(date_2 not in self.browser.contents)


        setRequest(self.portal.REQUEST)
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
