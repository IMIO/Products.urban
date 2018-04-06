#-*- coding: utf-8 -*-
from plone.app.testing import login, quickInstallProduct
from Products.urban.testing import URBAN_TESTS_LICENCES
from Products.urban.tests.helpers import BrowserTestCase

from plone.testing.z2 import Browser

from testfixtures import compare, StringComparison as S

import transaction


class TestTabsConfigView(BrowserTestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        self.portal = self.layer['portal']
        self.urban = self.portal.urban
        self.buildlicence = self.urban.buildlicences.objectValues('BuildLicence')[0]

        #isntall datagridfield so we can edit the tabs config
        quickInstallProduct(self.portal, 'Products.DataGridField')
        quickInstallProduct(self.portal, 'Products.ATReferenceBrowserWidget')
        quickInstallProduct(self.portal, 'Products.MasterSelectWidget')
        quickInstallProduct(self.portal, 'collective.datagridcolumns')

        default_user = self.layer.default_user
        default_password = self.layer.default_password
        login(self.portal, default_user)
        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)
        self.browser.handleErrors = False

    def testLicenceViewsDisplay(self):
        """
          check that any licence view is not broken for whatsoever reason
        """
        from Products.urban.config import URBAN_TYPES
        for licence_type in URBAN_TYPES:
            licences = getattr(self.urban, '%ss' % licence_type.lower()).objectValues()
            if licences:
                licence = licences[0]
                self.browser.open(licence.absolute_url())

    def testTabsReordering(self):
        """
         Put location tab on first postion in the buildlicence tabs config
         then check that this order is respected on some buildlicence view
        """
        buildlicence = self.buildlicence
        # first the tab order should be: description -> road -> location-> ...
        self.browser.open(buildlicence.absolute_url())
        compare(S(".*fieldsetlegend-urban_description.*fieldsetlegend-urban_location.*"), self.browser.contents.replace('\n', ''))
        # reorder the tabs in the config : location -> road -> description -> ...
        config = self.portal.portal_urban.buildlicence
        order = config.getTabsConfig()
        new_tab_order = [order[4]] + list(order[:4]) + list(order[5:])
        field = config.getField('tabsConfig')
        field.allow_delete = True
        config.setTabsConfig(new_tab_order)
        config.reindexObject()
        field.allow_delete = False
        transaction.commit()

        # the order should change on the licence display
        self.browser.open(buildlicence.absolute_url())
        compare(S(".*fieldsetlegend-urban_location.*fieldsetlegend-urban_description.*"), self.browser.contents.replace('\n', ''))
