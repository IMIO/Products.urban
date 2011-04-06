# -*- coding: utf-8 -*-
#
# File: testMeetingItem.py
#
# Copyright (c) 2007 by PloneGov
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from DateTime import DateTime
from Products.urban.UrbanTool import *
from Products.urban.tests.urbanTestCase import urbanTestCase

class testUrbanTool(urbanTestCase):
    
    def afterSetUp(self):
        """
        """
        pass    

    def test_generateReference(self):
        '''
           Test if generateReference is OK...
        '''
        tool = self.portal.portal_urban
        self.assertEqual(tool.generateReference('1234'),'1235')
        self.assertEqual(tool.generateReference('xxx1234'),'xxx1235')
        self.assertEqual(tool.generateReference('1234xxx'),'1235xxx')
        self.assertEqual(tool.generateReference('xxx1234xxx'),'xxx1235xxx')
        self.assertEqual(tool.generateReference('xxx'),'xxx1')
        self.assertEqual(tool.generateReference('xxx1234xxx1234xxx'),'xxx1234xxx1235xxx')
        self.assertEqual(tool.generateReference('xxx1234xxx1234'),'xxx1234xxx1235')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testUrbanTool))
    return suite
