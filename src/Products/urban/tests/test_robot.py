from Products.urban.testing import URBAN_TEST_ROBOT
from plone.testing import layered

import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    #    suite.addTests([
    #        layered(
    #            robotsuite.RobotTestSuite('test_specificfeatures.robot'),
    #            layer=URBAN_TEST_ROBOT
    #        ),
    #    ])
    return suite
