#-*- coding: utf-8 -*-
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.tests.helpers import BrowserTestCase

from plone import api
from plone.testing.z2 import Browser

import transaction


class TestUrbanDoc(BrowserTestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban

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
        self.urbandoc_model = getattr(self.event_type, 'urb-accuse.odt')
        transaction.commit()

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def test_TALCondition_visible_on_document_templates(self):
        self.browser.open(self.urbandoc_model.absolute_url() + '/view')
        self.assertTrue('TALCondition' in self.browser.contents)

    def test_TALCondition_hidden_on_generated_documents(self):
        event = self.urban_event
        generated_doc = event.objectValues('UrbanDoc')[0]
        self.browser.open(generated_doc.absolute_url() + '/view')
        self.assertTrue('TALCondition' not in self.browser.contents)

    def test_mayGenerateUrbanDoc_with_false_TALcondition(self):
        self.urbandoc_model.setTALCondition('python: False')
        may_generate_document = self.urbandoc_model.mayGenerateUrbanDoc(self.licence)
        self.assertTrue(not may_generate_document)

    def test_mayGenerateUrbanDoc_with_true(self):
        self.urbandoc_model.setTALCondition('python: True')
        may_generate_document = self.urbandoc_model.mayGenerateUrbanDoc(self.licence)
        self.assertTrue(may_generate_document)

    def test_link_to_generate_document_is_hidden_when_TALcondition_is_false(self):
        self.urbandoc_model.setTALCondition('python: False')

        # delete generated document (if any) to be sure to not confuse links to
        # generate documents from the link of generated documents
        document = self.urban_event.objectValues()[0]
        api.content.delete(document)
        transaction.commit()

        self.browser.open(self.urban_event.absolute_url())
        link = '{title}</a>'.format(title=self.urbandoc_model.Title())

        self.assertTrue(link not in self.browser.contents)

    def test_link_to_generate_document_is_visible_when_TALcondition_is_true(self):
        self.urbandoc_model.setTALCondition('python: True')

        # delete generated document (if any) to be sure to not confuse links to
        # generate documents from the link of generated documents
        document = self.urban_event.objectValues()[0]
        api.content.delete(document)
        transaction.commit()

        self.browser.open(self.urban_event.absolute_url())
        link = '{title}</a>'.format(title=self.urbandoc_model.Title())

        self.assertTrue(link in self.browser.contents)
