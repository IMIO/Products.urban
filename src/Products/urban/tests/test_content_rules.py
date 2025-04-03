# -*- coding: utf-8 -*-

import unittest2 as unittest
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL
from Products.urban import utils
from Products.urban.setuphandlers import setFolderAllowedTypes
from Products.urban.contentrules.stringinterp import FolderManagersMail
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes

from plone.app.testing import login
from plone import api

import transaction

EMAIL = "urbanmanager@urban.be"

class TestFolderManagersMail(unittest.TestCase):
    layer=URBAN_TESTS_CONFIG_FUNCTIONAL

    def setUp(self):
        portal = self.layer["portal"]
        self.portal = portal
        self.codt_buildlicences = portal.urban.codt_buildlicences
        default_user = self.layer.default_user
        login(portal, default_user)
        self.licence = api.content.create(
            container=self.codt_buildlicences,
            type="CODT_BuildLicence",
            id="newlicence"
        )
        self.folder_manager = self.portal.portal_urban.foldermanagers.foldermanager1
        self.urbanmanager_user = api.user.get(username="urbanmanager")

    def test_without_folder_manager(self):
        folder_managers_mail = FolderManagersMail(self.licence)
        self.assertEqual(folder_managers_mail(), "")

    def test_folder_manager_no_mail_user_no_mail(self):
        self.licence.setFoldermanagers([self.folder_manager.UID()])
        folder_managers_mail = FolderManagersMail(self.licence)
        self.assertEqual(folder_managers_mail(), "")

    def test_folder_manager_no_mail_user_mail(self):
        self.urbanmanager_user.setProperties(email=EMAIL)
        self.licence.setFoldermanagers([self.folder_manager.UID()])
        folder_managers_mail = FolderManagersMail(self.licence)
        self.assertEqual(folder_managers_mail(), EMAIL)

    def test_folder_manager_mail_user_no_mail(self):
        self.folder_manager.setEmail(EMAIL)
        self.licence.setFoldermanagers([self.folder_manager.UID()])
        folder_managers_mail = FolderManagersMail(self.licence)
        self.assertEqual(folder_managers_mail(), EMAIL)