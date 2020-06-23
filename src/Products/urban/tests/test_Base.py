# -*- coding: utf-8 -*-
import unittest2 as unittest
from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban import utils

from plone.app.testing import login
from plone import api

import transaction


class TestBase(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.portal_urban = portal.portal_urban
        default_user = self.layer.default_user
        login(self.portal, default_user)

        # create a test EnvClassOne licence
        self.licences = []
        content_type = 'BuildLicence'
        licence_folder = utils.getLicenceFolder(content_type)
        testlicence_id = 'test_{}'.format(content_type.lower())
        licence_folder.invokeFactory(content_type, id=testlicence_id)
        test_licence = getattr(licence_folder, testlicence_id)
        self.licences.append(test_licence)
        transaction.commit()

    def tearDown(self):
        with api.env.adopt_roles(['Manager']):
            for licence in self.licences:
                api.content.delete(licence)
        transaction.commit()

    def test_has_single_applicant(self):
        licence = self.licences[0]
        with api.env.adopt_roles(['Manager']):
            applicant = api.content.create(
                type='Applicant',
                id='fngaha',
                container=licence
            )
        applicant.setPersonTitle('mister')
        self.assertFalse(licence.hasMultipleApplicants())
        self.assertTrue(licence.hasSingleApplicant())

    def test_has_multiple_applicants(self):
        licence1 = self.licences[0]
        with api.env.adopt_roles(['Manager']):
            applicant1 = api.content.create(
                type='Applicant',
                id='fngaha',
                container=licence1
            )
        applicant1.setPersonTitle('mister')
        with api.env.adopt_roles(['Manager']):
            applicant2 = api.content.create(
                type='Applicant',
                id='sdelcourt',
                container=licence1
            )
        applicant2.setPersonTitle('mister')
        licence2 = self.licences[0]
        with api.env.adopt_roles(['Manager']):
            applicant = api.content.create(
                type='Applicant',
                id='test_couple_applicants',
                container=licence2
            )
        applicant.setPersonTitle('madam_and_mister')
        self.assertFalse(licence1.hasSingleApplicant())
        self.assertTrue(licence1.hasMultipleApplicants())
        self.assertFalse(licence2.hasSingleApplicant())
        self.assertTrue(licence2.hasMultipleApplicants())

    def test_has_single_male_applicant(self):
        licence = self.licences[0]
        with api.env.adopt_roles(['Manager']):
            applicant = api.content.create(
                type='Applicant',
                id='fngaha',
                container=licence
            )
        applicant.setPersonTitle('mister')
        self.assertFalse(licence.hasMultipleApplicants())
        self.assertTrue(licence.hasSingleMaleApplicant())

    def test_has_single_femal_applicant(self):
        licence = self.licences[0]
        with api.env.adopt_roles(['Manager']):
            applicant = api.content.create(
                type='Applicant',
                id='mgennart',
                container=licence
            )
        applicant.setPersonTitle('madam')
        self.assertFalse(licence.hasMultipleApplicants())
        self.assertTrue(licence.hasSingleFemaleApplicant())

    def test_parcel_indexing_on_licence(self):
        licence = self.licences[0]
        catalog = api.portal.get_tool('portal_catalog')

        licence_id = licence.id

        licence_brain = catalog(id=licence_id)[0]
        # so far, the index should be empty as  this licence contains no parcel
        self.assertFalse(licence_brain.parcelInfosIndex)

        # add a parcel1, the index should now contain this parcel reference
        api.content.create(container=licence, type='Parcel', id='parcel1', division='A', section='B', radical='6', exposant='D')
        parcel_1 = licence.parcel1
        licence_brain = catalog(id=licence_id)[0]
        self.assertIn(parcel_1.get_capakey(), licence_brain.parcelInfosIndex)

        # add a parcel2, the index should now contain the two parcel references
        api.content.create(container=licence, type='Parcel', id='parcel2', division='AA', section='B', radical='69', exposant='E')
        parcel_2 = licence.parcel2
        licence_brain = catalog(id=licence_id)[0]
        self.assertIn(parcel_1.get_capakey(), licence_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), licence_brain.parcelInfosIndex)

        # we remove parcel1, the ref of parcel2 should be the only remaining
        # one, the index
        licence.manage_delObjects(['parcel1'])
        licence_brain = catalog(id=licence_id)[0]
        self.assertNotIn(parcel_1.get_capakey(), licence_brain.parcelInfosIndex)
        self.assertIn(parcel_2.get_capakey(), licence_brain.parcelInfosIndex)
