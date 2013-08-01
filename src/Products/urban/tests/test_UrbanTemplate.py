# -*- coding: utf-8 -*-
import unittest
from time import sleep
from zope.component.interface import interfaceToName
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_LICENCES, URBAN_TESTS_PROFILE_FUNCTIONAL
from Products.urban.interfaces import IAcknowledgmentEvent
from Products.CMFCore.utils import getToolByName
from Products.urban.utils import getMd5Signature


class TestUrbanTemplates(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

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

    def testUrbanTemplatesUpdate(self):
        """
            Testing updating templates, depending on:
            - profile
            - md5Loaded
            - md5Modified
        """
        # check if template is well already installed
        my_accuse_folder = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'accuse-de-reception', None)
        self.assertNotEqual(my_accuse_folder, None)
        my_file_odt = getattr(my_accuse_folder, 'urb-accuse.odt', None)
        self.assertNotEqual(my_file_odt, None)
        my_update_file_datetime = my_file_odt.modified()

        # update template test by profil test (same template, identical md5loaded) : do nothing
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')
        self.assertEqual(my_file_odt.modified(), my_update_file_datetime)

        # update template test by profil test (md5Loaded changed) : replace
        my_file_odt.manage_changeProperties({"md5Loaded": 'reloadtemplate'})
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')
        self.assertNotEqual(my_file_odt.modified(), my_update_file_datetime)

        # update template test by profil testCommune1 : replace template
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:testCommune1', 'urban-Commune1UpdateTemplates')
        self.assertNotEqual(my_file_odt.modified(), my_update_file_datetime)
        my_update_file_datetime = my_file_odt.modified()  # warning, date have changed

        # update template testCommune1 by profil test: do nothing
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')
        self.assertEqual(my_file_odt.modified(), my_update_file_datetime)

        # update template testCommune1 by profil testCommune2: do nothing
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:testCommune2', 'urban-Commune2UpdateTemplates')
        self.assertEqual(my_file_odt.modified(), my_update_file_datetime)

        # modify the value of property profilename (testCommune1) by (extra) and launch test profile : replace template
        my_file_odt.manage_changeProperties({"profileName": 'extra'})
        my_update_file_datetime = my_file_odt.modified()  # warning, date have changed by manage_changeProperties
        sleep(1)
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')
        self.assertNotEqual(my_file_odt.modified(), my_update_file_datetime)

        # change the value of property md5Modified, set the value of property profileName to testCommune1 and update template test
        #   by profil testCommune1 : do nothing because template has been customised
        my_file_odt.manage_changeProperties({"md5Loaded": 'reloadtemplate'})
        my_file_odt.manage_changeProperties({"md5Modified": 'aaaaaaa'})
        my_update_file_datetime = my_file_odt.modified()  # warning, date have changed by manage_changeProperties
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:testCommune1', 'urban-Commune1UpdateTemplates')
        self.assertEqual(my_file_odt.modified(), my_update_file_datetime)

    def testUrbanTemplatesUpdateForced(self):
        """
            Testing updating templates when force
        """
        # check if template is well already installed
        my_accuse_folder = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'accuse-de-reception', None)
        my_file_odt = getattr(my_accuse_folder, 'urb-accuse.odt', None)
        self.assertNotEqual(my_file_odt, None)
        my_update_file_datetime = my_file_odt.modified()
        my_header_odt = getattr(self.portal_urban.globaltemplates, 'header.odt', None)
        self.assertNotEqual(my_header_odt, None)
        my_update_header_datetime = my_header_odt.modified()
        portal = self.layer['portal']

        # Without forcing
        # First loaded template is the same: no replacement
        my_update_file_datetime = my_file_odt.modified()
        my_update_header_datetime = my_header_odt.modified()
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')
        self.assertEqual(my_header_odt.modified(), my_update_header_datetime)
        self.assertEqual(my_file_odt.modified(), my_update_file_datetime)
        # Second loaded template isn't the same and template isn't modified: replacement
        my_file_odt.manage_changeProperties({"md5Loaded": 'reloadtemplate'})
        my_header_odt.manage_changeProperties({"md5Loaded": 'reloadtemplate'})
        my_update_file_datetime = my_file_odt.modified()
        my_update_header_datetime = my_header_odt.modified()
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')
        self.assertNotEquals(my_header_odt.modified(), my_update_header_datetime)
        self.assertNotEquals(my_file_odt.modified(), my_update_file_datetime)
        # Second loaded template isn't the same and template is modified : no replacement
        my_file_odt.manage_changeProperties({"md5Loaded": 'reloadtemplate', "md5Modified": 'modified'})
        my_header_odt.manage_changeProperties({"md5Loaded": 'reloadtemplate', "md5Modified": 'modified'})
        my_update_file_datetime = my_file_odt.modified()
        my_update_header_datetime = my_header_odt.modified()
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')
        self.assertEqual(my_header_odt.modified(), my_update_header_datetime)
        self.assertEqual(my_file_odt.modified(), my_update_file_datetime)

        # Forcing replacement when loaded template is the same as on the file system and hasn't been manually modified: replacement
        my_file_odt.manage_changeProperties({"md5Loaded": getMd5Signature(my_file_odt.data), "md5Modified": getMd5Signature(my_file_odt.data)})
        my_header_odt.manage_changeProperties({"md5Loaded": getMd5Signature(my_header_odt.data), "md5Modified": getMd5Signature(my_header_odt.data)})
        portal.REQUEST.form['reload_globals'] = 1
        portal.REQUEST.form['reload_events'] = 1
        my_update_file_datetime = my_file_odt.modified()
        my_update_header_datetime = my_header_odt.modified()
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')
        self.assertNotEquals(my_header_odt.modified(), my_update_header_datetime)
        self.assertNotEquals(my_file_odt.modified(), my_update_file_datetime)

        # Forcing replacement when loaded template is the same as on the file system but has been manually modified: no replacement
        my_file_odt.manage_changeProperties({"md5Loaded": getMd5Signature(my_file_odt.data), "md5Modified": 'modified'})
        my_header_odt.manage_changeProperties({"md5Loaded": getMd5Signature(my_header_odt.data), "md5Modified": 'modified'})
        portal.REQUEST.form['reload_globals'] = 1
        portal.REQUEST.form['reload_events'] = 1
        my_update_file_datetime = my_file_odt.modified()
        my_update_header_datetime = my_header_odt.modified()
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')
        self.assertEqual(my_header_odt.modified(), my_update_header_datetime)
        self.assertEqual(my_file_odt.modified(), my_update_file_datetime)
        portal.REQUEST.form.pop('reload_globals')
        portal.REQUEST.form.pop('reload_events')

        # Forcing replacement when loaded template is the same as on the file system, has been manually modified but is forced for this case: replacement
        my_file_odt.manage_changeProperties({"md5Loaded": getMd5Signature(my_file_odt.data), "md5Modified": 'modified'})
        my_header_odt.manage_changeProperties({"md5Loaded": getMd5Signature(my_header_odt.data), "md5Modified": 'modified'})
        portal.REQUEST.form['reload_globals'] = 1
        portal.REQUEST.form['reload_events'] = 1
        portal.REQUEST.form['replace_mod_globals'] = 1
        portal.REQUEST.form['replace_mod_events'] = 1
        my_update_file_datetime = my_file_odt.modified()
        my_update_header_datetime = my_header_odt.modified()
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')
        self.assertNotEquals(my_header_odt.modified(), my_update_header_datetime)
        self.assertNotEquals(my_file_odt.modified(), my_update_file_datetime)
        portal.REQUEST.form.pop('reload_globals')
        portal.REQUEST.form.pop('reload_events')

        # Forcing replacement when template has been modified
        portal.REQUEST.form['replace_mod_globals'] = 1
        portal.REQUEST.form['replace_mod_events'] = 1
        my_file_odt.manage_changeProperties({"md5Loaded": 'reloadtemplate', "md5Modified": 'modified'})
        my_header_odt.manage_changeProperties({"md5Loaded": 'reloadtemplate', "md5Modified": 'modified'})
        my_update_file_datetime = my_file_odt.modified()
        my_update_header_datetime = my_header_odt.modified()
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests', 'urban-updateAllUrbanTemplates')
        self.assertNotEquals(my_header_odt.modified(), my_update_header_datetime)
        self.assertNotEquals(my_file_odt.modified(), my_update_file_datetime)
        portal.REQUEST.form.pop('replace_mod_events')


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
        licences = [getattr(urban_folder, lf).objectValues()[0] for lf in licence_folders]
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
                    display_value = licence.getValueForTemplate(fieldname)
                    print '%s %s' % (fieldname, display_value)
                else:
                    method_name = self.field_exceptions[fieldname]
                    template_helpermethod = getattr(licence, method_name)
                    template_helpermethod()
            except:
                print '\n%s\n%s' % (licence, fieldname)
                self.fail()
