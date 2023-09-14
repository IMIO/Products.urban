# -*- coding: utf-8 -*-
import unittest

from plone.app.testing import login
from plone import api

from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.CMFCore.utils import getToolByName
from Products.urban.config import URBAN_TYPES
from Products.urban.content import UrbanEventInquiry
from Products.urban.interfaces import IUrbanEvent
from zope.lifecycleevent import ObjectCreatedEvent
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from zope.event import notify
from Products.Archetypes.event import EditBegunEvent


class TestDefaultValues(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.site = portal
        self.buildlicences = portal.urban.buildlicences
        login(portal, self.layer.default_user)

    def update_voc_cache(self, licence_config):
        with api.env.adopt_roles(['Manager']):
            voc_cache = self.portal_urban.restrictedTraverse('urban_vocabulary_cache')
            voc_cache.update_procedure_all_vocabulary_cache(licence_config)

    """
    Tests for the configurable listing default values
    """

    def createNewLicence(self):
        buildlicences = self.buildlicences
        buildlicences.invokeFactory('BuildLicence', id='newlicence', title='blabla')
        newlicence = buildlicences.newlicence
        # simulate edition events to trigger default value system
        notify(EditBegunEvent(newlicence))
        return newlicence

    def testNoDefaultValuesConfigured(self):
        # create a new buildlicence
        newlicence = self.createNewLicence()
        # any configurable selection field should be empty by default
        self.assertEqual(True, not newlicence.getWorkType())
        self.assertEqual((), newlicence.getMissingParts())
        self.assertEqual([], newlicence.getFolderCategory())
        self.assertEqual(True, not newlicence.getMissingParts())

    def testSingleSelectionFieldWithOneDefaultValue(self):
        # configure a default value for the field 'folder category'
        vocabulary_term = self.portal_urban.buildlicence.foldercategories.objectValues()[0]
        vocabulary_term.setIsDefaultValue(True)
        self.update_voc_cache(self.portal_urban.buildlicence)
        # create a new buildlicence
        newlicence = self.createNewLicence()
        # the value of folderCategory should be the one marked as default value
        self.assertEqual([vocabulary_term.id], newlicence.getFolderCategory())

    def testMultiSelectionFieldWithOneDefaultValue(self):
        # configure a default value for the field 'missing parts'
        vocabulary_term = self.portal_urban.buildlicence.missingparts.objectValues()[0]
        vocabulary_term.setIsDefaultValue(True)
        self.update_voc_cache(self.portal_urban.buildlicence)
        # create a new buildlicence
        newlicence = self.createNewLicence()
        # the value of missing parts should be the one marked as default value
        self.assertEqual((vocabulary_term.id, ), newlicence.getMissingParts())

    def testSingleSelectionFieldWithMultipleDefaultValues(self):
        # configure a default value for the field 'folder category'
        vocabulary_term_1 = self.portal_urban.buildlicence.foldercategories.objectValues()[0]
        vocabulary_term_1.setIsDefaultValue(True)
        vocabulary_term_2 = self.portal_urban.buildlicence.foldercategories.objectValues()[1]
        vocabulary_term_2.setIsDefaultValue(True)
        self.update_voc_cache(self.portal_urban.buildlicence)
        # create a new buildlicence
        newlicence = self.createNewLicence()
        # the value of folderCategory should be the one marked as default value
        self.assertEqual([vocabulary_term_1.id, vocabulary_term_2.id], newlicence.getFolderCategory())

    def testMultiSelectionFieldWithMultiplesDefaultValues(self):
        # configure a default value for the field 'missing parts'
        vocabulary_term_1 = self.portal_urban.buildlicence.missingparts.objectValues()[0]
        vocabulary_term_1.setIsDefaultValue(True)
        vocabulary_term_2 = self.portal_urban.buildlicence.missingparts.objectValues()[2]
        vocabulary_term_2.setIsDefaultValue(True)
        self.update_voc_cache(self.portal_urban.buildlicence)
        # create a new buildlicence
        newlicence = self.createNewLicence()
        # the value of missing parts should be the one marked as default value
        self.assertEqual((vocabulary_term_1.id, vocabulary_term_2.id, ), newlicence.getMissingParts())

    def testDefaultValueMethodIsDefinedForEachConfigurableListing(self):
        # each field with a configurable listing (<=> has a UrbanVocabulary defined as its vocabulary) should
        # have the 'getDefaultValue' method defined on it, else the default value system wont work
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
        # create a new buildlicence
        newlicence = self.createNewLicence()
        # text fields should be empty by default
        self.assertEqual('<p></p>', newlicence.Description())

    def testTextValueConfigured(self):
        licence_config = self.site.portal_urban.buildlicence
        # set the default text value fotr the fdescription field
        default_text = '<p>Bla bla</p>'
        licence_config.textDefaultValues = ({'text': default_text, 'fieldname': 'description'}, )
        # any new licence should have this text as value for the description field
        newlicence = self.createNewLicence()
        self.assertEquals(default_text, newlicence.Description())

    def testDefaultTextMethodIsDefinedForEachTextField(self):
        # each text field  should have the 'getDefaultText' method defined on it, else the default value system wont
        # work
        site = self.site
        catalog = getToolByName(site, 'portal_catalog')
        test_licences = [brain.getObject() for brain in catalog(portal_type=URBAN_TYPES)]
        for licence in test_licences:
            for field in licence.schema.fields():
                if hasattr(field, 'defaut_content_type') and field.default_content_type.startswith('text'):
                    self.assertEquals(field.default_method, 'getDefaultText')


class TestEventDefaultValues(unittest.TestCase):
    """
    Tests for the text default values
    """

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.site = portal
        login(portal, self.layer.default_user)
        # create a licence
        buildlicences = portal.urban.buildlicences
        buildlicences.invokeFactory(
            'BuildLicence',
            id='newlicence',
            title='blabla',
        )
        buildlicence = buildlicences.newlicence
        buildlicence.setSolicitOpinionsTo('sncb')
        self.licence = buildlicence

    def update_voc_cache(self):
        with api.env.adopt_roles(['Manager']):
            voc_cache = self.portal_urban.restrictedTraverse('urban_vocabulary_cache')
            voc_cache.update_all_cache()

    def testNoDefaultValuesConfigured(self):
        # create a new buildlicence
        event = self.licence.createUrbanEvent('sncb')
        # any configurable selection field should be empty by default
        self.assertFalse(event.getAdviceAgreementLevel())
        self.assertFalse(event.getExternalDecision())

    def testSingleSelectionFieldWithOneDefaultValue(self):
        # configure a default value for the field 'externalDecision'
        vocabulary_term = self.portal_urban.externaldecisions.objectValues()[0]
        vocabulary_term.setIsDefaultValue(True)
        self.update_voc_cache()
        # create a new urban event
        event = self.licence.createUrbanEvent('sncb')
        # the value of folderCategory should be the one marked as default value
        self.assertEqual([vocabulary_term.id], event.getExternalDecision())

    def testSingleSelectionFieldWithMultipleDefaultValues(self):
        # configure a default value for the field 'externalDecision'
        vocabulary_term_1 = self.portal_urban.externaldecisions.objectValues()[0]
        vocabulary_term_1.setIsDefaultValue(True)
        vocabulary_term_2 = self.portal_urban.externaldecisions.objectValues()[2]
        vocabulary_term_2.setIsDefaultValue(True)
        self.update_voc_cache()
        # create a new urban event
        event = self.licence.createUrbanEvent('sncb')
        # the value of folderCategory should be the one marked as default value
        self.assertEqual([vocabulary_term_1.id, vocabulary_term_2.id], event.getExternalDecision())

    def testDefaultValueMethodIsDefinedForEachConfigurableListing(self):
        # each field with a configurable listing (<=> has a UrbanVocabulary defined as its vocabulary) should
        # have the 'getDefaultValue' method defined on it, else the default value system wont work
        event = self.licence.createUrbanEvent('sncb')
        site = self.site
        catalog = getToolByName(site, 'portal_catalog')
        test_events = [brain.getObject() for brain in catalog(object_provides=IUrbanEvent.__identifier__)]
        for event in test_events:
            for field in event.schema.fields():
                if isinstance(field.vocabulary, UrbanVocabulary) and field.type != 'datagrid':
                    self.assertEquals(field.default_method, 'getDefaultValue')

    def testNoTextDefaultValuesConfigured(self):
        # create a new event 'rappor du college'
        # text field 'decisionText' should be empty by default
        event = self.licence.createUrbanEvent('rapport-du-college')
        decision_text = event.getDecisionText()
        self.assertEqual(decision_text, '<p></p>')

    def testTextValueConfigured(self):
        eventtypes = self.portal_urban.buildlicence.eventconfigs
        event_type = getattr(eventtypes, 'rapport-du-college')
        # set a a default text for the field 'decsionText'
        default_text = '<p>Kill bill!</p>'
        event_type.textDefaultValues = [{'text': default_text, 'fieldname': 'decisionText'}]
        # the created event should have this text in its field 'decisionText'
        event = self.licence.createUrbanEvent(event_type)
        notify(ObjectCreatedEvent(event))
        decision_text = event.getDecisionText()
        self.assertEqual(decision_text, default_text)

    def testTextValueConfiguredWithPythonExpression(self):
        eventtypes = self.portal_urban.buildlicence.eventconfigs
        event_type = getattr(eventtypes, 'rapport-du-college')
        # set a a default text for the field 'decsionText'
        default_text = '<p>Kill <b tal:replace="self/Title"></b> and <b tal:replace="event/getId"></b> </p>'
        event_type.textDefaultValues = [{'text': default_text, 'fieldname': 'decisionText'}]
        # the created event should have this text in its field 'decisionText'
        event = self.licence.createUrbanEvent(event_type)
        notify(ObjectCreatedEvent(event))
        decision_text = event.getDecisionText()

        expected_text = '<p>Kill %s and %s </p>' % (self.licence.Title(), event.getId())
        self.assertEqual(decision_text, expected_text)

    def testDefaultTextMethodIsDefinedForEachTextField(self):
        # each text field  should have the 'getDefaultText' method defined on it, else the default value system wont
        # work
        for field in UrbanEventInquiry.UrbanEventInquiry_schema.fields():
            if hasattr(field, 'defaut_content_type') and field.default_content_type.startswith('text'):
                self.assertEquals(field.default_method, 'getDefaultText')


class TestParcelApplicantDefaultValue(unittest.TestCase):
    """
    Tests for the text default values
    """

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.site = portal
        login(portal, self.layer.default_user)
        # create a licence
        buildlicences = portal.urban.buildlicences
        buildlicences.invokeFactory(
            'BuildLicence',
            id='newlicence',
            title='blabla',
        )
        buildlicence = buildlicences.newlicence
        self.licence = buildlicence

    def test_parcel_applicant_default_personTitle(self):
        searchparcelview = self.licence.restrictedTraverse('searchparcels')
        parcel_data = {
            'puissance': '',
            'division': '62006',
            'worklocations': (),
            'partie': '',
            'radical': '552',
            'section': 'A',
            'outdated': 'False',
            'bis': '',
            'exposant': 'V'
        }
        owners = {
            u'64122514647': {
                'city': u'AWANS',
                'name': u'Macours',
                'firstname': u'Jo\xeblle',
                'country': u'BE',
                'zipcode': u'4340',
                'number': u'61',
                'street': u'Rue de Bruxelles'
            }
        }
        searchparcelview.createParcelAndProprietary(parcel_data, owners)
        applicants = self.licence.getApplicants()
        applicant = applicants[0]
        self.assertEquals('madam_or_mister', applicant.getPersonTitle())
        display_view = applicant.restrictedTraverse('document_generation_helper_view')
        self.assertEquals(u'Madame/Monsieur', display_view.personTitle)
