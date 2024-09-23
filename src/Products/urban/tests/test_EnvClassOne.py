# -*- coding: utf-8 -*-

from Products.urban import utils
from Products.urban.testing import URBAN_TESTS_INTEGRATION
from Products.urban.tests.helpers import BrowserTestCase
from Products.urban.tests.helpers import SchemaFieldsTestCase
from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser
from zope.globalrequest import getRequest
from zope.globalrequest import setRequest

import transaction
import urllib2


class TestEnvClassOneInstall(BrowserTestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.urban = self.portal.urban
        self.portal_urban = self.portal.portal_urban
        self.browser = Browser(self.portal)
        default_user = self.layer.environment_default_user
        default_password = self.layer.environment_default_password
        self.browserLogin(default_user, default_password)
        if not getRequest():
            setRequest(self.portal.REQUEST)

    def test_envclassone_config_folder_exists(self):
        msg = "envclassone config folder not created"
        self.assertTrue("envclassone" in self.portal_urban.objectIds(), msg)
        envclassone = self.portal_urban.envclassone
        from Products.urban.LicenceConfig import LicenceConfig

        self.assertTrue(isinstance(envclassone, LicenceConfig))

    def test_envclassone_config_folder_is_visible(self):
        msg = "envclassone config folder is not visible in urban config"
        self.browser.open(self.portal_urban.absolute_url())
        contents = self.browser.contents
        self.assertTrue("Permis d'environnement classe 1" in contents, msg)

    def test_envclassone_config_folder_is_editable(self):
        self.browserLogin("urbanmanager")
        try:
            edit_url = self.portal_urban.envclassone.absolute_url() + "/edit"
            self.browser.open(edit_url)
        except urllib2.HTTPError, e:
            self.fail(msg="Got HTTP response code:" + str(e.code))

    def test_envclassone_folder_exist(self):
        msg = "envclassones folder not created"
        self.assertTrue("envclassones" in self.urban.objectIds(), msg)

    def test_envclassone_addable_types(self):
        msg = "cannot create EnvClassOne in licence folder"
        addable_types = self.urban.envclassones.immediatelyAddableTypes
        self.assertTrue("EnvClassOne" in addable_types, msg)
        msg = "can create an other content type in licence folder"
        self.assertEqual(len(addable_types), 1, msg)

    def test_envclassone_licence_folder_link_in_urban_default_view(self):
        self.browser.open(self.urban.absolute_url())
        folder_url = utils.getLicenceFolder("EnvClassOne").absolute_url()
        link = self.browser.getLink(url=folder_url)
        self.assertEqual(link.text, "Permis d'environnement classe 1")
        link.click()
        contents = self.browser.contents
        self.assertTrue("Permis d'environnement classe 1" in contents)

    def test_EnvClassOne_is_under_env_licence_workflow(self):
        workflow_tool = api.portal.get_tool("portal_workflow")
        envclassone_workflow = workflow_tool.getChainForPortalType("EnvClassOne")
        self.assertTrue("env_licence_workflow" in envclassone_workflow)


class TestEnvClassOneInstance(SchemaFieldsTestCase):

    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.urban = self.portal.urban

        # create a test EnvClassOne licence
        default_user = self.layer.environment_default_user
        default_password = self.layer.environment_default_password
        login(self.portal, default_user)
        envclassone_folder = self.urban.envclassones
        testlicence_id = "test_envclassone"
        envclassone_folder.invokeFactory("EnvClassOne", id=testlicence_id)
        transaction.commit()
        self.licence = getattr(envclassone_folder, testlicence_id)

        self.browser = Browser(self.portal)
        self.browserLogin(default_user, default_password)
        if not getRequest():
            setRequest(self.portal.REQUEST)

    def tearDown(self):
        if self.licence.wl_isLocked():
            self.licence.wl_clearLocks()
        with api.env.adopt_roles(["Manager"]):
            if not getRequest():
                setRequest(self.portal.REQUEST)
            api.content.delete(self.licence)
        transaction.commit()

    def test_envclassone_licence_exists(self):
        self.assertTrue(len(self.urban.envclassones.objectIds()) > 0)

    def test_envclassone_view_is_registered(self):
        msg = "EnvClassOne view is not registered"
        login(self.portal, "environmenteditor")
        try:
            self.licence.restrictedTraverse("envclassoneview")
        except AttributeError:
            self.fail(msg=msg)

    def test_envclassone_view(self):
        try:
            self.browser.open(self.licence.absolute_url())
        except urllib2.HTTPError, e:
            self.fail(msg="Got HTTP response code:" + str(e.code))

    def test_envclassone_edit(self):
        self.browser.open(self.licence.absolute_url() + "/edit")
        contents = self.browser.contents
        self.assertTrue("Voirie" in contents)
        self.assertTrue("Métadonnées" not in contents)
        self.assertTrue("Données" not in contents)

    def test_envclassone_has_attribute_hasEnvironmentImpactStudy(self):
        self.assertTrue(self.licence.getField("hasEnvironmentImpactStudy"))

    def test_envclassone_hasEnvironmentImpactStudy_is_visible(self):
        self._is_field_visible("Étude d'incidences sur l'environnement")

    def test_envclassone_hasEnvironmentImpactStudy_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Étude d'incidences sur l'environnement")

    def test_envclassone_has_attribute_isSeveso(self):
        self.assertTrue(self.licence.getField("isSeveso"))

    def test_envclassone_isSeveso_is_visible(self):
        self._is_field_visible("Établissement SEVESO")

    def test_envclassone_isSeveso_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Établissement SEVESO")

    def test_envclassone_has_attribute_publicRoadModifications(self):
        self.assertTrue(self.licence.getField("publicRoadModifications"))

    def test_envclassone_publicRoadModifications_is_visible(self):
        self._is_field_visible(
            "Modifications souhaitées au tracé et à l'équipement des voiries publiques"
        )

    def test_envclassone_publicRoadModifications_is_visible_in_edit(self):
        self._is_field_visible_in_edit(
            "Modifications souhaitées au tracé et à l'équipement des voiries publiques"
        )

    def test_envclassone_has_attribute_previousLicences(self):
        self.assertTrue(self.licence.getField("previousLicences"))

    def test_envclassone_previousLicences_is_visible(self):
        self._is_field_visible(
            "Permissions, enregistrements et déclarations existantes"
        )

    def test_envclassone_has_attribute_validityDelay(self):
        self.assertTrue(self.licence.getField("validityDelay"))

    def test_envclassone_validityDelay_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Durée de validité du permis")

    def test_envclassone_validityDelay_is_visible(self):
        self._is_field_visible("Durée de validité du permis")

    def test_envclassone_has_attribute_authority(self):
        self.assertTrue(self.licence.getField("authority"))

    def test_envclassone_authority_is_visible_in_edit(self):
        self._is_field_visible_in_edit("Autorité compétente")

    def test_envclassone_authority_is_visible(self):
        self._is_field_visible("Autorité compétente")

    def test_envclassone_has_attribute_ftSolicitOpinionsTo(self):
        self.assertTrue(self.licence.getField("ftSolicitOpinionsTo"))

    def test_envclassone_ftSolicitOpinionsTo_is_visible_in_edit(self):
        self._is_field_visible_in_edit("")

    def test_envclassone_ftSolicitOpinionsTo_is_visible(self):
        self._is_field_visible("")

    def test_envclassone_referenceDGATLP_translation(self):
        """
        Field referenceDGATLP should be translated as 'reference ARNE'
        """
        self._is_field_visible("Référence ARNE")
        self._is_field_visible_in_edit("Référence ARNE")

    def test_envclassone_workLocation_translation(self):
        self._is_field_visible("Situation")
        self._is_field_visible_in_edit("Situation")
