# -*- coding: utf-8 -*-
from Products.urban.testing import URBAN_TESTS_LICENCES_FUNCTIONAL

from plone.app.testing import login

import transaction
import unittest


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
        new_inspection_id = inspections.invokeFactory('Inspection', id='inspection1')
        new_inspection = inspections.inspection1
        # populate inspection with tenants and plaintiffs
        inspection_cfg = new_inspection.getLicenceConfig()
        import ipdb; ipdb.set_trace()
