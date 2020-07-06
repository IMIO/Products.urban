# -*- coding: utf-8 -*-
import unittest
from Products.urban.content.licence.BuildLicence import BuildLicence
from Products.urban.interfaces import IBuildLicence, IGenericLicence
from Products.urban.testing import URBAN_TESTS_PROFILE_DEFAULT


class TestInterfaces(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_DEFAULT

    def testGenericLicenceInterface(self):
        buildLicence = BuildLicence("build1")
        self.failUnless(IBuildLicence.providedBy(buildLicence))
        self.failUnless(IGenericLicence.providedBy(buildLicence))
