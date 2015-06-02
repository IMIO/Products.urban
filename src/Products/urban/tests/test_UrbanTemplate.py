# -*- coding: utf-8 -*-
import unittest
from zope.component.interface import interfaceToName
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_LICENCES, URBAN_TESTS_CONFIG
from Products.urban.interfaces import IAcknowledgmentEvent
from Products.CMFCore.utils import getToolByName


class TestUrbanTemplates(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.portal_setup = portal.portal_setup
        login(portal, 'urbanmanager')

    def testUrbanTemplateIsUnderActivationWF(self):
        portal = self.layer['portal']
        wf_tool = getToolByName(portal, 'portal_workflow')
        #Check that templates .odt files in urbanEventTypes are under activation wf policy
        urban_event_type = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'accuse-de-reception', None)
        template = getattr(urban_event_type, 'urb-accuse.odt', None)
        state = wf_tool.getInfoFor(template, 'review_state')
        self.assertEqual(state, 'enabled')


class TestUrbanDocuments(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.portal_setup = portal.portal_setup
        login(portal, 'urbaneditor')

    def testGeneratedDocumentIsNotUnderActivationWF(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        wf_tool = getToolByName(portal, 'portal_workflow')
        #Check that generated .odt files in urbanEvents are NOT under any wf policy
        interfaceName = interfaceToName(portal, IAcknowledgmentEvent)
        urban_event = catalog(object_provides=interfaceName)[0].getObject()
        document = getattr(urban_event, 'urb-accuse.odt', None)
        exception_msg = ""
        try:
            wf_tool.getInfoFor(document, 'review_state')
        except Exception, error:
            exception_msg = "%s" % error
        self.assertEqual(exception_msg, "No workflow provides '${name}' information.")

    def testListAvailableUrbanTemplates(self):
        """
        When a template is disabled in the config, it should be removed from the list of documents to generate.
        When a template is (re)enabled, it should (re)appears in the list.
        """
        portal = self.layer['portal']
        wf_tool = getToolByName(portal, 'portal_workflow')
        catalog = getToolByName(portal, 'portal_catalog')
        urban_event_type = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'accuse-de-reception', None)
        all_templates = [obj for obj in urban_event_type.objectValues() if obj.portal_type == 'UrbanDoc']
        folder_path = "%s/urban/buildlicences" % '/'.join(portal.getPhysicalPath())
        urban_event = catalog(object_provides=interfaceToName(portal, IAcknowledgmentEvent), path={'query': folder_path, 'depth': 2})
        urban_event = urban_event[0].getObject()
        #by default all the templates should be enabled
        self.assertEqual(len(all_templates), len(urban_event.getTemplates()))
        for i in range(len(all_templates)):
            self.assertEqual(all_templates[i].Title(), urban_event.getTemplates()[i].Title())
        #disable the first template, the available doc list should contain one element less
        wf_tool.doActionFor(all_templates[0], 'disable')
        self.assertEqual(len(all_templates) - 1, len(urban_event.getTemplates()))
        for i in range(len(all_templates) - 1):
            self.assertEqual(all_templates[i + 1].Title(), urban_event.getTemplates()[i].Title())
        #re-enable the first template, the available doc list should contain one element more
        wf_tool.doActionFor(all_templates[0], 'enable')
        self.assertEqual(len(all_templates), len(urban_event.getTemplates()))
        for i in range(len(all_templates)):
            self.assertEqual(all_templates[i].Title(), urban_event.getTemplates()[i].Title())


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
