# -*- coding: utf-8 -*-

from Products.GenericSetup.tool import DEPENDENCY_STRATEGY_NEW
from Products.urban.utils import run_entry_points
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import helpers
from plone.testing import z2
from zope.globalrequest import setRequest

import Products.urban


class UrbanLayer(PloneWithPackageLayer):
    def setUpPloneSite(self, portal):
        setRequest(portal.REQUEST)
        super(UrbanLayer, self).setUpPloneSite(portal)


URBAN_TESTS_PROFILE_DEFAULT = UrbanLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.urban,
    additional_z2_products=(
        'Products.urban',
        'Products.CMFPlacefulWorkflow',
        'imio.dashboard',
    ),
    gs_profile_id='Products.urban:tests',
    name="URBAN_TESTS_PROFILE_DEFAULT")

run_entry_points('Products.urban.testing.profile', 'base', URBAN_TESTS_PROFILE_DEFAULT)

URBAN_TESTS_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(URBAN_TESTS_PROFILE_DEFAULT,), name="URBAN_TESTS_PROFILE_FUNCTIONAL")


class UrbanWithUsersLayer(IntegrationTesting):
    """
    Instanciate test users

    Must collaborate with a layer that installs Plone and Urban
    Useful for performances: Plone site is instanciated only once
    """
    default_user = 'urbaneditor'
    default_password = 'urbaneditor'
    environment_default_user = 'environmenteditor'
    environment_default_password = 'environmenteditor'
    default_admin_user = 'urbanmanager'
    default_admin_password = 'urbanmanager'

    def setUp(self):
        # monkey patch to avoid running upgrade steps when reisntalling urban
        Products.GenericSetup.tool.DEFAULT_DEPENDENCY_STRATEGY = DEPENDENCY_STRATEGY_NEW
        super(UrbanWithUsersLayer, self).setUp()
        with helpers.ploneSite() as portal:
            portal_urban = portal.portal_urban
            cache_view = portal_urban.unrestrictedTraverse('urban_vocabulary_cache')
            cache_view.reset_all_cache()
            Products.urban.config.NIS = '92000'  # mock NIS code
            portal.setupCurrentSkin(portal.REQUEST)
            setRequest(portal.REQUEST)
            from Products.urban.setuphandlers import addTestUsers
            addTestUsers(portal)


URBAN_TESTS_INTEGRATION = UrbanWithUsersLayer(
    bases=(URBAN_TESTS_PROFILE_DEFAULT, ), name="URBAN_TESTS_INTEGRATION")


class UrbanConfigLayer(UrbanWithUsersLayer):
    """
    Instanciate urban config

    Must collaborate with a layer that installs Plone and Urban
    Useful for performances: Plone site is instanciated only once
    """
    def setUp(self):
        super(UrbanConfigLayer, self).setUp()
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
            setRequest(portal.REQUEST)
            helpers.applyProfile(portal, 'Products.urban:testsWithConfig')


URBAN_TESTS_CONFIG = UrbanConfigLayer(
    bases=(URBAN_TESTS_PROFILE_DEFAULT, ), name="URBAN_TESTS_CONFIG")


class UrbanLicencesLayer(UrbanConfigLayer):
    """
    Instanciate licences

    Must collaborate with a layer that installs Plone and Urban
    Useful for performances: Plone site is instanciated only once
    """
    def setUp(self):
        super(UrbanLicencesLayer, self).setUp()
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
            setRequest(portal.REQUEST)
            helpers.applyProfile(portal, 'Products.urban:testsWithLicences')


URBAN_TESTS_LICENCES = UrbanLicencesLayer(
    bases=(URBAN_TESTS_PROFILE_DEFAULT, ), name="URBAN_TESTS_LICENCES")


class UrbanImportsLayer(IntegrationTesting):
    """
    Must collaborate with a layer that installs Plone and Urban
    Useful for performances: Plone site is instanciated only once
    """
    def setUp(self):
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
            setRequest(portal.REQUEST)
            Products.urban.config.NIS = '92000'  # mock NIS code
            helpers.applyProfile(portal, 'Products.urban:tests-imports')


URBAN_IMPORTS = UrbanImportsLayer(
    bases=(URBAN_TESTS_PROFILE_DEFAULT, ), name="URBAN_IMPORTS")


class UrbanWithUsersFunctionalLayer(FunctionalTesting):
    """
    Instanciate test users

    Must collaborate with a layer that installs Plone and Urban
    Useful for performances: Plone site is instanciated only once
    """
    default_user = 'urbaneditor'
    default_password = 'urbaneditor'
    environment_default_user = 'environmenteditor'
    environment_default_password = 'environmenteditor'

    def setUp(self):
        Products.urban.config.NIS = '92000'  # mock NIS code
        # monkey patch to avoid running upgrade steps when reisntalling urban
        Products.GenericSetup.tool.DEFAULT_DEPENDENCY_STRATEGY = DEPENDENCY_STRATEGY_NEW
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
            setRequest(portal.REQUEST)
            from Products.urban.setuphandlers import addTestUsers
            addTestUsers(portal)


URBAN_TESTS_FUNCTIONAL = UrbanWithUsersFunctionalLayer(
    bases=(URBAN_TESTS_PROFILE_DEFAULT, ), name="URBAN_TESTS_FUNCTIONAL")


class UrbanConfigFunctionalLayer(UrbanWithUsersFunctionalLayer):
    """
    Instanciate urban config

    Must collaborate with a layer that installs Plone and Urban
    Useful for performances: Plone site is instanciated only once
    """
    def setUp(self):
        super(UrbanConfigFunctionalLayer, self).setUp()
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
            setRequest(portal.REQUEST)
            helpers.applyProfile(portal, 'Products.urban:testsWithConfig')


URBAN_TESTS_CONFIG_FUNCTIONAL = UrbanConfigFunctionalLayer(
    bases=(URBAN_TESTS_PROFILE_DEFAULT, ), name="URBAN_TESTS_CONFIG_FUNCTIONAL")


class UrbanLicencesFunctionalLayer(UrbanConfigFunctionalLayer):
    """
    Instanciate licences

    Must collaborate with a layer that installs Plone and Urban
    Useful for performances: Plone site is instanciated only once
    """
    def setUp(self):
        super(UrbanLicencesFunctionalLayer, self).setUp()
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
            setRequest(portal.REQUEST)
            helpers.applyProfile(portal, 'Products.urban:testsWithLicences')


URBAN_TESTS_LICENCES_FUNCTIONAL = UrbanLicencesFunctionalLayer(
    bases=(URBAN_TESTS_PROFILE_DEFAULT, ), name="URBAN_TESTS_LICENCES_FUNCTIONAL")


URBAN_TEST_ROBOT = UrbanConfigFunctionalLayer(
    bases=(
        URBAN_TESTS_PROFILE_DEFAULT,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name="URBAN_TEST_ROBOT"
)

# override test layers with those defined in specific profiles
all_layers = [obj for obj in locals().values() if isinstance(obj, (IntegrationTesting, FunctionalTesting))]
new_layers = run_entry_points('Products.urban.testing.profile', 'layers', all_layers) or {}
_this_module_ = globals()
for layer_name, new_layer in new_layers.iteritems():
    _this_module_[layer_name] = new_layer
