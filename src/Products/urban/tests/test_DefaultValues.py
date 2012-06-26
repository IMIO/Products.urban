# -*- coding: utf-8 -*-
import unittest
from zope.component import createObject
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL
from Products.CMFCore.utils import getToolByName
from Products.urban.config import URBAN_TYPES
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary


class TestDefaultValues(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.site = portal
        self.buildlicences = portal.urban.buildlicences
        urban = portal.urban
        login(portal, 'urbanmanager')


    def testNoDefaultValuesConfigured(self):
        buildlicences = self.buildlicences
        #create a new buildlicence
        buildlicences.invokeFactory('BuildLicence', id='newlicence',title='blabla')
        newlicence = buildlicences.newlicence
        #any configurable selection field should be empty by default
        self.assertEqual(True, not newlicence.getWorkType())
        self.assertEqual([''], newlicence.getFolderCategory())
        self.assertEqual(True, not newlicence.getMissingParts())


    def testSingleSelectionFieldWithOneDefaultValue(self):
        buildlicences = self.buildlicences
        #configure a default value for the field 'folder category'
        vocabulary_term = self.portal_urban.buildlicence.foldercategories.objectValues()[0]
        vocabulary_term.setIsDefaultValue(True)
        #create a new buildlicence
        buildlicences.invokeFactory('BuildLicence', id='newlicence',title='blabla')
        newlicence = buildlicences.newlicence
        #the value of folderCategory should be the one marked as default value
        self.assertEqual([vocabulary_term.id], newlicence.getFolderCategory())


    def testMultiSelectionFieldWithOneDefaultValue(self):
        buildlicences = self.buildlicences
        #configure a default value for the field 'missing parts'
        vocabulary_term = self.portal_urban.buildlicence.missingparts.objectValues()[0]
        vocabulary_term.setIsDefaultValue(True)
        #create a new buildlicence
        buildlicences.invokeFactory('BuildLicence', id='newlicence',title='blabla')
        newlicence = buildlicences.newlicence
        #the value of missing parts should be the one marked as default value
        self.assertEqual((vocabulary_term.id,), newlicence.getMissingParts())


    def testSingleSelectionFieldWithMultipleDefaultValues(self):
        buildlicences = self.buildlicences
        #configure a default value for the field 'folder category'
        vocabulary_term_1 = self.portal_urban.buildlicence.foldercategories.objectValues()[0]
        vocabulary_term_1.setIsDefaultValue(True)
        vocabulary_term_2 = self.portal_urban.buildlicence.foldercategories.objectValues()[2]
        vocabulary_term_2.setIsDefaultValue(True)
        #create a new buildlicence
        buildlicences.invokeFactory('BuildLicence', id='newlicence',title='blabla')
        newlicence = buildlicences.newlicence
        #the value of folderCategory should be the one marked as default value
        self.assertEqual([vocabulary_term_1.id, vocabulary_term_2.id], newlicence.getFolderCategory())


    def testMultiSelectionFieldWithMultiplesDefaultValues(self):
        buildlicences = self.buildlicences
        #configure a default value for the field 'missing parts'
        vocabulary_term_1 = self.portal_urban.buildlicence.missingparts.objectValues()[0]
        vocabulary_term_1.setIsDefaultValue(True)
        vocabulary_term_2 = self.portal_urban.buildlicence.missingparts.objectValues()[2]
        vocabulary_term_2.setIsDefaultValue(True)
        #create a new buildlicence
        buildlicences.invokeFactory('BuildLicence', id='newlicence',title='blabla')
        newlicence = buildlicences.newlicence
        #the value of missing parts should be the one marked as default value
        self.assertEqual((vocabulary_term_1.id, vocabulary_term_2.id,), newlicence.getMissingParts())


    def testDefaultValueMethodIsDefinedForEachConfigurableListing(self):
        #each field with a configurable listing (<=> has a UrbanVocabulary defined as its vocabulary) should
        #have the 'getDefaultValue' method defined on it, else the default value system wont work
        site = self.site
        catalog = getToolByName(site, 'portal_catalog')
        test_licences = [brain.getObject() for brain in catalog(portal_type=URBAN_TYPES)]
        for licence in test_licences:
            for field in licence.schema.fields():
                if isinstance(field.vocabulary, UrbanVocabulary) and field.type != 'datagrid':
                    self.assertEquals(field.default_method, 'getDefaultValue')
