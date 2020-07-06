# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL
from Products.urban.tests.helpers import BrowserTestCase

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser

import re
import transaction


class TestUrbanConfig(BrowserTestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.config = portal.portal_urban

        default_user = self.layer.default_user
        default_password = self.layer.default_password
        login(self.portal, default_user)
        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)
        self.browser.handleErrors = False

    def test_urbanconfig_view_display(self):
        """
         Tests urban config view is not broken for whatsoever reason
        """
        self.browser.open(self.config.absolute_url())

    def test_architects_config_view_display(self):
        """
         Tests architects folder view is not broken for whatsoever reason
        """
        self.browser.open(self.portal.urban.architects.absolute_url())

    def test_notaries_config_view_display(self):
        """
         Tests notaries folder view is not broken for whatsoever reason
        """
        self.browser.open(self.portal.urban.notaries.absolute_url())

    def test_geometricians_config_view_display(self):
        """
         Tests geometricians folder view is not broken for whatsoever reason
        """
        self.browser.open(self.portal.urban.geometricians.absolute_url())

    def test_parcellings_config_view_display(self):
        """
         Tests parcellings view is not broken for whatsoever reason
        """
        self.browser.open(self.portal.urban.parcellings.absolute_url())

    def test_foldermanagers_view_layout(self):
        """
        foldermanagers layout should be sorted_title_folderview
        """
        fm_folder = self.portal.portal_urban.foldermanagers
        self.assertEqual(fm_folder.getLayout(), 'sorted_title_folderview')


class TestUrbanConfigFunctional(BrowserTestCase):

    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.config = portal.portal_urban

        default_user = self.layer.default_user
        default_password = self.layer.default_password
        login(self.portal, default_user)
        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)
        self.browser.handleErrors = False

    def test_foldermanagers_view_sorting(self):
        fm_folder = self.portal.portal_urban.foldermanagers
        foldermanager1 = fm_folder.objectValues()[0]
        with api.env.adopt_roles(['Manager']):
            foldermanager2 = api.content.create(
                type='FolderManager', container=fm_folder, id='foldermanager2',
                name1='Bedot', name2='Alain', grade='agent-technique'
            )
            foldermanager3 = api.content.create(
                type='FolderManager', container=fm_folder, id='foldermanager3',
                name1='Madant', name2='Marc', grade='agent-technique'
            )
            transaction.commit()
        self.browser.open(fm_folder.absolute_url())
        regex = "{}.*{}.*{}".format(foldermanager2.Title(), foldermanager1.Title(), foldermanager3.Title())
        regex = regex.replace('(', '\(').replace(')', '\)')  # escape parenthesis
        self.assertTrue(re.search(regex, self.browser.contents, flags=re.DOTALL))
