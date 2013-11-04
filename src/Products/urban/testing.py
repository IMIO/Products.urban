# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer, IntegrationTesting, FunctionalTesting, helpers
import Products.urban


URBAN_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                             package=Products.urban,
                             name='URBAN_ZCML')

URBAN_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, URBAN_ZCML),
                                 name='URBAN_Z2')

URBAN_TESTS_PROFILE_DEFAULT = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.urban,
    additional_z2_products=('Products.urban', 'Products.CMFPlacefulWorkflow'),
    gs_profile_id='Products.urban:tests',
    name="URBAN_TESTS_PROFILE_DEFAULT")


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
    def setUp(self):
        super(UrbanWithUsersLayer, self).setUp()
        with helpers.ploneSite() as portal:
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
            helpers.applyProfile(portal, 'Products.urban:testsWithConfig')

URBAN_TESTS_CONFIG = UrbanConfigLayer(
    bases=(URBAN_TESTS_PROFILE_DEFAULT, ), name="URBAN_TESTS_CONFIG")


class UrbanEnvclassOneLayer(UrbanWithUsersLayer):
    """
    Instanciate a EnvClassOne test licence

    Must collaborate with a layer that installs Plone and Urban
    Useful for performances: Plone site is instanciated only once
    """
    def setUp(self):
        super(UrbanEnvclassOneLayer, self).setUp()
        with helpers.ploneSite() as portal:
            helpers.login(portal, 'urbaneditor')
            portal.urban.envclassones.invokeFactory('EnvClassOne', id='test_licence_envclassone')

URBAN_TESTS_ENVCLASSONE = UrbanEnvclassOneLayer(
    bases=(URBAN_TESTS_PROFILE_DEFAULT, ), name="URBAN_TESTS_ENVCLASSONE")


class UrbanLicencesLayer(UrbanConfigLayer):
    """
    Instanciate licences

    Must collaborate with a layer that installs Plone and Urban
    Useful for performances: Plone site is instanciated only once
    """
    def setUp(self):
        super(UrbanLicencesLayer, self).setUp()
        with helpers.ploneSite() as portal:
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
            helpers.applyProfile(portal, 'Products.urban:tests-imports')

URBAN_IMPORTS = UrbanImportsLayer(
    bases=(URBAN_TESTS_PROFILE_DEFAULT, ), name="URBAN_IMPORTS")
