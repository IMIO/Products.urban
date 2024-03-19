# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_LICENCES_FUNCTIONAL
from Products.urban.tests.helpers import SchemaFieldsTestCase
from datetime import datetime
from plone import api
from plone.app.testing import login
from plone.app.testing import logout

import unittest


class TestCODTBuildLicence(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        portal = self.layer["portal"]
        self.portal = portal
        login(self.portal, self.layer.default_user)
        self.portal_urban = portal.portal_urban
        event_config = self.portal_urban.codt_buildlicence.urbaneventtypes["depot-de-la-demande"]

        self.licence_1 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 1",
        )
        self.licence_1.setProcedureChoice("simple")
        event = self.licence_1.createUrbanEvent(event_config)
        event.setEventDate(datetime(2024, 3, 31))

        self.licence_1_prorogated = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 1 prorogated",
        )
        self.licence_1_prorogated.setProrogation(True)
        self.licence_1_prorogated.setProcedureChoice("simple")
        event = self.licence_1_prorogated.createUrbanEvent(event_config)
        event.setEventDate(datetime(2024, 3, 31))

        self.licence_2 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 2",
        )
        self.licence_2.setProcedureChoice("simple")
        event = self.licence_2.createUrbanEvent(event_config)
        event.setEventDate(datetime(2024, 4, 1))

        self.licence_2_prorogated = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 2 prorogated",
        )
        self.licence_2_prorogated.setProrogation(True)
        self.licence_2_prorogated.setProcedureChoice("simple")
        event = self.licence_2_prorogated.createUrbanEvent(event_config)
        event.setEventDate(datetime(2024, 4, 1))

        logout()
        login(portal, "urbaneditor")

    def tearDown(self):
        login(self.portal, self.layer.default_user)
        api.content.delete(self.licence_1)
        api.content.delete(self.licence_1_prorogated)
        api.content.delete(self.licence_2)
        api.content.delete(self.licence_2_prorogated)

    def test_getProrogationDelay(self):
        self.assertEqual("30 days", self.licence_1.getProrogationDelay())
        self.assertEqual("20 days", self.licence_2.getProrogationDelay())
        self.assertEqual(30, self.licence_1.getProrogationDelay(text_format=False))
        self.assertEqual(20, self.licence_2.getProrogationDelay(text_format=False))

    def test_getProrogationDelays(self):
        self.assertEqual("60j", self.licence_1.getProrogationDelays())
        self.assertEqual("60j", self.licence_1_prorogated.getProrogationDelays())
        self.assertEqual("50j", self.licence_2.getProrogationDelays())
        self.assertEqual("50j", self.licence_2_prorogated.getProrogationDelays())

    def test_getProcedureDelays(self):
        self.assertEqual("30j", self.licence_1.getProcedureDelays())
        self.assertEqual("60j", self.licence_1_prorogated.getProcedureDelays())
        self.assertEqual("30j", self.licence_2.getProcedureDelays())
        self.assertEqual("50j", self.licence_2_prorogated.getProcedureDelays())

    def test_is_CODT2024(self):
        self.assertFalse(self.licence_1.is_CODT2024())
        self.assertTrue(self.licence_2.is_CODT2024())

    def test_is_not_CODT2024(self):
        self.assertTrue(self.licence_1.is_not_CODT2024())
        self.assertFalse(self.licence_2.is_not_CODT2024())