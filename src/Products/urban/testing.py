# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting, FunctionalTesting
import Products.urban


URBAN_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                             package=Products.urban,
                             name='URBAN_ZCML')

URBAN_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, URBAN_ZCML),
                                 name='URBAN_Z2')


class UrbanPloneLayer(PloneWithPackageLayer):

    def setUpZope(self, app, configurationContext):
        super(UrbanPloneLayer, self).setUpZope(app, configurationContext)
        z2.installProduct(app, 'Products.urban')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.urban')


URBAN = UrbanPloneLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.urban,
    gs_profile_id='Products.urban:default',
    name="URBAN")

URBAN_TESTS_PROFILE = PloneWithPackageLayer(
    bases=(URBAN, ),
    zcml_filename="testing.zcml",
    zcml_package=Products.urban,
    gs_profile_id='Products.urban:tests',
    name="URBAN_TESTS_PROFILE")

URBAN_INTEGRATION = IntegrationTesting(
    bases=(URBAN,), name="URBAN_INTEGRATION")

URBAN_TESTS_PROFILE_INTEGRATION = IntegrationTesting(
    bases=(URBAN_TESTS_PROFILE,), name="URBAN_TESTS_PROFILE_INTEGRATION")

URBAN_TESTS_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(URBAN_TESTS_PROFILE,), name="URBAN_TESTS_PROFILE_FUNCTIONAL")
