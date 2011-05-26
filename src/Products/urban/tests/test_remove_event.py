# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.component import createObject
from plone.app.testing import quickInstallProduct, login
from plone.app.testing import setRoles
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.app.testing.interfaces import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from Products.urban.testing import URBAN_TESTS_PROFILE_INTEGRATION


class TestRemoveEvent(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_INTEGRATION
    
    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.folderBuildLicences=self.portal.urban.buildlicences
        self.tool=getToolByName(self.portal, "portal_urban")
        
    def test_removeEventParcel(self):
        self.folderBuildLicences.invokeFactory('BuildLicence', 'buildLicence')
        self.folderBuildLicences.buildLicence.invokeFactory('PortionOut', 'portionOut')
        portionOut=self.folderBuildLicences.buildLicence.portionOut
        self.folderBuildLicences.buildLicence.reindexObject()
        resParcel=self.tool.searchByParcel("BuildLicence", portionOut.getDivision(), portionOut.getSection(), portionOut.getRadical(), portionOut.getBis(), portionOut.getExposant(), portionOut.getPuissance(), portionOut.getPartie())
        self.assertEqual(len(resParcel), 1) 
        self.folderBuildLicences.buildLicence.manage_delObjects(["portionOut"])
        self.folderBuildLicences.buildLicence.reindexObject()
        resParcel=self.tool.searchByParcel("BuildLicence", portionOut.getDivision(), portionOut.getSection(), portionOut.getRadical(), portionOut.getBis(), portionOut.getExposant(), portionOut.getPuissance(), portionOut.getPartie())
        self.assertEqual(len(resParcel), 0)
        
    def test_removeEventApplicant(self):
        pass