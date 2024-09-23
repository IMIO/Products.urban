#  -*- coding: utf-8 -*-
import unittest2 as unittest

from imio.urban.core.contents.eventconfig import IEventConfig

from Products.CMFCore.utils import getToolByName
from Products.urban.interfaces import (
    IAcknowledgmentEvent,
    IOpinionRequestEvent,
    IInquiryEvent,
)
from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.testing import URBAN_TESTS_LICENCES

from plone import api
from plone.app.testing import quickInstallProduct, login
from plone.app.testing import setRoles
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.app.testing.interfaces import TEST_USER_ID

from zope.component.interface import interfaceToName


class TestInstall(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer["portal"]
        self.portal = portal
        login(portal, "urbaneditor")
        self.licence = portal.urban.buildlicences.objectValues()[-1]

    def testEventTypesCreated(self):
        catalog = getToolByName(self.portal, "portal_catalog")
        interfaceName = interfaceToName(self.portal, IEventConfig)
        eventTypes = catalog(object_provides=interfaceName)
        self.failUnless(len(eventTypes) > 0)

    def testEventWithoutEventTypeType(self):
        # 'avis-etude-incidence' can only be added if it is defined on the licence
        self.licence.setImpactStudy(True)
        self.licence.createUrbanEvent("avis-etude-incidence")

    def testAcknowledgmentSearchByInterface(self):
        licence = self.licence
        # there is already 10 events created on the licence
        self.assertEqual(len(licence.objectValues("UrbanEvent")), 10)
        urbanEvent = licence.createUrbanEvent("accuse-de-reception")
        self.assertEqual(len(licence.objectValues("UrbanEvent")), 11)
        self.failUnless(IAcknowledgmentEvent.providedBy(urbanEvent))
        events = licence.getAllEvents(IAcknowledgmentEvent)
        # == 2 because there was an existing event 'accusé de réception' on the
        # licence
        self.assertEqual(len(events), 2)

    def testInquirySearchByInterface(self):
        licence = self.licence
        self.assertEqual(len(licence.objectValues("UrbanEvent")), 10)
        # no need to create an inquiry event, its already existing in the test
        # licence
        urban_event = licence.getLastEvent(IInquiryEvent)
        self.failUnless(IInquiryEvent.providedBy(urban_event))

    def testOpinionRequestMarkerInterface(self):
        licence = self.licence
        self.assertEqual(len(licence.objectValues("UrbanEvent")), 10)
        # no need to create an opinion request event, its already existing in
        # the test licence
        urbanEvent = licence.getLastEvent(IOpinionRequestEvent)
        if not urbanEvent:
            licence.solicitOpinionsTo = ("belgacom",)
            licence.createAllAdvices()
            urbanEvent = licence.getLastEvent(IOpinionRequestEvent)
        self.failUnless(IOpinionRequestEvent.providedBy(urbanEvent))


class TestContact(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal_urban = self.portal.portal_urban
        self.buildlicence = self.portal_urban.buildlicence
        self.foldermanagers = self.buildlicence.foldermanagers
        self.folderBuildLicences = self.portal.urban.buildlicences
        # set language to 'fr' as we do some translations above
        ltool = self.portal.portal_languages
        defaultLanguage = "fr"
        supportedLanguages = ["en", "fr"]
        ltool.manage_setLanguageSettings(
            defaultLanguage, supportedLanguages, setUseCombinedLanguageCodes=False
        )
        # this needs to be done in tests for the language to be taken into account...
        ltool.setLanguageBindings()

    def test_getSignaleticIsUnicode(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory("FolderManager", "agent")
        agent = self.foldermanagers.agent
        agent.setName1(u"Robin")
        agent.setPersonTitle(u"master")
        self.failUnless(isinstance(agent.getSignaletic(), unicode))
        self.failUnless(isinstance(agent.getSignaletic(withaddress=True), unicode))
        self.failUnless(isinstance(agent.getSignaletic(linebyline=True), unicode))
        self.failUnless(
            isinstance(agent.getSignaletic(withaddress=True, linebyline=True), unicode)
        )

    def test_name1GetSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory("FolderManager", "agent")
        agent = self.foldermanagers.agent
        agent.setName1(u"Robiné")
        agent.setName2(u"Hood")
        agent.setPersonTitle(u"master")
        agent.setNumber(u"1")
        agent.setCity(u"Sherwood")
        agent.REQUEST.set("HTTP_ACCEPT_LANGUAGE", "fr")
        self.assertEquals(agent.getSignaletic(), u"Maître Robiné Hood")
        self.assertEquals(
            agent.getSignaletic(linebyline=True), u"<p>Maître Robiné Hood</p>"
        )
        self.assertEquals(
            agent.getSignaletic(withaddress=True),
            u"Maître Robiné Hood, domicilié 1 Sherwood",
        )
        self.assertEquals(
            agent.getSignaletic(withaddress=True, linebyline=True),
            u"<p>Maître Robiné Hood<br />, 1<br /> Sherwood</p>",
        )

    def test_name2GetSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory("FolderManager", "agent")
        agent = self.foldermanagers.agent
        agent.setName1(u"Robin")
        agent.setName2(u"Hoodé")
        agent.setPersonTitle(u"master")
        agent.setNumber(u"1")
        agent.setCity(u"Sherwood")
        agent.REQUEST.set("HTTP_ACCEPT_LANGUAGE", "fr")
        self.assertEquals(agent.getSignaletic(), u"Maître Robin Hoodé")
        self.assertEquals(
            agent.getSignaletic(linebyline=True), u"<p>Maître Robin Hoodé</p>"
        )
        self.assertEquals(
            agent.getSignaletic(withaddress=True),
            u"Maître Robin Hoodé, domicilié 1 Sherwood",
        )
        self.assertEquals(
            agent.getSignaletic(withaddress=True, linebyline=True),
            u"<p>Maître Robin Hoodé<br />, 1<br /> Sherwood</p>",
        )

    def test_personTitleGetSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory("FolderManager", "agent")
        agent = self.foldermanagers.agent
        agent.setName1(u"Robin")
        agent.setName2(u"Hood")
        agent.setPersonTitle(u"master")
        agent.setNumber(u"1")
        agent.setCity(u"Sherwood")
        agent.REQUEST.set("HTTP_ACCEPT_LANGUAGE", "fr")
        self.assertEquals(agent.getSignaletic(), u"Maître Robin Hood")
        self.assertEquals(
            agent.getSignaletic(linebyline=True), u"<p>Maître Robin Hood</p>"
        )
        self.assertEquals(
            agent.getSignaletic(withaddress=True),
            u"Maître Robin Hood, domicilié 1 Sherwood",
        )
        self.assertEquals(
            agent.getSignaletic(withaddress=True, linebyline=True),
            u"<p>Maître Robin Hood<br />, 1<br /> Sherwood</p>",
        )

    def test_cityGetSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.foldermanagers.invokeFactory("FolderManager", "agent")
        agent = self.foldermanagers.agent
        agent.setName1(u"Robin")
        agent.setName2(u"Hood")
        agent.setPersonTitle(u"master")
        agent.setNumber(u"1")
        agent.setCity(u"Sherwoodé")
        agent.REQUEST.set("HTTP_ACCEPT_LANGUAGE", "fr")
        self.assertEquals(agent.getSignaletic(), u"Maître Robin Hood")
        self.assertEquals(
            agent.getSignaletic(linebyline=True), u"<p>Maître Robin Hood</p>"
        )
        self.assertEquals(
            agent.getSignaletic(withaddress=True),
            u"Maître Robin Hood, domicilié 1 Sherwoodé",
        )
        self.assertEquals(
            agent.getSignaletic(withaddress=True, linebyline=True),
            u"<p>Maître Robin Hood<br />, 1<br /> Sherwoodé</p>",
        )

    def test_getApplicantsSignaletic(self):
        login(self.portal, TEST_USER_NAME)
        self.folderBuildLicences.invokeFactory("BuildLicence", "buildLicence")
        buildLicence = self.folderBuildLicences.buildLicence
        buildLicence.invokeFactory("Applicant", "applicant")
        applicant = buildLicence.applicant
        applicant.setName1(u"Robiné")
        applicant.setName2(u"Hoodé")
        applicant.setPersonTitle(u"master")
        applicant.setNumber(u"1")
        applicant.setCity(u"Sherwoodé")
        buildLicence.REQUEST.set("HTTP_ACCEPT_LANGUAGE", "fr")
        self.assertEquals(
            buildLicence.getApplicantsSignaletic(), u"Maître Robiné Hoodé"
        )
        self.assertEquals(
            buildLicence.getApplicantsSignaletic(withaddress=True),
            u"Maître Robiné Hoodé, domicilié 1 Sherwoodé",
        )
        api.content.delete(buildLicence)
