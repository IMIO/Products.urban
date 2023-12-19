# -*- coding: utf-8 -*-

from Products.urban import interfaces
from Products.urban.config import URBAN_TYPES
from Products.urban.config import URBAN_CODT_TYPES
from Products.urban.testing import URBAN_TESTS_INTEGRATION
from Products.urban.tests.helpers import SchemaFieldsTestCase
from Products.urban import utils
from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser
from zope.globalrequest import getRequest
from zope.globalrequest import setRequest

import transaction


class TestGenericLicenceFields(SchemaFieldsTestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        default_user = self.layer.default_user
        default_password = self.layer.default_password
        self.portal.acl_users.source_groups.addPrincipalToGroup(default_user, 'environment_editors')
        login(self.portal, default_user)
        self.licences = []
        exceptions = ['ExplosivesPossession', 'Inspection', 'Ticket']
        if not getRequest():
            setRequest(self.portal.REQUEST)
        for content_type in URBAN_TYPES:
            if content_type in exceptions:
                continue
            licence_folder = utils.getLicenceFolder(content_type)
            testlicence_id = 'test_{}'.format(content_type.lower())
            licence_folder.invokeFactory(content_type, id=testlicence_id)
            test_licence = getattr(licence_folder, testlicence_id)
            self.licences.append(test_licence)
        transaction.commit()

        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)

    def tearDown(self):
        with api.env.adopt_roles(['Manager']):
            if not getRequest():
                setRequest(self.portal.REQUEST)
            for licence in self.licences:
                api.content.delete(licence)
        default_user = self.layer.default_user
        self.portal.acl_users.source_groups.removePrincipalFromGroup(default_user, 'environment_editors')
        transaction.commit()

    def test_has_attribute_licenceSubject(self):
        field_name = 'licenceSubject'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_licenceSubject_is_visible(self):
        for licence in self.licences:
            msg = "field 'object' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Objet</span>:", licence, msg)

    def test_has_attribute_reference(self):
        field_name = 'reference'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_reference_is_visible(self):
        for licence in self.licences:
            msg = "field 'reference' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Référence</span>:", licence, msg)

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
            reference_is_visible = \
                "<span>Référence FD (TLPE)</span>:" in contents \
                or \
                "<span>Référence SPW Economie, Emploi, Recherche</span>:" in contents \
                or \
                "<span>Référence ARNE</span>:" in contents \
                or \
                "<span>Référence notaire</span>:" in contents
            self.assertTrue(reference_is_visible, msg)

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
                "Situation" in contents

            self.assertTrue(worklocation_is_visible, msg)

    def test_has_attribute_folderCategory(self):
        field_name = 'folderCategory'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_folderCategory_is_visible(self):
        for licence in self.licences:
            msg = "field 'folderCategory' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Type de dossier</span>:", licence, msg)

    def test_has_attribute_missingParts(self):
        field_name = 'missingParts'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_missingParts(self):
        for licence in self.licences:
            msg = "field 'missingParts' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Pièces manquantes</span>:", licence, msg)

    def test_has_attribute_missingPartsDetails(self):
        field_name = 'missingPartsDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_missingPartsDetails(self):
        for licence in self.licences:
            msg = "field 'missingPartsDetails' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Détails concernant les pièces manquantes</span>:", licence, msg)

    def test_has_attribute_description(self):
        field_name = 'description'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_description(self):
        for licence in self.licences:
            msg = "field 'description' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Observations</span>:", licence, msg)

    def test_has_attribute_roadMissingParts(self):
        field_name = 'roadMissingParts'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_roadMissingParts(self):
        for licence in self.licences:
            msg = "field 'roadMissingParts' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Pièces manquantes (Fiche Voirie)</span>:", licence, msg)

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
            self.assertTrue(
                "<span>Détails concernant les pièces manquantes (Fiche Voirie)</span>:"
                or
                "<span>Compléments</span>"
                in contents, msg
            )

    def test_has_attribute_roadType(self):
        field_name = 'roadType'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_roadType(self):
        for licence in self.licences:
            msg = "field 'roadType' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Type de voirie</span>:", licence, msg)

    def test_has_attribute_roadCoating(self):
        field_name = 'roadCoating'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_roadCoating(self):
        for licence in self.licences:
            msg = "field 'roadCoating' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Revêtement</span>:", licence, msg)

    def test_has_attribute_roadEquipments(self):
        field_name = 'roadEquipments'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_roadEquipments(self):
        for licence in self.licences:
            msg = "field 'roadEquipments' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Equipement de la voirie au droit du bien</span>:", licence, msg)

    def test_has_attribute_pash(self):
        field_name = 'pash'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_pash(self):
        for licence in self.licences:
            msg = "field 'pash' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>PASH</span>:", licence, msg)

    def test_has_attribute_pashDetails(self):
        field_name = 'pashDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_pashDetails(self):
        for licence in self.licences:
            msg = "field 'pashDetails' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Détails concernant le PASH</span>:", licence, msg)

    def test_has_attribute_catchmentArea(self):
        field_name = 'catchmentArea'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_catchmentArea(self):
        for licence in self.licences:
            msg = "field 'catchmentArea' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Zone de captage</span>:", licence, msg)

    def test_has_attribute_catchmentAreaDetails(self):
        field_name = 'catchmentAreaDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_catchmentAreaDetails(self):
        for licence in self.licences:
            msg = "field 'catchmentAreaDetails' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Détails concernant la zone de captage</span>:", licence, msg)

    def test_has_attribute_floodingLevel(self):
        field_name = 'floodingLevel'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_floodingLevel(self):
        for licence in self.licences:
            msg = "field 'floodingLevel' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Zone inondable (Fiche Voirie)</span>:", licence, msg)

    def test_has_attribute_floodingLevelDetails(self):
        field_name = 'floodingLevelDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_floodingLevelDetails(self):
        for licence in self.licences:
            msg = "field 'floodingLevelDetails' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Détails concernant la zone inondable</span>:", licence, msg)

    def test_has_attribute_equipmentAndRoadRequirements(self):
        field_name = 'equipmentAndRoadRequirements'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_equipmentAndRoadRequirements(self):
        for licence in self.licences:
            msg = "field 'equipmentAndRoadRequirements' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Prescriptions relatives à la voirie et aux équipements</span>:", licence, msg)

    def test_has_attribute_technicalRemarks(self):
        field_name = 'technicalRemarks'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_technicalRemarks(self):
        for licence in self.licences:
            msg = "field 'technicalRemarks' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Remarques techniques</span>:", licence, msg)

    def test_has_attribute_locationMissingParts(self):
        field_name = 'locationMissingParts'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_locationMissingParts(self):
        for licence in self.licences:
            msg = "field 'locationMissingParts' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Pièces manquantes (Fiche Urbanisme)</span>:", licence, msg)

    def test_has_attribute_locationMissingPartsDetails(self):
        field_name = 'locationMissingPartsDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_locationMissingPartsDetails(self):
        for licence in self.licences:
            msg = "field 'locationMissingPartsDetails' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Détails concernant pièces manquantes (Fiche Urbanisme)</span>:", licence, msg)

    def test_has_attribute_folderZone(self):
        field_name = 'folderZone'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_folderZone(self):
        for licence in self.licences:
            msg = "field 'folderZone' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Zonage au plan de secteur</span>:", licence, msg)

    def test_has_attribute_folderZoneDetails(self):
        field_name = 'folderZoneDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_folderZoneDetails(self):
        for licence in self.licences:
            msg = "field 'folderZoneDetails' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Détails concernant le zonage</span>:", licence, msg)

    def test_has_attribute_locationFloodingLevel(self):
        field_name = 'locationFloodingLevel'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_locationFloodingLevel(self):
        for licence in self.licences:
            msg = "field 'locationFloodingLevel' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Zone inondable (Fiche Urbanisme)</span>:", licence, msg)

    def test_has_attribute_locationTechnicalRemarks(self):
        field_name = 'locationTechnicalRemarks'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_locationTechnicalRemarks(self):
        for licence in self.licences:
            msg = "field 'locationTechnicalRemarks' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Remarques techniques (Fiche Urbanisme)</span>:", licence, msg)

    def test_has_attribute_isInPCA(self):
        field_name = 'isInPCA'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_isInPCA(self):
        for licence in self.licences:
            # CODT licence PCA is renamed to SOL
            if interfaces.ICODT_BaseBuildLicence.providedBy(licence) or 'CODT' in licence.portal_type:
                continue
            msg = "field 'isInPCA' not visible on {}".format(licence.getPortalTypeName())
            expected_field = "<span>Schéma d'Orientation Local</span>"
            if licence.portal_type in URBAN_CODT_TYPES:
                expected_field = "<span>SOL</span>"
            self._is_field_visible(expected_field, licence, msg)

    def test_has_attribute_pca(self):
        field_name = 'pca'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_pca(self):
        for licence in self.licences:
            # CODT licence PCA is renamed to SOL
            if interfaces.ICODT_BaseBuildLicence.providedBy(licence) or 'CODT' in licence.portal_type:
                continue
            msg = "field 'pca' not visible on {}".format(licence.getPortalTypeName())
            expected_field = "<span>Schéma d'Orientation Local</span>"
            if licence.portal_type in URBAN_CODT_TYPES:
                expected_field = "<span>SOL</span>"
            self._is_field_visible(expected_field, licence, msg)

    def test_has_attribute_solicitRoadOpinionsTo(self):
        field_name = 'solicitRoadOpinionsTo'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_solicitRoadOpinionsTo(self):
        for licence in self.licences:
            msg = "field 'solicitRoadOpinionsTo' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Un avis sera sollicité par l'urbanisme à</span>:", licence, msg)

    def test_has_attribute_isInSubdivision(self):
        field_name = 'isInSubdivision'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_isInSubdivision(self):
        for licence in self.licences:
            # CODT licence parcellings is renamed to urbanisation licence
            if interfaces.ICODT_BaseBuildLicence.providedBy(licence) or 'CODT' in licence.portal_type:
                continue
            msg = "field 'isInSubdivision' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Le bien se situe dans un permis d'urbanisation</span>:", licence, msg)

    def test_has_attribute_subdivisionDetails(self):
        field_name = 'subdivisionDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_subdivisionDetails(self):
        for licence in self.licences:
            # CODT licence parcellings is renamed to urbanisation licence
            if interfaces.ICODT_BaseBuildLicence.providedBy(licence) or 'CODT' in licence.portal_type:
                continue
            msg = "field 'subdivisionDetails' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Le bien se situe dans un permis d'urbanisation</span>:", licence, msg)

    def test_has_attribute_protectedBuilding(self):
        field_name = 'protectedBuilding'
        for licence in self.licences:
            config = licence.getLicenceConfig()
            if 'patrimony' in [line['value'] for line in config.getActiveTabs()]:
                msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
                self.assertTrue(licence.getField(field_name), msg)

    def test_protectedBuilding(self):
        for licence in self.licences:
            config = licence.getLicenceConfig()
            tabs = [row['value'] for row in config.getActiveTabs()]
            if 'patrimony' not in tabs:
                continue
            msg = "field 'protectedBuilding' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Bien classé ou assimilé</span>:", licence, msg)

    def test_has_attribute_protectedBuildingDetails(self):
        field_name = 'protectedBuildingDetails'
        for licence in self.licences:
            config = licence.getLicenceConfig()
            if 'patrimony' in [line['value'] for line in config.getActiveTabs()]:
                msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
                self.assertTrue(licence.getField(field_name), msg)

    def test_protectedBuildingDetails(self):
        for licence in self.licences:
            config = licence.getLicenceConfig()
            tabs = [row['value'] for row in config.getActiveTabs()]
            if 'patrimony' not in tabs:
                continue
            msg = "field 'protectedBuildingDetails' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Détails concernant le bien (classé ou assimilé)</span>:", licence, msg)

    def test_has_attribute_solicitLocationOpinionsTo(self):
        field_name = 'solicitLocationOpinionsTo'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_solicitLocationOpinionsTo(self):
        for licence in self.licences:
            msg = "field 'solicitLocationOpinionsTo' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Un avis sera sollicité par l'urbanisme à</span>:", licence, msg)

    def test_has_attribute_folderCategoryTownship(self):
        field_name = 'folderCategoryTownship'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_folderCategoryTownship(self):
        for licence in self.licences:
            msg = "field 'folderCategoryTownship' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Catégorie du dossier communal</span>:", licence, msg)

    def test_has_attribute_areParcelsVerified(self):
        field_name = 'areParcelsVerified'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_has_attribute_foldermanagers(self):
        field_name = 'foldermanagers'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_foldermanagers(self):
        for licence in self.licences:
            msg = "field 'foldermanagers' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Agent(s) traitant(s)</span>:", licence, msg)

    def test_has_attribute_parcellings(self):
        field_name = 'parcellings'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(licence.getField(field_name), msg)

    def test_parcellings(self):
        for licence in self.licences:
            # CODT licence parcellings is renamed to urbanisation licence
            msg = "field 'parcellings' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Le bien se situe dans un permis d'urbanisation</span>:", licence, msg)
