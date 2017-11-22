# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import helpers

from plone.testing import z2
from Products.urban.utils import run_entry_points

import Products.urban


URBAN_TESTS_PROFILE_DEFAULT = PloneWithPackageLayer(
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


URBAN_TESTS_PROFILE_INTEGRATION = IntegrationTesting(
    bases=(URBAN_TESTS_PROFILE_DEFAULT,), name="URBAN_TESTS_PROFILE_INTEGRATION")

URBAN_TESTS_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(URBAN_TESTS_PROFILE_DEFAULT,), name="URBAN_TESTS_PROFILE_FUNCTIONAL")


class UrbanWithUsersLayer(IntegrationTesting):
    """
    Instanciate test users

    Must collaborate with a layer that installs Plone and Urban
    Useful for performances: Plone site is instanciated only once
    """
    default_user = 'urbanmanager'
    default_password = 'urbanmanager'

    def setUp(self):
        super(UrbanWithUsersLayer, self).setUp()
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
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
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
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
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
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

    def setUp(self):
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
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
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
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
        with helpers.ploneSite() as portal:
            portal.setupCurrentSkin(portal.REQUEST)
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
new_layers = run_entry_points('Products.urban.testing.profile', 'layers', all_layers)
_this_module_ = globals()
for layer_name, new_layer in new_layers.iteritems():
    _this_module_[layer_name] = new_layer
