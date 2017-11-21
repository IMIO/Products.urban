#-*- coding: utf-8 -*-

from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL
from Products.urban.tests.helpers import BrowserTestCase

from plone import api
from plone.testing.z2 import Browser

import transaction


class TestUrbanDoc(BrowserTestCase):

    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_urban = self.portal.portal_urban
        self.portal_urban.setGenerateSingletonDocuments(False)

        # create a test BuildLicence
        login(self.portal, self.layer.default_user)
        buildlicence_folder = self.portal.urban.buildlicences
        testlicence_id = 'test_buildlicence'
        buildlicence_folder.invokeFactory('BuildLicence', id=testlicence_id)
        self.licence = getattr(buildlicence_folder, testlicence_id)
        # create a test UrbanEvent in test_buildlicence
        self.catalog = api.portal.get_tool('portal_catalog')
        event_type_brain = self.catalog(portal_type='UrbanEventType', id='accuse-de-reception')[0]
        self.event_type = event_type_brain.getObject()
        self.urban_event = self.licence.createUrbanEvent(self.event_type)
        self.urbandoc_model = getattr(self.event_type, 'urb-accuse.odt')
        transaction.commit()

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def tearDown(self):
        api.content.delete(self.licence)
        transaction.commit()

    def test_link_to_generate_document_is_hidden_with_disabled_state(self):
        api.content.transition(self.urbandoc_model, 'disable')
        transaction.commit()

        self.browser.open(self.urban_event.absolute_url())
        link = '{title}</a>'.format(title=self.urbandoc_model.Title())

        self.assertTrue(link not in self.browser.contents)

    def test_link_to_generate_document_is_visible_with_enabled_state(self):

        self.browser.open(self.urban_event.absolute_url())
        link = '{title}</a>'.format(title=self.urbandoc_model.Title())

        self.assertTrue(link in self.browser.contents)
