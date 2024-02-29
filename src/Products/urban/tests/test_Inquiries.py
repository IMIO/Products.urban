# -*- coding: utf-8 -*-
from OFS.ObjectManager import BeforeDeleteException

from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL

from plone import api
from plone.app.testing import login
from zope.component import createObject

import transaction
import unittest


class TestBuildLicenceInquiries(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    def setUp(self):
        portal = self.layer["portal"]
        self.urban = portal.urban

        # create a test BuildLicence
        default_user = self.layer.default_user
        login(portal, default_user)
        buildlicence_folder = self.urban.buildlicences
        testlicence_id = "test_buildlicence"
        buildlicence_folder.invokeFactory("BuildLicence", id=testlicence_id)
        self.licence = getattr(buildlicence_folder, testlicence_id)

        # create un inquiry event
        createObject("UrbanEventInquiry", "enquete-publique", self.licence)
        transaction.commit()

    def _addInquiry(self):
        """
        Helper method for adding an Inquiry object
        """
        INQUIRY_ID = "inquiry"
        i = 1
        while hasattr(self.licence, INQUIRY_ID + str(i)):
            i = i + 1
        inquiryId = self.licence.invokeFactory("Inquiry", id=INQUIRY_ID + str(i))
        return getattr(self.licence, inquiryId)

    def testGenericLicenceGetInquiries(self):
        """
        Test the GenericLicence.getInquiries method
        """
        licence = self.licence
        # by default, an inquiry is already defined defined on the licence
        self.assertEqual(licence.getInquiries(), [])
        # we can add extra inquiries by adding "Inquiry" objects
        inquiry = self._addInquiry()
        self.assertEqual(licence.getInquiries(), [licence, inquiry])

    def testGenericLicenceGetUrbanEventInquiries(self):
        """
        Test the GenericLicence.getUrbanEventInquiries method
        """
        licence = self.licence
        # by default, an inquiry is already defined defined on the licence
        self.assertEquals(len(licence.getUrbanEventInquiries()), 1)
        # we can not add a second urbanEventInquiry if only one inquiry
        # is defined
        self.assertRaises(
            ValueError, createObject, "UrbanEventInquiry", "enquete-publique", licence
        )
        # after adding a second Inquiry...
        self._addInquiry()
        # ... we can add a supplementary UrbanEventInquiry
        createObject("UrbanEventInquiry", "enquete-publique", licence)
        self.assertEquals(len(licence.getUrbanEventInquiries()), 2)

    def testUrbanEventInquiryGetLinkedInquiry(self):
        """
        Test the UbanEventInquiry.getLinkedInquiry method
        There is a "1 to 1" link between an Inquiry and an UrbanEventInquiry
        (if exists)
        An Inquiry can exist alone but an UrbanEventInquiry must be linekd to
        an existing Inquiry
        """
        licence = self.licence
        # the licence is the 'inquiry1'
        inquiry1 = licence
        # now we can create an UrbanEventInquiry
        urbanEventInquiry1 = licence.objectValues("UrbanEventInquiry")[0]
        self.assertEquals(urbanEventInquiry1.getLinkedInquiry(), inquiry1)
        # define a second Inquiry so we will be able to add a second
        # UrbanEventInquiry
        inquiry2 = self._addInquiry()
        urbanEventInquiry2 = createObject(
            "UrbanEventInquiry", "enquete-publique", licence
        )
        self.assertEquals(urbanEventInquiry2.getLinkedInquiry(), inquiry2)
        # and test that getting the first linked inqury still works
        self.assertEquals(urbanEventInquiry1.getLinkedInquiry(), inquiry1)

    def testInquiryGetUrbanEventLinkedInquiry(self):
        """
        Test the Inquiry.getUrbanEventLinkedInquiry method
        There is a "1 to 1" link between an Inquiry and an UrbanEventInquiry
        (if exists)
        An Inquiry can exist alone but an UrbanEventInquiry must be linekd to
        an existing Inquiry
        """
        licence = self.licence
        # delete default inquiry event
        oldinquiry_id = licence.objectValues("UrbanEventInquiry")[0].id
        licence.manage_delObjects(oldinquiry_id)
        # the buildLicence is finally the 'inquiry1'
        inquiry1 = licence
        # maybe no UrbanEventInquiry is linked
        self.assertEquals(inquiry1.getLinkedUrbanEventInquiry(), None)
        # now we can create an UrbanEventInquiry
        urbanEventInquiry1 = createObject(
            "UrbanEventInquiry", "enquete-publique", licence
        )
        self.assertEquals(inquiry1.getLinkedUrbanEventInquiry(), urbanEventInquiry1)
        # define a second Inquiry so we will be able to add a second
        # UrbanEventInquiry
        inquiry2 = self._addInquiry()
        urbanEventInquiry2 = createObject(
            "UrbanEventInquiry", "enquete-publique", licence
        )
        self.assertEquals(inquiry2.getLinkedUrbanEventInquiry(), urbanEventInquiry2)
        # and test that getting the first linked inqury still works
        self.assertEquals(inquiry1.getLinkedUrbanEventInquiry(), urbanEventInquiry1)

    def testCanNotDeleteNextInquiriesIfLinked(self):
        """
        The first Inquiry is tested here above
        If we have several inquiries, the behaviour is the same : we can not
        remove an Inquiry that is already linked an UrbanEventInquiry
        Here, for the next inquiries, we use a zope event 'onDelete'
        """
        licence = self.licence
        # now test next inquiries
        inquiry2 = self._addInquiry()
        urbanEventInquiry2 = createObject(
            "UrbanEventInquiry", "enquete-publique", licence
        )
        # we can not delete the inquiry2 as urbanEventInquiry2 exists
        self.assertRaises(BeforeDeleteException, licence.manage_delObjects, inquiry2.id)
        # if we delete urbanEventInquiry2...
        api.content.delete(urbanEventInquiry2)
        # ... then now we can remove the inquiry2
        api.content.delete(inquiry2)

    def testCanNotDeleteUrbanEventInquiryIfNotTheLast(self):
        """
        To keep a logical behaviour, we can only remove the last
        UrbanEventInquiry
        """
        licence = self.licence
        # add 3 inquiries and 3 linked UrbanEventInquiries
        urbanEventInquiry1 = licence.objectValues("UrbanEventInquiry")[0]
        self._addInquiry()
        urbanEventInquiry2 = createObject(
            "UrbanEventInquiry", "enquete-publique", licence
        )
        self._addInquiry()
        urbanEventInquiry3 = createObject(
            "UrbanEventInquiry", "enquete-publique", licence
        )
        # we cannot not remove an UrbanEventInquiry if it is not the last
        self.assertRaises(
            BeforeDeleteException, licence.manage_delObjects, urbanEventInquiry2.id
        )
        self.assertRaises(
            BeforeDeleteException, licence.manage_delObjects, urbanEventInquiry1.id
        )
        # removing UrbanEventInquiries by the last works
        api.content.delete(urbanEventInquiry3)
        api.content.delete(urbanEventInquiry2)
        api.content.delete(urbanEventInquiry1)
