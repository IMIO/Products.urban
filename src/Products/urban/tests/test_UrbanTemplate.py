# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_LICENCES, URBAN_TESTS_CONFIG
from Products.urban.interfaces import IAcknowledgmentEvent

from plone import api

from plone.app.testing import login

from zope.component.interface import interfaceToName

import unittest


class TestUrbanTemplates(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_urban = self.portal.portal_urban
        login(self.portal, 'urbanmanager')

        self.catalog = api.portal.get_tool('portal_catalog')
        event_type = self.catalog(portal_type='UrbanEventType', id='accuse-de-reception')[0].getObject()
        self.urbandoc_model = getattr(event_type, 'urb-accuse.odt')

    def testUrbanTemplateIsUnderActivationWF(self):
        #Check that templates .odt files in urbanEventTypes are under activation wf policy
        urban_event_type = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'accuse-de-reception', None)
        template = getattr(urban_event_type, 'urb-accuse.odt', None)
        self.assertTrue(api.content.get_state(template) == 'enabled')

    def test_generation_condition_with_disabled_state(self):
        api.content.transition(self.urbandoc_model, 'disable')
        may_generate_document = self.urbandoc_model.can_be_generated(self.portal)
        self.assertTrue(not may_generate_document)

    def test_generation_condition_with_enabled_state(self):
        may_generate_document = self.urbandoc_model.can_be_generated(self.portal)
        self.assertTrue(may_generate_document)


class TestUrbanDocuments(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.portal_setup = portal.portal_setup
        login(portal, 'urbaneditor')

    def testGeneratedDocumentIsNotUnderActivationWF(self):
        portal = self.layer['portal']
        catalog = api.portal.get_tool('portal_catalog')
        wf_tool = api.portal_catalog('portal_workflow')
        #Check that generated .odt files in urbanEvents are NOT under any wf policy
        interfaceName = interfaceToName(portal, IAcknowledgmentEvent)
        urban_event = catalog(object_provides=interfaceName)[0].getObject()
        document = getattr(urban_event, 'urb-accuse.odt', None)
        msg = 'No workflow expected for Generated documents'
        self.assertTrue(wf_tool.getDefaultChainFor(document.portal_type) == (), msg)


class TestTemplateMethods(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        login(portal, 'urbaneditor')

        licence_folders = [
            'buildlicences',
            'parceloutlicences',
            'divisions',
            'notaryletters',
            'urbancertificateones',
            'urbancertificatetwos',
            'declarations',
            'miscdemands',
        ]

        urban_folder = portal.urban
        licences = [getattr(urban_folder, lf).objectValues()[-1] for lf in licence_folders]
        self.licences = licences

        field_exceptions = {
            'workLocations': 'getWorkLocationSignaletic',
            'architects': 'getArchitectsSignaletic',
            'geometricians': 'getGeometriciansSignaletic',
            'notaryContact': 'getNotariesSignaletic',
            'foldermanagers': 'getFolderManagersSignaletic',
            # datagrid
            'roadEquipments': 'Title',
        }
        self.field_exceptions = field_exceptions

    def testGetValueForTemplate(self):
        for licence in self.licences:
            self._testGVFTforLicence(licence)

    def _testGVFTforLicence(self, licence):
        fields = licence.schema.fields()
        field_names = [f.getName() for f in fields if f.schemata not in ['default', 'metadata']]

        for fieldname in field_names:
            try:
                if fieldname not in self.field_exceptions:
                    licence.getValueForTemplate(fieldname)
                else:
                    method_name = self.field_exceptions[fieldname]
                    template_helpermethod = getattr(licence, method_name)
                    template_helpermethod()
            except:
                print '\n%s\n%s' % (licence, fieldname)
                self.fail()
