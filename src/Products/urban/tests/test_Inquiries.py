# -*- coding: utf-8 -*-
import unittest
from DateTime import DateTime
from OFS.ObjectManager import BeforeDeleteException
from zope.component import createObject
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_LICENCES


class TestBuildLicenceInquiries(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.buildlicence = portal.urban.buildlicences.objectValues()[0]
        login(portal, 'urbaneditor')

    def _addInquiry(self):
        """
          Helper method for adding an Inquiry object
        """
        INQUIRY_ID = "inquiry"
        i = 1
        while hasattr(self.buildlicence, INQUIRY_ID + str(i)):
            i = i + 1
        inquiryId = self.buildlicence.invokeFactory("Inquiry", id=INQUIRY_ID + str(i))
        return getattr(self.buildlicence, inquiryId)

    def testGenericLicenceGetInquiries(self):
        """
          Test the GenericLicence.getInquiries method
        """
        buildlicence = self.buildlicence
        # by default, an inquiry is already defined defined on the licence
        self.assertEqual(buildlicence.getInquiries(), [buildlicence, ])
        # we can add extra inquiries by adding "Inquiry" objects
        inquiry = self._addInquiry()
        self.assertEqual(buildlicence.getInquiries(), [buildlicence, inquiry])
        # special case, if we remove the defined investigationStart
        # date on the licence
        #this is still considered as an Inquiry because an extra Inquiry exists
        startDate = None
        buildlicence.setInvestigationStart(startDate)
        self.assertEqual(buildlicence.getInquiries(), [buildlicence, inquiry])

    def testGenericLicenceGetUrbanEventInquiries(self):
        """
          Test the GenericLicence.getUrbanEventInquiries method
        """
        buildlicence = self.buildlicence
        # by default, an inquiry is already defined defined on the licence
        self.assertEquals(len(buildlicence.getUrbanEventInquiries()), 1)
        # we can not add a second urbanEventInquiry if only one inquiry
        # is defined
        self.assertRaises(ValueError, createObject, 'UrbanEventInquiry', 'enquete-publique', buildlicence)
        #after adding a second Inquiry...
        self._addInquiry()
        #... we can add a supplementary UrbanEventInquiry
        createObject('UrbanEventInquiry', 'enquete-publique', buildlicence)
        self.assertEquals(len(buildlicence.getUrbanEventInquiries()), 2)

    def testUrbanEventInquiryGetLinkedInquiry(self):
        """
          Test the UbanEventInquiry.getLinkedInquiry method
          There is a "1 to 1" link between an Inquiry and an UrbanEventInquiry
          (if exists)
          An Inquiry can exist alone but an UrbanEventInquiry must be linekd to
          an existing Inquiry
        """
        buildlicence = self.buildlicence
        #the buildlicence is the 'inquiry1'
        inquiry1 = buildlicence
        #now we can create an UrbanEventInquiry
        urbanEventInquiry1 = buildlicence.objectValues('UrbanEventInquiry')[0]
        self.assertEquals(urbanEventInquiry1.getLinkedInquiry(), inquiry1)
        # define a second Inquiry so we will be able to add a second
        # UrbanEventInquiry
        inquiry2 = self._addInquiry()
        urbanEventInquiry2 = createObject('UrbanEventInquiry', 'enquete-publique', buildlicence)
        self.assertEquals(urbanEventInquiry2.getLinkedInquiry(), inquiry2)
        #and test that getting the first linked inqury still works
        self.assertEquals(urbanEventInquiry1.getLinkedInquiry(), inquiry1)

    def testInquiryGetUrbanEventLinkedInquiry(self):
        """
          Test the Inquiry.getUrbanEventLinkedInquiry method
          There is a "1 to 1" link between an Inquiry and an UrbanEventInquiry
          (if exists)
          An Inquiry can exist alone but an UrbanEventInquiry must be linekd to
          an existing Inquiry
        """
        buildlicence = self.buildlicence
        #delete default inquiry event
        oldinquiry_id = buildlicence.objectValues('UrbanEventInquiry')[0].id
        buildlicence.manage_delObjects(oldinquiry_id)
        #define an inquiry on the licence so we can add an UrbanEventInquiry
        startDate = DateTime('01/01/2011')
        buildlicence.setInvestigationStart(startDate)
        #the buildLicence is finally the 'inquiry1'
        inquiry1 = buildlicence
        #maybe no UrbanEventInquiry is linked
        self.assertEquals(inquiry1.getLinkedUrbanEventInquiry(), None)
        #now we can create an UrbanEventInquiry
        urbanEventInquiry1 = createObject('UrbanEventInquiry', 'enquete-publique', buildlicence)
        self.assertEquals(inquiry1.getLinkedUrbanEventInquiry(), urbanEventInquiry1)
        # define a second Inquiry so we will be able to add a second
        # UrbanEventInquiry
        inquiry2 = self._addInquiry()
        urbanEventInquiry2 = createObject('UrbanEventInquiry', 'enquete-publique', buildlicence)
        self.assertEquals(inquiry2.getLinkedUrbanEventInquiry(), urbanEventInquiry2)
        #and test that getting the first linked inqury still works
        self.assertEquals(inquiry1.getLinkedUrbanEventInquiry(), urbanEventInquiry1)

    def testCanNotDeleteFirstInquiryIfLinkedToUrbanEventInquiryValidator(self):
        """
          We can not remove an existing Inquiry if it is linked to an
          UrbanEventInquiry
          This is done in the user interface by the investigationStart
          validator
        """
        buildlicence = self.buildlicence
        #delete default inquiry event
        oldinquiry_id = buildlicence.objectValues('UrbanEventInquiry')[0].id
        buildlicence.manage_delObjects(oldinquiry_id)
        # set startDate is None
        startDate = None
        buildlicence.setInvestigationStart(startDate)
        # no message is returned by the validator if no UrbanEventInquiry is
        # defined
        #no matter what is passed to the validator : None here...
        self.assertEquals(buildlicence.validate_investigationStart(startDate), None)
        startDate = DateTime('01/01/2011')
        #... or a date here
        buildlicence.setInvestigationStart(startDate)
        self.assertEquals(buildlicence.validate_investigationStart(startDate), None)
        #add an UrbanEventInquiry
        createObject('UrbanEventInquiry', 'enquete-publique', buildlicence)
        # now that an UrbanEventInquiry is linked to the inquiry, we can not
        # remove the defined date
        startDate = None
        self.assertNotEquals(buildlicence.validate_investigationStart(
            startDate), None)
        #but we can change the date
        startDate = DateTime('01/02/2011')
        self.assertEquals(buildlicence.validate_investigationStart(
            startDate), None)

    def testCanNotDeleteNextInquiriesIfLinked(self):
        """
          The first Inquiry is tested here above
          If we have several inquiries, the behaviour is the same : we can not
          remove an Inquiry that is already linked an UrbanEventInquiry
          Here, for the next inquiries, we use a zope event 'onDelete'
        """
        buildlicence = self.buildlicence
        #now test next inquiries
        inquiry2 = self._addInquiry()
        urbanEventInquiry2 = createObject('UrbanEventInquiry', 'enquete-publique', buildlicence)
        #we can not delete the inquiry2 as urbanEventInquiry2 exists
        self.assertRaises(BeforeDeleteException, buildlicence.manage_delObjects, inquiry2.id)
        #if we delete urbanEventInquiry2...
        buildlicence.manage_delObjects(urbanEventInquiry2.id)
        #... then now we can remove the inquiry2
        buildlicence.manage_delObjects(inquiry2.id)

    def testCanNotDeleteUrbanEventInquiryIfNotTheLast(self):
        """
          To keep a logical behaviour, we can only remove the last
          UrbanEventInquiry
        """
        buildlicence = self.buildlicence
        #add 3 inquiries and 3 linked UrbanEventInquiries
        urbanEventInquiry1 = buildlicence.objectValues('UrbanEventInquiry')[0]
        self._addInquiry()
        urbanEventInquiry2 = createObject('UrbanEventInquiry', 'enquete-publique', buildlicence)
        self._addInquiry()
        urbanEventInquiry3 = createObject('UrbanEventInquiry', 'enquete-publique', buildlicence)
        #we cannot not remove an UrbanEventInquiry if it is not the last
        self.assertRaises(BeforeDeleteException,
                          buildlicence.manage_delObjects, urbanEventInquiry2.id)
        self.assertRaises(BeforeDeleteException,
                          buildlicence.manage_delObjects, urbanEventInquiry1.id)
        #removing UrbanEventInquiries by the last works
        buildlicence.manage_delObjects(urbanEventInquiry3.id)
        buildlicence.manage_delObjects(urbanEventInquiry2.id)
        buildlicence.manage_delObjects(urbanEventInquiry1.id)
