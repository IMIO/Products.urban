# -*- coding: utf-8 -*-
from plone.testing import z2, zca, Layer
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting, FunctionalTesting
import Products.urban


URBAN_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                             package=Products.urban,
                             name='URBAN_ZCML')

URBAN_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, URBAN_ZCML),
                                 name='URBAN_Z2')

URBAN = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.urban,
    additional_z2_products=('Products.urban','Products.CMFPlacefulWorkflow'),
    gs_profile_id='Products.urban:default',
    name="URBAN")

URBAN_TESTS_PROFILE_DEFAULT = PloneWithPackageLayer(
    bases=(URBAN, ),
    zcml_filename="testing.zcml",
    zcml_package=Products.urban,
    additional_z2_products=('Products.urban',),
    gs_profile_id='Products.urban:default',
    name="URBAN_TESTS_PROFILE_DEFAULT")

class UrbanTestLayer(Layer):

    def setUp(self):
        portal = self['portal']
        applyProfile(portal, 'Products.urban:tests')

URBAN_TESTS_PROFILE = UrbanTestLayer(
    bases=(URBAN_TESTS_PROFILE_DEFAULT, ),
    name="URBAN_TESTS_PROFILE")

URBAN_INTEGRATION = IntegrationTesting(
    bases=(URBAN,), name="URBAN_INTEGRATION")

URBAN_TESTS_PROFILE_INTEGRATION = IntegrationTesting(
    bases=(URBAN_TESTS_PROFILE,), name="URBAN_TESTS_PROFILE_INTEGRATION")

URBAN_TESTS_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(URBAN_TESTS_PROFILE,), name="URBAN_TESTS_PROFILE_FUNCTIONAL")
