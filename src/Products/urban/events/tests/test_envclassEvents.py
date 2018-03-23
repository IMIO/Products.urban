# -*- coding: utf-8 -*-
import unittest
from Products.urban.testing import URBAN_TESTS_INTEGRATION

from Products.urban.events.envclassEvents import update_rubric_history
from Products.urban.events.envclassEvents import get_last_value_history

class TestEnvEvent(unittest.TestCase):
    layer = URBAN_TESTS_INTEGRATION

    def setUp(self):
        pass
        self.rubric = type('Rubric', (object,),)
        self.rubric.rubrics_history = []
        self.acl = type('ACL', (object,),)
        self.acl.acl_history = []



    def testCreationDatefoo(self):
        self.rubric.rubrics_history = ['element1']
        new_element = ['element1', 'element2']
        foo = get_last_value_history(self.rubric, 'rubrics_history')

        update_rubric_history(self.rubric)
        import pdb;pdb.set_trace()
        self.assertTrue(True)

