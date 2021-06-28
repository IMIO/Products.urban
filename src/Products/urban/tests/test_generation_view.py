# -*- coding: utf-8 -*-
from Products.urban.testing import URBAN_TESTS_LICENCES_FUNCTIONAL

from plone.app.testing import login

import unittest
from Products.urban.docgen.helper_view import UrbanDocGenerationEventHelperView


class TestUrbanGenerationView(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.buildlicence = portal.urban.buildlicences.objectValues('BuildLicence')[0]
        self.portal_urban = portal.portal_urban
        login(portal, 'urbaneditor')

    def test_get_base_generation_context(self):
        inspections = self.portal.urban.inspections
        inspections.invokeFactory('Inspection', id='inspection1')
        new_inspection = inspections.inspection1

        new_inspection.invokeFactory('Plaintiff', id='plaintiff1', name1='Renée', name2='Black')
        new_inspection.invokeFactory('Proprietary', id='proprietary1', name1='Ursula', name2='Frei')
        new_inspection.invokeFactory('Tenant', id='tenant1', name1='Aeron', name2='Lorelei')
        new_event = new_inspection.createUrbanEvent('rapport')
        docgen_view = new_event.restrictedTraverse('urban-document-generation')
        gener_ctx = docgen_view.get_base_generation_context()

        self.assertIsInstance(gener_ctx['plaintiffobj'], UrbanDocGenerationEventHelperView)
        self.assertIsInstance(gener_ctx['proprietaryobj'], UrbanDocGenerationEventHelperView)
        self.assertIsInstance(gener_ctx['tenantobj'], UrbanDocGenerationEventHelperView)
