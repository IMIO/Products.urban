# -*- coding: utf-8 -*-
from Products.urban.content.licence.BuildLicence import BuildLicence
from Products.urban.interfaces import IBuildLicence
from Products.urban.interfaces import IGenericLicence
from Products.urban.testing import URBAN_TESTS_PROFILE_DEFAULT

import unittest


class TestInterfaces(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_DEFAULT

    def testGenericLicenceInterface(self):
        buildLicence = BuildLicence("build1")
        self.failUnless(IBuildLicence.providedBy(buildLicence))
        self.failUnless(IGenericLicence.providedBy(buildLicence))
