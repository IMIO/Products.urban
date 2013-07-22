# -*- coding: utf-8 -*-
import unittest
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL
from Products.CMFCore.utils import getToolByName
from Products.urban.config import URBAN_TYPES
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban import UrbanEventInquiry
from zope.event import notify
from Products.Archetypes.event import EditBegunEvent


class TestDefaultValues(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.site = portal
        self.buildlicences = portal.urban.buildlicences
        login(portal, 'urbanmanager')

    """
    Tests for the configurable listing default values
    """

    def createNewLicence(self):
        buildlicences = self.buildlicences
        buildlicences.invokeFactory('BuildLicence', id='newlicence', title='blabla')
        newlicence = buildlicences.newlicence
        #simulate edition events to trigger default value system
        notify(EditBegunEvent(newlicence))
        return newlicence

    def testNoDefaultValuesConfigured(self):
        #create a new buildlicence
        newlicence = self.createNewLicence()
        #any configurable selection field should be empty by default
        self.assertEqual(True, not newlicence.getWorkType())
        self.assertEqual('', newlicence.getFolderCategory())
        self.assertEqual(True, not newlicence.getMissingParts())

    def testSingleSelectionFieldWithOneDefaultValue(self):
        #configure a default value for the field 'folder category'
        vocabulary_term = self.portal_urban.buildlicence.foldercategories.objectValues()[0]
        vocabulary_term.setIsDefaultValue(True)
        #create a new buildlicence
        newlicence = self.createNewLicence()
        #the value of folderCategory should be the one marked as default value
        self.assertEqual([vocabulary_term.id], newlicence.getFolderCategory())

    def testMultiSelectionFieldWithOneDefaultValue(self):
        #configure a default value for the field 'missing parts'
        vocabulary_term = self.portal_urban.buildlicence.missingparts.objectValues()[0]
        vocabulary_term.setIsDefaultValue(True)
        #create a new buildlicence
        newlicence = self.createNewLicence()
        #the value of missing parts should be the one marked as default value
        self.assertEqual((vocabulary_term.id, ), newlicence.getMissingParts())

    def testSingleSelectionFieldWithMultipleDefaultValues(self):
        #configure a default value for the field 'folder category'
        vocabulary_term_1 = self.portal_urban.buildlicence.foldercategories.objectValues()[0]
        vocabulary_term_1.setIsDefaultValue(True)
        vocabulary_term_2 = self.portal_urban.buildlicence.foldercategories.objectValues()[2]
        vocabulary_term_2.setIsDefaultValue(True)
        #create a new buildlicence
        newlicence = self.createNewLicence()
        #the value of folderCategory should be the one marked as default value
        self.assertEqual([vocabulary_term_1.id, vocabulary_term_2.id], newlicence.getFolderCategory())

    def testMultiSelectionFieldWithMultiplesDefaultValues(self):
        #configure a default value for the field 'missing parts'
        vocabulary_term_1 = self.portal_urban.buildlicence.missingparts.objectValues()[0]
        vocabulary_term_1.setIsDefaultValue(True)
        vocabulary_term_2 = self.portal_urban.buildlicence.missingparts.objectValues()[2]
        vocabulary_term_2.setIsDefaultValue(True)
        #create a new buildlicence
        newlicence = self.createNewLicence()
        #the value of missing parts should be the one marked as default value
        self.assertEqual((vocabulary_term_1.id, vocabulary_term_2.id, ), newlicence.getMissingParts())

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

    """
    Tests for the text default values
    """
    def testNoTextDefaultValuesConfigured(self):
        #create a new buildlicence
        newlicence = self.createNewLicence()
        #text fields should be empty by default
        self.assertEqual('<p></p>', newlicence.Description())

    def testTextValueConfigured(self):
        licence_config = self.site.portal_urban.buildlicence
        #set the default text value fotr the fdescription field
        default_text = '<p>Bla bla</p>'
        licence_config.setTextDefaultValues(({'text': default_text, 'fieldname': 'description'}, ))
        #any new licence should have this text as value for the description field
        newlicence = self.createNewLicence()
        self.assertEquals(default_text, newlicence.Description())

    def testDefaultTextMethodIsDefinedForEachTextField(self):
        #each text field  should have the 'getDefaultText' method defined on it, else the default value system wont work
        site = self.site
        catalog = getToolByName(site, 'portal_catalog')
        test_licences = [brain.getObject() for brain in catalog(portal_type=URBAN_TYPES)]
        for licence in test_licences:
            for field in licence.schema.fields():
                if hasattr(field, 'defaut_content_type') and field.default_content_type.startswith('text'):
                    self.assertEquals(field.default_method, 'getDefaultText')


class TestEventDefaultValues(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.site = portal
        login(portal, 'urbanmanager')
        #create a licence
        buildlicences = portal.urban.buildlicences
        buildlicences.invokeFactory('BuildLicence', id='newlicence', title='blabla')
        buildlicence = buildlicences.newlicence
        self.licence = buildlicence

    def createEvent(self, licence, event_type):
        self.portal_urban.createUrbanEvent(licence.UID(), event_type.UID())
        urban_event = licence.objectValues('UrbanEvent')[-1]
        #simulate edition event to trigger default value system
        notify(EditBegunEvent(urban_event))
        return urban_event

    """
    Tests for the text default values
    """
    def testNoTextDefaultValuesConfigured(self):
        #create a new event 'rappor du college'
        #text field 'decisionText' should be empty by default
        eventtypes = self.portal_urban.buildlicence.urbaneventtypes
        event_type = getattr(eventtypes, 'rapport-du-college')
        event = self.createEvent(self.licence, event_type)
        decision_text = event.getDecisionText()
        self.failUnless(decision_text == '')

    def testTextValueConfigured(self):
        eventtypes = self.portal_urban.buildlicence.urbaneventtypes
        event_type = getattr(eventtypes, 'rapport-du-college')
        # set a a default text for the field 'decsionText'
        default_text = '<p>Kill bill!</p>'
        event_type.setTextDefaultValues([{'text': default_text, 'fieldname': 'decisionText'}])
        # the created event should have this text in its field 'decisionText'
        event = self.createEvent(self.licence, event_type)
        decision_text = event.getDecisionText()
        self.failUnless(decision_text == default_text)

    def testTextValueConfiguredWithPythonExpression(self):
        eventtypes = self.portal_urban.buildlicence.urbaneventtypes
        event_type = getattr(eventtypes, 'rapport-du-college')
        # set a a default text for the field 'decsionText'
        default_text = '<p>Kill [[python: folder.Title()]] and [[python: object.getId()]] </p>'
        event_type.setTextDefaultValues([{'text': default_text, 'fieldname': 'decisionText'}])
        # the created event should have this text in its field 'decisionText'
        event = self.createEvent(self.licence, event_type)
        decision_text = event.getDecisionText()

        expected_text = '<p>Kill %s and %s </p>' % (self.licence.Title(), event.getId())
        self.failUnless(decision_text == expected_text)

    def testDefaultTextMethodIsDefinedForEachTextField(self):
        #each text field  should have the 'getDefaultText' method defined on it, else the default value system wont work
        for field in UrbanEventInquiry.UrbanEventInquiry_schema.fields():
            if hasattr(field, 'defaut_content_type') and field.default_content_type.startswith('text'):
                self.assertEquals(field.default_method, 'getDefaultText')
