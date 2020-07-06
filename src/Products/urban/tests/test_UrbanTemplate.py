# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_LICENCES

from plone.app.testing import login

import unittest


class TestTemplateMethods(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer["portal"]
        self.portal_urban = portal.portal_urban
        login(portal, "urbaneditor")

        licence_folders = [
            "buildlicences",
            "parceloutlicences",
            # 'divisions',  #  divisions are disabled for liege
            "notaryletters",
            "urbancertificateones",
            "urbancertificatetwos",
            "declarations",
            # 'miscdemands',  #  miscdemands are disabled for liege
        ]

        urban_folder = portal.urban
        licences = [
            getattr(urban_folder, lf).objectValues()[-1] for lf in licence_folders
        ]
        self.licences = licences

        field_exceptions = {
            "workLocations": "getWorkLocationSignaletic",
            "architects": "getArchitectsSignaletic",
            "geometricians": "getGeometriciansSignaletic",
            "notaryContact": "getNotariesSignaletic",
            "foldermanagers": "getFolderManagersSignaletic",
            # datagrid
            "roadEquipments": "Title",
            "specificFeatures": "getSpecificFeaturesForTemplate",
            "roadSpecificFeatures": "getSpecificFeaturesForTemplate",
            "locationSpecificFeatures": "getSpecificFeaturesForTemplate",
            "customSpecificFeatures": "getSpecificFeaturesForTemplate",
            "townshipSpecificFeatures": "getSpecificFeaturesForTemplate",
        }
        self.field_exceptions = field_exceptions

    def testGetValueForTemplate(self):
        for licence in self.licences:
            self._testGVFTforLicence(licence)

    def _testGVFTforLicence(self, licence):
        fields = licence.schema.fields()
        field_names = [
            f.getName() for f in fields if f.schemata not in ["default", "metadata"]
        ]

        for fieldname in field_names:
            if fieldname not in self.field_exceptions:
                licence.getValueForTemplate(fieldname)
            else:
                method_name = self.field_exceptions[fieldname]
                template_helpermethod = getattr(licence, method_name)
                template_helpermethod()
