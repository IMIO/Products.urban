# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.urban import utils
from Products.urban.testing import URBAN_TESTS_INTEGRATION
from Products.urban.testing import URBAN_TESTS_LICENCES

from plone.app.testing import login
from plone.testing.z2 import Browser
from time import sleep

import transaction
import unittest


class TestBuildLicence(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.buildlicence = portal.urban.buildlicences.objectValues()[-1]
        self.portal_urban = portal.portal_urban
        login(portal, 'urbaneditor')

    def testLicenceTitleUpdate(self):
        # verify that the licence title update correctly when we add or remove applicants/proprietaries
        #on the licence
        licence = self.buildlicence
        self.assertTrue(licence.Title() == 'PU/2014/1/ - Exemple Permis Urbanisme -  Smith & Wesson')
        #remove the applicant
        applicant_id = licence.objectValues('Contact')[0].id
        licence.manage_delObjects([applicant_id])
        self.assertTrue(licence.Title() == 'PU/2014/1/ - Exemple Permis Urbanisme - no_applicant_defined')
        #add an applicant back
        licence. invokeFactory('Applicant', 'new_applicant', name1='Quentin', name2='Tinchimiloupète')
        self.assertTrue(licence.Title() == 'PU/2014/1/ - Exemple Permis Urbanisme -  Quentin Tinchimiloupète')

    def testGetLastEventWithoutEvent(self):
        buildlicences = self.portal.urban.buildlicences
        LICENCE_ID = 'buildlicence1'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildlicence = getattr(buildlicences, LICENCE_ID)
        self.assertEqual(buildlicence._getLastEvent(), None)

    def testGetLastEventWithOneEvent(self):
        buildlicence = self.buildlicence
        createdEvent = buildlicence.createUrbanEvent('depot-de-la-demande')
        event = buildlicence._getLastEvent()
        self.assertEqual(createdEvent, event)
        self.failUnless(event is not None)

    def testGetLastEventWithMoreThanOneEvent(self):
        buildlicence = self.buildlicence
        buildlicence.createUrbanEvent('depot-de-la-demande', description='A')
        ev2 = buildlicence.createUrbanEvent('depot-de-la-demande', description='B')
        sleep(1)
        event = buildlicence._getLastEvent()
        self.failUnless(event is not None)
        self.assertEqual(event.Description(), 'B')
        self.assertEqual(event, ev2)

    def testGetAllOpinionRequests(self):
        buildlicence = self.buildlicence
        opinions = buildlicence.objectValues('UrbanEventOpinionRequest')
        self.assertEqual(buildlicence.getAllOpinionRequests(), opinions)

    def testGetLastDeposit(self):
        buildlicence = self.buildlicence
        buildlicence.createUrbanEvent('dossier-incomplet', description='A')
        sleep(1)
        buildlicence.createUrbanEvent('depot-de-la-demande', description='B')
        sleep(1)
        ev3 = buildlicence.createUrbanEvent('depot-de-la-demande', description='C')
        sleep(1)
        event = buildlicence.getLastDeposit()
        self.assertEqual(event.Description(), 'C')
        self.assertEqual(event, ev3)

    def testGetAcknowledgement(self):
        buildlicence = self.buildlicence
        buildlicence.createUrbanEvent('dossier-incomplet', description='A')
        ev2 = buildlicence.createUrbanEvent('accuse-de-reception', description='B')
        buildlicence.createUrbanEvent('depot-de-la-demande', description='C')
        event = buildlicence.getLastAcknowledgment()
        self.assertEqual(event.Description(), 'B')
        self.assertEqual(event, ev2)

    def testGetCurrentFolderManager(self):
        buildlicences = self.portal.urban.buildlicences
        #1 link login on treatment agent
        at = getattr(self.portal_urban.buildlicence.foldermanagers, 'foldermanager1')
        at.setPloneUserId('urbaneditor')
        #2 create an empty buildlicence
        LICENCE_ID = 'licence2'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildLicence2 = getattr(buildlicences, LICENCE_ID)
        buildLicence2.setFoldermanagers(utils.getCurrentFolderManager())
        #3 check if agent treatment exist
        self.assertEqual(buildLicence2.getFoldermanagers()[0].getPloneUserId(), 'urbaneditor')
        at.setPloneUserId('urbanreader')
        LICENCE_ID = 'licence3'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildLicence3 = getattr(buildlicences, LICENCE_ID)
        buildLicence3.setFoldermanagers(utils.getCurrentFolderManager())
        self.assertEqual(len(buildLicence3.getFoldermanagers()), 0)

    def testGetAllAdvicesWithoutOpinionRequest(self):
        buildlicence = self.buildlicence
        self.assertEqual(buildlicence.getAllAdvices(), [])

    def testGetAllAdvicesWithOpinionRequest(self):
        buildlicence = self.buildlicence
        opinions = ('sncb', 'belgacom')
        buildlicence.setSolicitOpinionsTo(opinions)
        # == 1 because the opinion request event of belgacom already exists
        self.assertEqual(len(buildlicence.getAllAdvices()), 1)

    def testCreateAllAdvicesWithoutOpinionRequest(self):
        buildlicences = self.portal.urban.buildlicences
        LICENCE_ID = 'buildlicence1'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildlicence = getattr(buildlicences, LICENCE_ID)
        buildlicence.createAllAdvices()
        self.assertEqual(buildlicence.getAllOpinionRequests(), [])

    def testCreateAllAdvicesWithOpinionRequest(self):
        buildlicences = self.portal.urban.buildlicences
        LICENCE_ID = 'buildlicence1'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildlicence = getattr(buildlicences, LICENCE_ID)
        #set opinion request to 'belgacom' and 'sncb'
        startDate = DateTime('01/01/2011')
        opinions = ('sncb', 'belgacom')
        buildlicence.setSolicitOpinionsTo(opinions)
        buildlicence.setInvestigationStart(startDate)
        buildlicence.createAllAdvices()
        self.assertEqual(len(buildlicence.getAllOpinionRequests()), 2)


class TestBuildLicenceFields(unittest.TestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        # create a test EnvClassOne licence
        login(self.portal, 'urbaneditor')
        self.licences = []
        for content_type in ['BuildLicence', 'ParcelOutLicence']:
            licence_folder = utils.getLicenceFolder(content_type)
            testlicence_id = 'test_{}'.format(content_type)
            if testlicence_id not in licence_folder.objectIds():
                licence_folder.invokeFactory(content_type, id=testlicence_id)
                transaction.commit()
            test_licence = getattr(licence_folder, testlicence_id)
            self.licences.append(test_licence)
        self.test_buildlicence = self.licences[0]

        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def tearDown(self):
        self.urban.buildlicences.manage_delObjects(self.licences[0].id)
        self.urban.parceloutlicences.manage_delObjects(self.licences[1].id)
        transaction.commit()

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_has_attribute_workType(self):
        field_name = 'workType'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_workType_is_visible(self):
        for licence in self.licences:
            msg = "field 'workType' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Nature des travaux</span>:" in contents, msg)

    def test_has_attribute_usage(self):
        field_name = 'usage'
        msg = "field '{}' not on class BuildLicence".format(field_name)
        self.assertTrue(hasattr(self.test_buildlicence, field_name), msg)

    def test_usage_is_visible(self):
        msg = "field 'usage' not visible on BuildLicence"
        self.browser.open(self.test_buildlicence.absolute_url())
        contents = self.browser.contents
        self.assertTrue("<span>Statistiques INS</span>:" in contents, msg)

    def test_has_attribute_annoncedDelay(self):
        field_name = 'annoncedDelay'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_annoncedDelay_is_visible(self):
        for licence in self.licences:
            msg = "field 'annoncedDelay' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Délai annoncé</span>:" in contents, msg)

    def test_has_attribute_annoncedDelayDetails(self):
        field_name = 'annoncedDelayDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_annoncedDelayDetails_is_visible(self):
        for licence in self.licences:
            msg = "field 'annoncedDelayDetails' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Détails concernant le délai annoncé</span>:" in contents, msg)

    def test_has_attribute_townshipCouncilFolder(self):
        field_name = 'townshipCouncilFolder'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_townshipCouncilFolder_is_visible(self):
        for licence in self.licences:
            msg = "field 'townshipCouncilFolder' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Dossier \"Conseil Communal\"</span>:" in contents, msg)

    def test_has_attribute_impactStudy(self):
        field_name = 'impactStudy'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_impactStudy_is_visible(self):
        for licence in self.licences:
            msg = "field 'impactStudy' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Etude d'incidence?</span>:" in contents, msg)

    def test_has_attribute_implantation(self):
        field_name = 'implantation'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_implantation_is_visible(self):
        for licence in self.licences:
            msg = "field 'implantation' not visible on {}".format(licence.getPortalTypeName())
            self.browser.open(licence.absolute_url())
            contents = self.browser.contents
            self.assertTrue("<span>Implantation (art. 137)</span>:" in contents, msg)

    def test_has_attribute_pebType(self):
        field_name = 'pebType'
        msg = "field '{}' not on class BuildLicence".format(field_name)
        self.assertTrue(hasattr(self.test_buildlicence, field_name), msg)

    def test_pebType_is_visible(self):
        msg = "field 'pebType' not visible on BuildLicence"
        self.browser.open(self.test_buildlicence.absolute_url())
        contents = self.browser.contents
        self.assertTrue("<span>Type de PEB</span>:" in contents, msg)

    def test_has_attribute_pebDetails(self):
        field_name = 'pebDetails'
        msg = "field '{}' not on class BuildLicence".format(field_name)
        self.assertTrue(hasattr(self.test_buildlicence, field_name), msg)

    def test_pebDetails_is_visible(self):
        msg = "field 'pebDetails' not visible on BuildLicence"
        self.browser.open(self.test_buildlicence.absolute_url())
        contents = self.browser.contents
        self.assertTrue("<span>Détails concernant le PEB</span>:" in contents, msg)
