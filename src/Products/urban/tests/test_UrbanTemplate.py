# -*- coding: utf-8 -*-

from Products.urban.interfaces import IEnvironmentBase
from Products.urban.profiles.testsWithLicences.licences_data import licences_data
from Products.urban.testing import URBAN_TESTS_LICENCES

from plone import api
from plone.app.testing import login

import unittest


class TestTemplateMethods(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.portal_urban = portal.portal_urban
        login(portal, 'urbaneditor')

        licence_folders = ['{}s'.format(ptype.lower()) for ptype in licences_data.keys()]

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
            'specificFeatures': 'getSpecificFeaturesForTemplate',
            'roadSpecificFeatures': 'getSpecificFeaturesForTemplate',
            'locationSpecificFeatures': 'getSpecificFeaturesForTemplate',
            'customSpecificFeatures': 'getSpecificFeaturesForTemplate',
            'townshipSpecificFeatures': 'getSpecificFeaturesForTemplate',
        }
        self.field_exceptions = field_exceptions

    def testGetValueForTemplate(self):
        for licence in self.licences:
            self._testGVFTforLicence(licence)

    def _testGVFTforLicence(self, licence):
        if IEnvironmentBase.providedBy(licence):
            login(self.portal, 'environmenteditor')
        else:
            login(self.portal, 'urbaneditor')
        fields = licence.schema.fields()
        field_names = [f.getName() for f in fields if f.schemata not in ['default', 'metadata']]

        for fieldname in field_names:
            if fieldname not in self.field_exceptions:
                licence.getValueForTemplate(fieldname)
            else:
                method_name = self.field_exceptions[fieldname]
                template_helpermethod = getattr(licence, method_name, None)
                if template_helpermethod:
                    template_helpermethod()

    def testUrbanTemplateIsUnderActivationWF(self):
        wf_tool = api.portal.get_tool('portal_workflow')
        # Check that templates .odt files in urbanEventTypes are under activation wf policy
        urban_event_type = getattr(self.portal_urban.buildlicence.eventconfigs, 'accuse-de-reception', None)
        template = getattr(urban_event_type, 'urb-accuse.odt', None)
        state = wf_tool.getInfoFor(template, 'review_state')
        self.assertEqual(state, 'enabled')

    def testGeneratedDocumentIsNotUnderActivationWF(self):
        wf_tool = api.portal.get_tool('portal_workflow')

        # Check that generated .odt files in urbanEvents are NOT under any wf policy
        buildlicence = [l for l in self.licences if l.portal_type == 'BuildLicence'][0]
        urban_event = buildlicence.getLastAcknowledgment()
        document = getattr(urban_event, 'urb-accuse.odt', None)
        exception_msg = ""
        try:
            wf_tool.getInfoFor(document, 'review_state')
        except Exception, error:
            exception_msg = "%s" % error
        self.assertEqual(exception_msg, "No workflow provides '${name}' information.")
