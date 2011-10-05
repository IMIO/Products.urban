# -*- coding: utf-8 -*-
import unittest
from DateTime import DateTime
from OFS.ObjectManager import BeforeDeleteException
from zope.component import createObject
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL


class TestBuildLicenceInquiries(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        urban = portal.urban
        self.buildLicences = urban.buildlicences
        LICENCE_ID = 'licence1'
        login(portal, 'urbaneditor')
        self.buildLicences.invokeFactory('BuildLicence', LICENCE_ID)
        self.buildLicence = getattr(self.buildLicences, LICENCE_ID)

    def _addInquiry(self):
        """
          Helper method for adding an Inquiry object
        """
        INQUIRY_ID = "inquiry"
        i = 1
        while hasattr(self.buildLicence, INQUIRY_ID + str(i)):
            i = i + 1
        inquiryId = self.buildLicence.invokeFactory("Inquiry",
                id=INQUIRY_ID + str(i))
        return getattr(self.buildLicence, inquiryId)

    def testGenericLicenceGetInquiries(self):
        """
          Test the GenericLicence.getInquiries method
        """
        # by default, no inquiry is defined
        self.assertEqual(self.buildLicence.getInquiries(), [])
        # to get at least one inquiry, we have to define a
        # investigationStart on the licence
        startDate = DateTime('01/01/2011')
        self.buildLicence.setInvestigationStart(startDate)
        self.assertEqual(self.buildLicence.getInquiries(),
                [self.buildLicence, ])
        # we can add extra inquiries by adding "Inquiry" objects
        inquiry = self._addInquiry()
        self.assertEqual(self.buildLicence.getInquiries(),
                [self.buildLicence, inquiry])
        # special case, if we remove the defined investigationStart
        # date on the licence
        #this is still considered as an Inquiry because an extra Inquiry exists
        startDate = None
        self.buildLicence.setInvestigationStart(startDate)
        self.assertEqual(self.buildLicence.getInquiries(),
                [self.buildLicence, inquiry])

    def testGenericLicenceGetUrbanEventInquiries(self):
        """
          Test the GenericLicence.getUrbanEventInquiries method
        """
        #by default, no UrbanEventInquiries exist
        self.assertEqual(self.buildLicence.getUrbanEventInquiries(), [])
        #we can not add an urbanEventInquiry if no inquiry is defined
        self.assertRaises(ValueError, createObject, 'UrbanEventInquiry',
                'enquete-publique', self.buildLicence)
        #define an inquiry on the licence so we can add an UrbanEventInquiry
        startDate = DateTime('01/01/2011')
        self.buildLicence.setInvestigationStart(startDate)
        createObject('UrbanEventInquiry', 'enquete-publique',
                self.buildLicence)
        self.assertEquals(len(self.buildLicence.getUrbanEventInquiries()), 1)
        # we can not add a second urbanEventInquiry if only one inquiry
        # is defined
        self.assertRaises(ValueError, createObject, 'UrbanEventInquiry',
                'enquete-publique', self.buildLicence)
        #after adding a second Inquiry...
        self._addInquiry()
        #... we can add a supplementary UrbanEventInquiry
        createObject('UrbanEventInquiry', 'enquete-publique',
                self.buildLicence)
        self.assertEquals(len(self.buildLicence.getUrbanEventInquiries()), 2)

    def testUrbanEventInquiryGetLinkedInquiry(self):
        """
          Test the UbanEventInquiry.getLinkedInquiry method
          There is a "1 to 1" link between an Inquiry and an UrbanEventInquiry
          (if exists)
          An Inquiry can exist alone but an UrbanEventInquiry must be linekd to
          an existing Inquiry
        """
        #define an inquiry on the licence so we can add an UrbanEventInquiry
        startDate = DateTime('01/01/2011')
        self.buildLicence.setInvestigationStart(startDate)
        #the buildLicence is finally the 'inquiry1'
        inquiry1 = self.buildLicence
        #now we can create an UrbanEventInquiry
        urbanEventInquiry1 = createObject('UrbanEventInquiry',
                'enquete-publique', self.buildLicence)
        self.assertEquals(urbanEventInquiry1.getLinkedInquiry(), inquiry1)
        # define a second Inquiry so we will be able to add a second
        # UrbanEventInquiry
        inquiry2 = self._addInquiry()
        urbanEventInquiry2 = createObject('UrbanEventInquiry',
                'enquete-publique', self.buildLicence)
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
        #define an inquiry on the licence so we can add an UrbanEventInquiry
        startDate = DateTime('01/01/2011')
        self.buildLicence.setInvestigationStart(startDate)
        #the buildLicence is finally the 'inquiry1'
        inquiry1 = self.buildLicence
        #maybe no UrbanEventInquiry is linked
        self.assertEquals(inquiry1.getLinkedUrbanEventInquiry(), None)
        #now we can create an UrbanEventInquiry
        urbanEventInquiry1 = createObject('UrbanEventInquiry',
                'enquete-publique', self.buildLicence)
        self.assertEquals(inquiry1.getLinkedUrbanEventInquiry(),
                urbanEventInquiry1)
        # define a second Inquiry so we will be able to add a second
        # UrbanEventInquiry
        inquiry2 = self._addInquiry()
        urbanEventInquiry2 = createObject('UrbanEventInquiry',
                'enquete-publique', self.buildLicence)
        self.assertEquals(inquiry2.getLinkedUrbanEventInquiry(),
                urbanEventInquiry2)
        #and test that getting the first linked inqury still works
        self.assertEquals(inquiry1.getLinkedUrbanEventInquiry(),
                urbanEventInquiry1)

    def testCanNotDeleteFirstInquiryIfLinkedToUrbanEventInquiryValidator(self):
        """
          We can not remove an existing Inquiry if it is linked to an
          UrbanEventInquiry
          This is done in the user interface by the investigationStart
          validator
        """
        # by default, startDate is None
        startDate = None
        # no message is returned by the validator if no UrbanEventInquiry is
        # defined
        #no matter what is passed to the validator : None here...
        self.assertEquals(self.buildLicence.validate_investigationStart(
            startDate), None)
        startDate = DateTime('01/01/2011')
        #... or a date here
        self.buildLicence.setInvestigationStart(startDate)
        self.assertEquals(self.buildLicence.validate_investigationStart(
            startDate), None)
        #add an UrbanEventInquiry
        createObject('UrbanEventInquiry', 'enquete-publique',
                self.buildLicence)
        # now that an UrbanEventInquiry is linked to the inquiry, we can not
        # remove the defined date
        startDate = None
        self.assertNotEquals(self.buildLicence.validate_investigationStart(
            startDate), None)
        #but we can change the date
        startDate = DateTime('01/02/2011')
        self.assertEquals(self.buildLicence.validate_investigationStart(
            startDate), None)

    def testCanNotDeleteNextInquiriesIfLinked(self):
        """
          The first Inquiry is tested here above
          If we have several inquiries, the behaviour is the same : we can not
          remove an Inquiry that is already linked an UrbanEventInquiry
          Here, for the next inquiries, we use a zope event 'onDelete'
        """
        #the first inquiry already tested...
        startDate = DateTime('01/01/2011')
        self.buildLicence.setInvestigationStart(startDate)
        createObject('UrbanEventInquiry', 'enquete-publique',
                self.buildLicence)
        #now test next inquiries
        inquiry2 = self._addInquiry()
        urbanEventInquiry2 = createObject('UrbanEventInquiry',
                'enquete-publique', self.buildLicence)
        #we can not delete the inquiry2 as urbanEventInquiry2 exists
        self.assertRaises(BeforeDeleteException,
                self.buildLicence.manage_delObjects, inquiry2.id)
        #if we delete urbanEventInquiry2...
        self.buildLicence.manage_delObjects(urbanEventInquiry2.id)
        #... then now we can remove the inquiry2
        self.buildLicence.manage_delObjects(inquiry2.id)

    def testCanNotDeleteUrbanEventInquiryIfNotTheLast(self):
        """
          To keep a logical behaviour, we can only remove the last
          UrbanEventInquiry
        """
        #add 3 inquiries and 3 linked UrbanEventInquiries
        startDate = DateTime('01/01/2011')
        self.buildLicence.setInvestigationStart(startDate)
        urbanEventInquiry1 = createObject('UrbanEventInquiry',
                'enquete-publique', self.buildLicence)
        self._addInquiry()
        urbanEventInquiry2 = createObject('UrbanEventInquiry',
                'enquete-publique', self.buildLicence)
        self._addInquiry()
        urbanEventInquiry3 = createObject('UrbanEventInquiry',
                'enquete-publique', self.buildLicence)
        #we cannot not remove an UrbanEventInquiry if it is not the last
        self.assertRaises(BeforeDeleteException,
                self.buildLicence.manage_delObjects, urbanEventInquiry2.id)
        self.assertRaises(BeforeDeleteException,
                self.buildLicence.manage_delObjects, urbanEventInquiry1.id)
        #removing UrbanEventInquiries by the last works
        self.buildLicence.manage_delObjects(urbanEventInquiry3.id)
        self.buildLicence.manage_delObjects(urbanEventInquiry2.id)
        self.buildLicence.manage_delObjects(urbanEventInquiry1.id)
