# -*- coding: utf-8 -*-

from Products.urban.schedule.delay import UrbanBaseDelay

import unittest


class TestUrbanBaseDelay(unittest.TestCase):
    def test_get_default_delay_value(self):
        # Archetypes default value of delay fields is [""]
        self.assertEqual(UrbanBaseDelay.get_default_delay_value([""]), "")
