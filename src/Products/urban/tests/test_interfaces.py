# -*- coding: utf-8 -*-
import unittest
from Products.urban.BuildLicence import BuildLicence
from Products.urban.interfaces import IBuildLicence, IGenericLicence
from Products.urban.testing import URBAN_Z2


class TestInterfaces(unittest.TestCase):

    layer = URBAN_Z2

    def testGenericLicenceInterface(self):
        buildLicence = BuildLicence('build1')
        self.failUnless(IBuildLicence.providedBy(buildLicence))
        self.failUnless(IGenericLicence.providedBy(buildLicence))
