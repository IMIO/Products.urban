# -*- coding: utf-8 -*-
import unittest2 as unittest
from Products.urban.config import URBAN_TYPES
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
        login(portal, 'urbaneditor')

        # create a test EnvClassOne licence
        self.licences = []
        for content_type in URBAN_TYPES:
            licence_folder = utils.getLicenceFolder(content_type)
            testlicence_id = 'test_{}'.format(content_type.lower())
            licence_folder.invokeFactory(content_type, id=testlicence_id)
            test_licence = getattr(licence_folder, testlicence_id)
            self.licences.append(test_licence)
        transaction.commit()

    def tearDown(self):
        for licence in self.licences:
            api.content.delete(licence)
            transaction.commit()

    def test_has_single_applicant(self):
        licence = self.licences[0]
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
        applicant1 = api.content.create(
            type='Applicant',
            id='fngaha',
            container=licence1
        )
        applicant1.setPersonTitle('mister')
        applicant2 = api.content.create(
            type='Applicant',
            id='sdelcourt',
            container=licence1
        )
        applicant2.setPersonTitle('mister')
        licence2 = self.licences[0]
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
        applicant = api.content.create(
            type='Applicant',
            id='mgennart',
            container=licence
        )
        applicant.setPersonTitle('madam')
        self.assertFalse(licence.hasMultipleApplicants())
        self.assertTrue(licence.hasSingleFemaleApplicant())
