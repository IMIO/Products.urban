# -*- coding: utf-8 -*-

from Products.urban import utils
from Products.urban.interfaces import ICODT_BaseBuildLicence
from Products.urban.testing import URBAN_TESTS_INTEGRATION
from Products.urban.testing import URBAN_TESTS_LICENCES_FUNCTIONAL
from Products.urban.tests.helpers import SchemaFieldsTestCase
from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser
from time import sleep
from zope.globalrequest import getRequest
from zope.globalrequest import setRequest

import transaction
import unittest


class TestBuildLicence(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.buildlicence = portal.urban.buildlicences.objectValues('BuildLicence')[0]
        self.portal_urban = portal.portal_urban
        login(portal, 'urbaneditor')
        if not getRequest():
            setRequest(self.portal.REQUEST)

    def testLicenceTitleUpdate(self):
        # verify that the licence title update correctly when we add or remove applicants/proprietaries
        # on the licence
        licence = self.buildlicence
        self.assertTrue(licence.Title().endswith('/1 - Exemple Permis Urbanisme - Mes Smith & Wesson'))
        # remove the applicant
        applicant_id = licence.objectValues('Applicant')[0].id
        licence.manage_delObjects([applicant_id])
        self.assertTrue(licence.Title().endswith('/1 - Exemple Permis Urbanisme - no_applicant_defined'))
        # add an applicant back
        licence.invokeFactory('Applicant', 'new_applicant', name1='Quentin', name2='Tinchimiloupète')
        self.assertTrue(licence.Title().endswith('/1 - Exemple Permis Urbanisme -  Quentin Tinchimiloupète'))

    def test_LicenceUpdateTitleForCodt_buildlicence(self):
        # check that the licence updateTitle method add all applicants or proprietaries or notaries to the Licence Title
        licence = self.buildlicence
        self.assertTrue(licence.Title().endswith('/1 - Exemple Permis Urbanisme - Mes Smith & Wesson'))
        # add another applicant
        licence.invokeFactory('Applicant', 'new_applicant', name1='Chuck', name2='Norris')
        # call updateTitle()
        licence.updateTitle()
        # add applicant with invokeFactory add a space before the name of the applicant => 2spaces
        self.assertTrue(licence.Title().endswith('/1 - Exemple Permis Urbanisme - Mes Smith & Wesson,  Chuck Norris'))

    def test_LicenceUpdateTitleForInspection(self):
        # check that the licence updateTitle method add all proprietaries on inspections titles
        inspection_expl = self.portal.urban.inspections.objectValues('Inspection')[0]
        # for the inspection the proprietary is before inspection name
        self.assertTrue(inspection_expl.Title().endswith('/1 - Mes Smith & Wesson - Exemple Inspection'))
        # add proprietary
        inspection_expl.invokeFactory('Proprietary', 'new_proprietary', name1='Chuck', name2='Norris')
        # call updateTitle()
        inspection_expl.updateTitle()
        self.assertTrue(inspection_expl.Title().endswith(
            '/1 - Mes Smith & Wesson,  Chuck Norris - Exemple Inspection'))

    def test_LicenceUpdateTitleForNotaryLetter(self):
        # check that the licence updateTitle method add all proprietaries and notaries on notary letters titles
        licence = self.portal.urban.notaryletters.objectValues()[1]
        self.assertTrue(licence.Title().endswith('/1 - Mes Smith & Wesson -  NotaryName1 NotarySurname1'))
        notaries = self.portal.urban.notaries.objectValues()
        notaries = list(notaries)
        # add all notaries to the licence and add a proprietary
        licence.setNotaryContact(notaries)
        licence.invokeFactory('Proprietary', id='proprietary2', name1='Aeron', name2='Lorelei')
        licence.updateTitle()

        titleparts = licence.Title().split(" - ")
        notarieslist = titleparts[2].split(", ")
        notariesset = set(notarieslist)
        testnotariesset = set([' André Sanfrapper', ' NotaryName1 NotarySurname1'])
        self.assertEqual(notariesset, testnotariesset)
        testproprietaries = 'Mes Smith & Wesson,  Aeron Lorelei'
        self.assertEqual(titleparts[1], testproprietaries)

    def testGetLastEventWithoutEvent(self):
        buildlicences = self.portal.urban.buildlicences
        LICENCE_ID = 'buildlicence1'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildlicence = getattr(buildlicences, LICENCE_ID)
        self.assertFalse(buildlicence.getLastEvent())

    def testGetLastEventWithOneEvent(self):
        buildlicence = self.buildlicence
        createdEvent = buildlicence.createUrbanEvent('depot-de-la-demande')
        event = buildlicence.getLastEvent()
        self.assertEqual(createdEvent, event)
        self.failUnless(event is not None)

    def testGetLastEventWithMoreThanOneEvent(self):
        buildlicence = self.buildlicence
        buildlicence.createUrbanEvent('depot-de-la-demande', description='A')
        ev2 = buildlicence.createUrbanEvent('depot-de-la-demande', description='B')
        sleep(1)
        event = buildlicence.getLastEvent()
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
        # 1 link login on treatment agent
        at = getattr(self.portal_urban.buildlicence.foldermanagers, 'foldermanager1')
        at.setPloneUserId('urbaneditor')
        # 2 create an empty buildlicence
        LICENCE_ID = 'licence2'
        buildlicences.invokeFactory('BuildLicence', LICENCE_ID)
        buildLicence2 = getattr(buildlicences, LICENCE_ID)
        buildLicence2.setFoldermanagers(utils.getCurrentFolderManager())
        # 3 check if agent treatment exist
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
        created_advices = [ob for ob in buildlicence.objectValues() if ob.portal_type == 'UrbanEventOpinionRequest']
        self.assertEqual(len(buildlicence.getAllAdvices()), 2 - len(created_advices))

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
        # set opinion request to 'belgacom' and 'sncb'
        opinions = ('sncb', 'belgacom')
        buildlicence.setSolicitOpinionsTo(opinions)
        buildlicence.createAllAdvices()
        self.assertEqual(len(buildlicence.getAllOpinionRequests()), 2)


class TestBuildLicenceFields(SchemaFieldsTestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban

        default_user = self.layer.default_user
        default_password = self.layer.default_password
        login(self.portal, default_user)
        self.licences = []
        # create 'BuildLicence' and 'ParcelOutLicence'
        for content_type in ['BuildLicence', 'ParcelOutLicence']:
            licence_folder = utils.getLicenceFolder(content_type)
            testlicence_id = 'test_{}'.format(content_type.lower())
            licence_folder.invokeFactory(content_type, id=testlicence_id)
            transaction.commit()
            test_licence = getattr(licence_folder, testlicence_id)
            self.licences.append(test_licence)
        self.licence = self.licences[0]
        # create a CODT_BuildLicence
        licence_folder_codtbuildlicences = utils.getLicenceFolder('CODT_BuildLicence')
        codtbuildlicence_testlicence_id = 'test_{}'.format('CODT_BuildLicence'.lower())
        licence_folder_codtbuildlicences.invokeFactory('CODT_BuildLicence', id=codtbuildlicence_testlicence_id)
        transaction.commit()
        self.licences.append(getattr(licence_folder_codtbuildlicences, codtbuildlicence_testlicence_id))

        # create a CODT_ParcelOutLicence
        licence_folder_codtparceloutlicences = utils.getLicenceFolder('CODT_ParcelOutLicence')
        codtparceloutlicence_testlicence_id = 'test_{}'.format('CODT_ParcelOutLicence'.lower())
        licence_folder_codtparceloutlicences.invokeFactory('CODT_ParcelOutLicence', id=codtparceloutlicence_testlicence_id)
        transaction.commit()
        self.licences.append(getattr(licence_folder_codtparceloutlicences, codtparceloutlicence_testlicence_id))

        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)
        if not getRequest():
            setRequest(self.portal.REQUEST)

    def tearDown(self):
        with api.env.adopt_roles(['Manager']):
            if not getRequest():
                setRequest(self.portal.REQUEST)
            for licence in self.licences:
                api.content.delete(licence)
        transaction.commit()

    def test_has_attribute_workType(self):
        field_name = 'workType'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_workType_is_visible(self):
        for licence in self.licences:
            msg = "field 'workType' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Nature des travaux (liste 220)</span>:", licence, msg)

    def test_has_attribute_usage(self):
        field_name = 'usage'
        msg = "field '{}' not on class BuildLicence".format(field_name)
        self.assertTrue(hasattr(self.licences[0], field_name), msg)

    def test_usage_is_visible(self):
        msg = "field 'usage' not visible on BuildLicence"
        self._is_field_visible("<span>Statistiques INS</span>:", msg=msg)

    def test_has_attribute_annoncedDelay(self):
        field_name = 'annoncedDelay'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_annoncedDelay_is_visible(self):
        for licence in self.licences:
            msg = "field 'annoncedDelay' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Délai annoncé</span>:", licence, msg)

    def test_has_attribute_annoncedDelayDetails(self):
        field_name = 'annoncedDelayDetails'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_annoncedDelayDetails_is_visible(self):
        for licence in self.licences:
            msg = "field 'annoncedDelayDetails' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Détails concernant le délai annoncé</span>:", licence, msg)

    def test_has_attribute_townshipCouncilFolder(self):
        field_name = 'townshipCouncilFolder'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_townshipCouncilFolder_is_visible(self):
        for licence in self.licences:
            msg = "field 'townshipCouncilFolder' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Dossier \"Conseil Communal\"</span>:", licence, msg)

    def test_has_attribute_impactStudy(self):
        field_name = 'impactStudy'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_impactStudy_is_visible(self):
        for licence in self.licences:
            msg = "field 'impactStudy' not visible on {}".format(licence.getPortalTypeName())
            self._is_field_visible("<span>Étude d'incidences ?</span>:", licence, msg)

    def test_has_attribute_implantation(self):
        field_name = 'implantation'
        for licence in self.licences:
            msg = "field '{}' not on class {}".format(field_name, licence.getPortalTypeName())
            self.assertTrue(hasattr(licence, field_name), msg)

    def test_implantation_is_visible(self):
        for licence in self.licences:
            msg = "field 'implantation' not visible on {}".format(licence.getPortalTypeName())
            if ICODT_BaseBuildLicence.providedBy(licence):
                self._is_field_visible("<span>Implantation (art D.IV.72)</span>:", licence, msg)
            else:
                self._is_field_visible("<span>Implantation (art. 137)</span>:", licence, msg)

    def test_has_attribute_pebType(self):
        field_name = 'pebType'
        msg = "field '{}' not on class BuildLicence".format(field_name)
        self.assertTrue(hasattr(self.licences[0], field_name), msg)

    def test_pebType_is_visible(self):
        msg = "field 'pebType' not visible on BuildLicence"
        self._is_field_visible("<span>Type de PEB</span>:", msg=msg)

    def test_has_attribute_pebDetails(self):
        field_name = 'pebDetails'
        msg = "field '{}' not on class BuildLicence".format(field_name)
        self.assertTrue(hasattr(self.licences[0], field_name), msg)

    def test_pebDetails_is_visible(self):
        msg = "field 'pebDetails' not visible on BuildLicence"
        self._is_field_visible("<span>Détails concernant le PEB</span>:", msg=msg)

    def test_has_attribute_representativeContacts(self):
        field_name = 'representativeContacts'
        msg = "field '{}' not on class ParcelOutLicence".format(field_name)
        self.assertTrue(self.licences[1].getField('representativeContacts'), msg)
        msg = "field '{}' not on class CODT ParcelOutLicence".format(field_name)
        self.assertTrue(self.licences[3].getField('representativeContacts'), msg)

    def test_representativeContacts_is_visible(self):
        msg = "field 'representativeContacts' not visible on CODT ParcelOutLicence"
        self._is_field_visible("<legend>Architecte(s) ou géomètre(s)</legend>", obj= self.licences[3], msg=msg)
        msg = "field 'representativeContacts' not visible on CODT BuildLicence"
        self._is_field_visible("<legend>Architecte(s) ou géomètre(s)</legend>", obj= self.licences[2], msg=msg)
