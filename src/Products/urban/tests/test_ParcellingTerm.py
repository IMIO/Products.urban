# -*- coding: utf-8 -*-
import unittest2 as unittest
from Products.CMFCore.utils import getToolByName
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_CONFIG


class TestParcellingTerm(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer["portal"]
        self.portal = portal
        self.parcellingterm = portal.urban.parcellings.objectValues()[0]
        self.portal_urban = portal.portal_urban
        login(self.portal, self.layer.default_user)

    def testParcellingTitleUpdate(self):
        parcelling = self.parcellingterm
        self.assertTrue(
            parcelling.Title()
            == "Lotissement 1 (Andr\xc3\xa9 Ledieu - 01/01/2005 - 10)"
        )
        # after adding a parcel1, title should be updated with the base
        # references  of this parcel (here:  A, B, C but not D)
        parcelling.invokeFactory(
            "PortionOut",
            "parcel1",
            division="A",
            section="B",
            radical="6",
            exposant="D",
        )
        self.assertTrue(
            parcelling.Title()
            == 'Lotissement 1 (Andr\xc3\xa9 Ledieu - Jan 01, 2005 - "A B 6")'
        )

        # after adding a parcel2 with the same base refs, the title
        # should not change
        parcelling.invokeFactory(
            "PortionOut",
            "parcel2",
            division="A",
            section="B",
            radical="6",
            exposant="E",
        )
        self.assertTrue(
            parcelling.Title()
            == 'Lotissement 1 (Andr\xc3\xa9 Ledieu - Jan 01, 2005 - "A B 6")'
        )

        # after adding a parcel3 with different base refs, the title
        # should be updated
        parcelling.invokeFactory(
            "PortionOut",
            "parcel3",
            division="AA",
            section="BB",
            radical="69",
            exposant="D",
        )
        self.assertTrue(
            parcelling.Title()
            == 'Lotissement 1 (Andr\xc3\xa9 Ledieu - Jan 01, 2005 - "AA BB 69", "A B 6")'
        )

        # we remove parcel1 and parcel2, title should change to only
        # keep the base refs of parcel3
        parcelling.manage_delObjects(["parcel1", "parcel2"])
        self.assertTrue(
            parcelling.Title()
            == 'Lotissement 1 (Andr\xc3\xa9 Ledieu - Jan 01, 2005 - "AA BB 69")'
        )

    def testParcellingIndexing(self):
        catalog = getToolByName(self.portal, "portal_catalog")

        parcelling = self.parcellingterm
        parcelling_id = parcelling.id

        parcelling_brain = catalog(id=parcelling_id)[0]
        # so far, the index should be empty as  this parcelling contains no parcel
        self.assertFalse(parcelling_brain.parcelInfosIndex)

        # add a parcel1, the index should now contain this parcel reference
        parcelling.invokeFactory(
            "PortionOut",
            "parcel1",
            division="A",
            section="B",
            radical="6",
            exposant="D",
        )
        parcel_1 = parcelling.parcel1
        parcelling_brain = catalog(id=parcelling_id)[0]
        self.assertTrue(parcel_1.get_capakey() in parcelling_brain.parcelInfosIndex)

        # add a parcel2, the index should now contain the two parcel references
        parcelling.invokeFactory(
            "PortionOut",
            "parcel2",
            division="AA",
            section="B",
            radical="69",
            exposant="E",
        )
        parcel_2 = parcelling.parcel2
        parcelling_brain = catalog(id=parcelling_id)[0]
        self.assertTrue(parcel_1.get_capakey() in parcelling_brain.parcelInfosIndex)
        self.assertTrue(parcel_2.get_capakey() in parcelling_brain.parcelInfosIndex)

        # we remove parcel1, the ref of parcel2 should be the only remaining
        # one in the index
        parcelling.manage_delObjects(["parcel1"])
        parcelling_brain = catalog(id=parcelling_id)[0]
        self.assertFalse(parcel_1.get_capakey() in parcelling_brain.parcelInfosIndex)
        self.assertTrue(parcel_2.get_capakey() in parcelling_brain.parcelInfosIndex)
