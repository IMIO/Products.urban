# -*- coding: utf-8 -*-


from OFS.ObjectManager import BeforeDeleteException
from Products.urban.testing import URBAN_TESTS_LICENCES_FUNCTIONAL

from plone.app.testing import login
from plone import api

import unittest


class TestUrbanStreets(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        site = self.layer["portal"]
        self.site = site
        self.buildlicence = site.urban.buildlicences.objectValues()[-1]
        self.city = site.urban.portal_urban.streets.objectValues()[-1]
        self.portal = self.layer["portal"]

    def test_streets_delete(self):
        # create a street
        wl = self.buildlicence.getWorkLocations()
        wll = list(wl)
        street_1 = self.city.objectValues()[0]
        street_2 = self.city.objectValues()[1]
        wll.append({"street": street_1.UID(), "number": "123"})
        # link licence to this first street
        self.buildlicence.setWorkLocations(tuple(wll))

        # street must not be deleted if linked to a licence
        login(self.portal, "urbanmanager")
        self.assertRaises(
            BeforeDeleteException, self.city.manage_delObjects, [street_1.id]
        )

        # delete this former street must not raise a BeforeDeleteException
        self.city.manage_delObjects([street_2.id])
