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
        # mdhyne, to do -> populate inspection with tenants and plaintiffs
        inspection_cfg = new_inspection.getLicenceConfig()
        new_event = new_inspection.createUrbanEvent(urban_event_type=event_cfg.UID())
        docgen_view = new_event.restrictedTraverse('urban-document-generation')
        # mdhyne, to do -> call the method we want to test
        # mdhyne, to do -> evaluate that the result is the one we want ;-)

