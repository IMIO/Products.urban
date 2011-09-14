# -*- coding: utf-8 -*-
import unittest
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL

from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from testfixtures import compare, StringComparison as S


class TestSearchStreetsForm(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        #self.request = self.layer['request']
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.buildLicences = self.urban.buildlicences
        self.searchByStreets = self.urban.urban_searchbystreet
        login(self.portal, 'urbaneditor')
        self.browser = Browser(self.portal)
        self.browserLogin('urbaneditor')

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def testSearchStreetsWithoutContent(self):
        """perform a streets search without content,
           thus no result must be returned
        """
        self.browser.open(self.urban.absolute_url() + '/urban_searchbystreet')
        self.browser.getControl("Rechercher").click()
        compare(S("(?s).*sultats de la recherche courante.*"),
                self.browser.contents)

    def testSearchStreetsBuildlicenceWithoutStreet(self):
        """create a buildlience content without a street
           and check that this content is found
           if search is performed without indicating a particular street
        """
        #create a buildlicence content
        self.buildLicences = self.urban.buildlicences
        self.buildLicences.invokeFactory('BuildLicence', 'buildlicence1',
                title=u"test_buildlicence")
        import transaction
        transaction.commit()
        self.browser.open(self.urban.absolute_url() + '/urban_searchbystreet')
        self.browser.getControl("Rechercher").click()
        compare(S("(?s).*sultats de la recherche courante.*"),
                self.browser.contents)

    def testSearchStreetsNoBuildlicenceWithoutStreet(self):
        """create a buildlicence content item without a street
           and check that this content is not found
           if search is performed without indicating a particular street
           and by deselecting buildlicence type
        """
        #create a buildlicence content
        self.buildLicences = self.urban.buildlicences
        self.buildLicences.invokeFactory('BuildLicence', 'buildlicence1',
                title=u"test_buildlicence")
        import transaction
        transaction.commit()
        self.browser.open(self.urban.absolute_url() + '/urban_searchbystreet')
        #deselect buildlicence type as content to find
        self.browser.getControl(name='form.BuildLicence').value = False
        self.browser.getControl("Rechercher").click()
        self.assertFalse("sultats de la recherche courante" in
                self.browser.contents)

    def testSearchStreetsDeclarationWithoutStreet(self):
        """create a buildlience content without a street
           and check that this content is found
           if search is performed without indicating a particular street
        """
        #create a declaration content
        self.declarations = self.urban.declarations
        self.declarations.invokeFactory('Declaration', 'declaration1',
                title=u"test_declaration")
        import transaction
        transaction.commit()
        self.browser.open(self.urban.absolute_url() + '/urban_searchbystreet')
        self.browser.getControl("Rechercher").click()
        compare(S("(?s).*sultats de la recherche courante.*"),
                self.browser.contents)

    def testSearchStreetsNotDeclarationWithoutStreet(self):
        """create a buildlicence content without a street
           and check that this content is not found
           if search is performed without indicating a particular street
           and by deselecting buildlicence type
        """
        #create a declaration content
        self.declarations = self.urban.declarations
        self.declarations.invokeFactory('Declaration', 'declaration1',
                title=u"test_declaration")
        import transaction
        transaction.commit()
        self.browser.open(self.urban.absolute_url() + '/urban_searchbystreet')
        #deselect declaration type as content to find
        self.browser.getControl(name='form.Declaration').value = False
        self.browser.getControl("Rechercher").click()
        compare(S("(?s).*sultats de la recherche courante.*"),
                self.browser.contents)

    def XXXtestSearchStreetsBuildlicenceWithStreet(self):
        """create a buildlicence content with a street location.
           Check that this content is found
           if search is performed by indicating a particular street
        """
        #create a buildlicence content
        self.buildLicences = self.urban.buildlicences
        self.buildLicences.invokeFactory('BuildLicence', 'buildlicence1',
                title=u"test_buildlicence")
        #edit this latter and add a street
        self.buildLicence = getattr(self.buildLicences, 'buildlicence1')
        self.streets = self.catalog(portal_type='Street')
        self.street = self.streets[0].getObject()
        self.buildLicence.setWorkLocations((
            {'link': self.streets[0].getURL(), 'numero': '12',
             'orderindex_': '1', 'title': self.street.Title(),
             'uid': self.street.UID()},
            {'link': '', 'numero': '', 'orderindex_': 'template_row_marker',
            'title': '', 'uid': ''}))
        import transaction
        transaction.commit()
        self.browser.open(self.urban.absolute_url() + '/urban_searchbystreet')
        self.browser.getControl(name='form.streetSearch.to').value = [
                self.street.UID(), ]
        self.browser.getControl("Rechercher").click()
        compare(S("(?s).*sultats de la recherche courante.*"),
                self.browser.contents)
