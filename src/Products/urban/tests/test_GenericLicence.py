#-*- coding: utf-8 -*-
from Products.urban.config import URBAN_TYPES
from Products.urban.testing import URBAN_TESTS_INTEGRATION
from Products.urban import utils

from plone.app.testing import login
from plone.testing.z2 import Browser

import transaction
import unittest


class TestGenericLicenceFields(unittest.TestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test EnvClassOne licence
        login(self.portal, 'urbaneditor')
        self.licences = []
        for content_type in URBAN_TYPES:
            licence_folder = utils.getLicenceFolder(content_type)
            testlicence_id = 'test_{}'.format(content_type)
            if testlicence_id not in licence_folder.objectIds():
                licence_folder.invokeFactory(content_type, id=testlicence_id)
                transaction.commit()
            test_licence = getattr(licence_folder, testlicence_id)
            self.licences.append(test_licence)

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_has_attribute_licenceSubject(self):
        field_name = 'licenceSubject'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_licenceSubject_is_visible(self):
        for licence in self.licences:
            msg = "field 'object' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Objet</span>:" in contents, msg)

    def test_has_attribute_reference(self):
        field_name = 'reference'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_reference_is_visible(self):
        for licence in self.licences:
            msg = "field 'reference' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Référence</span>:" in contents, msg)

    def test_has_attribute_referenceDGATLP(self):
        field_name = 'referenceDGATLP'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_referenceDGATLP_is_visible(self):
        for licence in self.licences:
            msg = "field 'referenceDGATLP' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Référence DGO4</span>:" in contents, msg)

    def test_has_attribute_workLocations(self):
        field_name = 'workLocations'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_workLocations_is_visible(self):
        for licence in self.licences:
            msg = "field 'workLocations' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            worklocation_is_visible = \
                "Adresse(s) des travaux" in contents \
                or \
                "Adresse de l'exploitation" in contents

            self.assertTrue(worklocation_is_visible, msg)

    def test_has_attribute_folderCategory(self):
        field_name = 'folderCategory'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_folderCategory_is_visible(self):
        for licence in self.licences:
            msg = "field 'folderCategory' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Catégorie du dossier RW</span>:" in contents, msg)

    def test_has_attribute_missingParts(self):
        field_name = 'missingParts'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_missingParts(self):
        for licence in self.licences:
            msg = "field 'missingParts' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Pièces manquantes</span>:" in contents, msg)

    def test_has_attribute_missingPartsDetails(self):
        field_name = 'missingPartsDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_missingPartsDetails(self):
        for licence in self.licences:
            msg = "field 'missingPartsDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant les pièces manquantes</span>:" in contents, msg)

    def test_has_attribute_description(self):
        field_name = 'description'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_description(self):
        for licence in self.licences:
            msg = "field 'description' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Observations</span>:" in contents, msg)

    def test_has_attribute_roadMissingParts(self):
        field_name = 'roadMissingParts'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_roadMissingParts(self):
        for licence in self.licences:
            msg = "field 'roadMissingParts' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Pièces manquantes (Fiche Voirie)</span>:" in contents, msg)

    def test_has_attribute_roadMissingPartsDetails(self):
        field_name = 'roadMissingPartsDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_roadMissingPartsDetails(self):
        for licence in self.licences:
            msg = "field 'roadMissingPartsDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant les pièces manquantes (Fiche Voirie)</span>:" in contents, msg)

    def test_has_attribute_roadType(self):
        field_name = 'roadType'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_roadType(self):
        for licence in self.licences:
            msg = "field 'roadType' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Type de voirie</span>:" in contents, msg)

    def test_has_attribute_roadCoating(self):
        field_name = 'roadCoating'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_roadCoating(self):
        for licence in self.licences:
            msg = "field 'roadCoating' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Revêtement</span>:" in contents, msg)

    def test_has_attribute_roadEquipments(self):
        field_name = 'roadEquipments'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_roadEquipments(self):
        for licence in self.licences:
            msg = "field 'roadEquipments' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Equipement de la voirie au droit du bien</span>:" in contents, msg)

    def test_has_attribute_pash(self):
        field_name = 'pash'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_pash(self):
        for licence in self.licences:
            msg = "field 'pash' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>PASH</span>:" in contents, msg)

    def test_has_attribute_pashDetails(self):
        field_name = 'pashDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_pashDetails(self):
        for licence in self.licences:
            msg = "field 'pashDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant le PASH</span>:" in contents, msg)

    def test_has_attribute_catchmentArea(self):
        field_name = 'catchmentArea'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_catchmentArea(self):
        for licence in self.licences:
            msg = "field 'catchmentArea' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Zone de captage</span>:" in contents, msg)

    def test_has_attribute_catchmentAreaDetails(self):
        field_name = 'catchmentAreaDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_catchmentAreaDetails(self):
        for licence in self.licences:
            msg = "field 'catchmentAreaDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant la zone de captage</span>:" in contents, msg)

    def test_has_attribute_floodingLevel(self):
        field_name = 'floodingLevel'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_floodingLevel(self):
        for licence in self.licences:
            msg = "field 'floodingLevel' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Zone inondable (Fiche Voirie)</span>:" in contents, msg)

    def test_has_attribute_floodingLevelDetails(self):
        field_name = 'floodingLevelDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_floodingLevelDetails(self):
        for licence in self.licences:
            msg = "field 'floodingLevelDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant la zone inondable</span>:" in contents, msg)

    def test_has_attribute_equipmentAndRoadRequirements(self):
        field_name = 'equipmentAndRoadRequirements'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_equipmentAndRoadRequirements(self):
        for licence in self.licences:
            msg = "field 'equipmentAndRoadRequirements' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Prescriptions relatives à la voirie et aux équipements</span>:" in contents, msg)

    def test_has_attribute_technicalRemarks(self):
        field_name = 'technicalRemarks'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_technicalRemarks(self):
        for licence in self.licences:
            msg = "field 'technicalRemarks' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Remarques techniques</span>:" in contents, msg)

    def test_has_attribute_locationMissingParts(self):
        field_name = 'locationMissingParts'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_locationMissingParts(self):
        for licence in self.licences:
            msg = "field 'locationMissingParts' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Pièces manquantes (Fiche Urbanisme)</span>:" in contents, msg)

    def test_has_attribute_locationMissingPartsDetails(self):
        field_name = 'locationMissingPartsDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_locationMissingPartsDetails(self):
        for licence in self.licences:
            msg = "field 'locationMissingPartsDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant pièces manquantes (Fiche Urbanisme)</span>:" in contents, msg)

    def test_has_attribute_folderZone(self):
        field_name = 'folderZone'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_folderZone(self):
        for licence in self.licences:
            msg = "field 'folderZone' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Zonage au plan de secteur</span>:" in contents, msg)

    def test_has_attribute_folderZoneDetails(self):
        field_name = 'folderZoneDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_folderZoneDetails(self):
        for licence in self.licences:
            msg = "field 'folderZoneDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant le zonage</span>:" in contents, msg)

    def test_has_attribute_locationFloodingLevel(self):
        field_name = 'locationFloodingLevel'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_locationFloodingLevel(self):
        for licence in self.licences:
            msg = "field 'locationFloodingLevel' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Zone inondable (Fiche Urbanisme)</span>:" in contents, msg)

    def test_has_attribute_locationTechnicalRemarks(self):
        field_name = 'locationTechnicalRemarks'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_locationTechnicalRemarks(self):
        for licence in self.licences:
            msg = "field 'locationTechnicalRemarks' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Remarques techniques (Fiche Urbanisme)</span>:" in contents, msg)

    def test_has_attribute_isInPCA(self):
        field_name = 'isInPCA'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_isInPCA(self):
        for licence in self.licences:
            msg = "field 'isInPCA' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Le bien se situe dans un PCA</span>:" in contents, msg)

    def test_has_attribute_pca(self):
        field_name = 'pca'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_pca(self):
        for licence in self.licences:
            msg = "field 'pca' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Le bien se situe dans un PCA</span>:" in contents, msg)

    def test_has_attribute_solicitRoadOpinionsTo(self):
        field_name = 'solicitRoadOpinionsTo'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_solicitRoadOpinionsTo(self):
        for licence in self.licences:
            msg = "field 'solicitRoadOpinionsTo' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Un avis sera solicité par l'urbanisme à</span>:" in contents, msg)

    def test_has_attribute_isInSubdivision(self):
        field_name = 'isInSubdivision'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_isInSubdivision(self):
        for licence in self.licences:
            msg = "field 'isInSubdivision' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Le bien se situe dans un lotissement</span>:" in contents, msg)

    def test_has_attribute_subdivisionDetails(self):
        field_name = 'subdivisionDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_subdivisionDetails(self):
        for licence in self.licences:
            msg = "field 'subdivisionDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Le bien se situe dans un lotissement</span>:" in contents, msg)

    def test_has_attribute_protectedBuilding(self):
        field_name = 'protectedBuilding'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_protectedBuilding(self):
        for licence in self.licences:
            msg = "field 'protectedBuilding' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Bien classé ou assimilé</span>:" in contents, msg)

    def test_has_attribute_protectedBuildingDetails(self):
        field_name = 'protectedBuildingDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_protectedBuildingDetails(self):
        for licence in self.licences:
            msg = "field 'protectedBuildingDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant le bien (classé ou assimilé)</span>:" in contents, msg)

    def test_has_attribute_SSC(self):
        field_name = 'SSC'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_SSC(self):
        for licence in self.licences:
            msg = "field 'SSC' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Schéma de Structure Communal (S.S.C.)</span>:" in contents, msg)

    def test_has_attribute_sscDetails(self):
        field_name = 'sscDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_sscDetails(self):
        for licence in self.licences:
            msg = "field 'sscDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant le SSC</span>:" in contents, msg)

    def test_has_attribute_RCU(self):
        field_name = 'RCU'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_RCU(self):
        for licence in self.licences:
            msg = "field 'RCU' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Règlement Communal d'Urbanisme (R.C.U.)</span>:" in contents, msg)

    def test_has_attribute_rcuDetails(self):
        field_name = 'rcuDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_rcuDetails(self):
        for licence in self.licences:
            msg = "field 'rcuDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant le RCU</span>:" in contents, msg)

    def test_has_attribute_solicitLocationOpinionsTo(self):
        field_name = 'solicitLocationOpinionsTo'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_solicitLocationOpinionsTo(self):
        for licence in self.licences:
            msg = "field 'solicitLocationOpinionsTo' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Un avis sera solicité par l'urbanisme à</span>:" in contents, msg)

    def test_has_attribute_folderCategoryTownship(self):
        field_name = 'folderCategoryTownship'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_folderCategoryTownship(self):
        for licence in self.licences:
            msg = "field 'folderCategoryTownship' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Catégorie du dossier communale</span>:" in contents, msg)

    def test_has_attribute_areParcelsVerified(self):
        field_name = 'areParcelsVerified'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_areParcelsVerified(self):
        for licence in self.licences:
            msg = "field 'areParcelsVerified' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Les parcelles ont été vérifiées?</span>:" in contents, msg)

    def test_has_attribute_foldermanagers(self):
        field_name = 'foldermanagers'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_foldermanagers(self):
        for licence in self.licences:
            msg = "field 'foldermanagers' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Agent(s) traitant(s)</span>:" in contents, msg)

    def test_has_attribute_parcellings(self):
        field_name = 'parcellings'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_parcellings(self):
        for licence in self.licences:
            msg = "field 'parcellings' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Le bien se situe dans un lotissement</span>:" in contents, msg)
