# -*- coding: utf-8 -*-
from plone.app.testing import login
from Products.urban.interfaces import IGenericLicence
from Products.urban.testing import URBAN_TESTS_LICENCES
from Products.urban.tests.helpers import BrowserTestCase
from Products.urban.setuphandlers import createFolderDefaultValues
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from testfixtures import compare, StringComparison as S
from collective.eeafaceted.dashboard.utils import getDashboardQueryResult
from DateTime import DateTime
from zope.globalrequest.local import setLocal
from plone import api
from plone.app.testing import login
from mock import patch


class TestExportViews(BrowserTestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        self.portal = self.layer["portal"]
        self.urban = self.portal.urban
        self.catalog = getToolByName(self.portal, "portal_catalog")
        self.statsview = self.urban.restrictedTraverse("urbanstatsview")
        login(self.portal, "urbaneditor")
        self.browser = Browser(self.portal)
        self.browserLogin("urbaneditor")
        self.browser.open("%s%s" % (self.urban.absolute_url(), "/urbanstatsview"))

    def testStatsViewDisplay(self):
        # check that the stats view is simply available
        self.browser.open(self.urban.absolute_url() + "/urbanstatsview")
        compare(S("(?s).*Statistiques des dossiers.*"), self.browser.contents)

    def testStatsViewEmptyResult(self):
        # check the display result when no licences fall under stats criteria
        self.browser.open(self.urban.absolute_url() + "/urbanstatsview")
        self.browser.getControl("Statistics").click()
        new_url = "%s/urbanstatsview%s" % (
            self.urban.absolute_url(),
            self.browser.url.split("/urban")[1],
        )
        self.browser.open(new_url)
        compare(S("(?s).*0 dossiers.*"), self.browser.contents)

    def testStatsViewsResult(self):
        licences_number = 8
        # check the normal case display result
        self.browser.open(self.urban.absolute_url() + "/urbanstatsview")
        self.browser.getControl(name="licence_states").getControl(
            value="in_progress"
        ).click()
        self.browser.getControl("Statistics").click()
        new_url = "%s/urbanstatsview%s" % (
            self.urban.absolute_url(),
            self.browser.url.split("/urban")[1],
        )
        self.browser.open(new_url)
        compare(S("(?s).*{} dossiers.*".format(licences_number)), self.browser.contents)

    @patch("Products.urban.viewlets.urbain_220.UrbainXMLExport.get_date_range")
    def testUrbainXMLExport(self, get_date_range):
        """
        Test to verify that special characters like ï, ë, à, é, etc.,
        appear correctly when generating list 220.

        """

        get_date_range.return_value = (DateTime("2000/01/01"), DateTime("2050/01/01"))

        # We have to use setLocal to make request.environ available to fingerpointing
        # https://github.com/collective/collective.fingerpointing/issues/100
        # TODO: Move this to a layer

        setLocal("request", self.portal.REQUEST)

        # Log in as an urban manager to access the dashboard
        login(self.portal, "urbanmanager")
        dashboard = self.urban.unrestrictedTraverse("codt_buildlicences")
        urbain_xml_view = dashboard.unrestrictedTraverse("generate_urbain_220xml")

        brains = getDashboardQueryResult(dashboard)
        licence = brains[0].getObject()

        # Set the licence workflow state to "accepted"
        licence.workflow_history.get("codt_buildlicence_workflow")[0][
            "review_state"
        ] = "accepted"

        workTypeInfo = {"id": "DEM", "title": "Démolition", "extraValue": "DEM"}
        portal_urban = getToolByName(self.portal, "portal_urban")
        licenceconfig = portal_urban.codt_buildlicence

        worktypes_folder = licenceconfig.folderbuildworktypes
        worktypes_folder.invokeFactory("UrbanVocabularyTerm", **workTypeInfo)
        licence.setWorkType(workTypeInfo.get("id"))

        start = DateTime("2000/01/01")
        end = DateTime("2050/01/01")

        res = urbain_xml_view.generateUrbainXML(brains, start, end)
        self.assertIn('encoding="utf-8"', res)
        self.assertIsInstance(res, unicode)

        # Set test values to verify special character handling
        applicant = licence.getApplicants()[0]
        test_applicant_name = "Joséphine"
        test_street = "Rue du Château"
        test_city = "Chièvres"

        applicant.setName1(test_applicant_name)
        applicant.setStreet(test_street)
        applicant.setCity(test_city)

        res = urbain_xml_view.generateUrbainXML(brains, start, end)
        self.assertIn(test_applicant_name, res)
        self.assertIn(test_street, res)
        self.assertIn(test_city, res)
