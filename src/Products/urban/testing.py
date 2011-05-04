# -*- coding: utf-8 -*-
from plone.testing import z2
from plone.app.testing import (PloneWithPackageLayer, PLONE_FIXTURE, IntegrationTesting,
                               applyProfile)
import Products.urban


class UrbanPloneWithPackageLayer(PloneWithPackageLayer):

    def setUpZope(self, app, configurationContext):
        super(UrbanPloneWithPackageLayer, self).setUpZope(app, configurationContext)
        z2.installProduct(app, 'Products.urban')

    def applyProfiles(self, portal):
        super(UrbanPloneWithPackageLayer, self).applyProfiles(portal)
        applyProfile(portal, 'Products.urban:tests')


PLONE_WITH_URBAN_INSTALLED = UrbanPloneWithPackageLayer(bases=(PLONE_FIXTURE,),
                                                       zcml_filename="testing.zcml",
                                                       zcml_package=Products.urban,
                                                  gs_profile_id='Products.urban:default',
                                                  name="PLONE_WITH_URBAN_INSTALLED")

URBAN_WITH_PLONE = IntegrationTesting(bases=(PLONE_WITH_URBAN_INSTALLED,), name="URBAN_WITH_PLONE")
