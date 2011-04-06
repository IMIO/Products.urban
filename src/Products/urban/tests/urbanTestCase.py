# -*- coding: utf-8 -*-
#
# Copyright (c) 2008 by PloneGov
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

import os.path
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from AccessControl.SecurityManagement import getSecurityManager
from ZPublisher.HTTPRequest import FileUpload

# Initialize Zope & Plone test systems.
ZopeTestCase.installProduct('urban')
PloneTestCase.setupPloneSite(products=['urban'])

class urbanTestCase(PloneTestCase.PloneTestCase):
    '''Base class for defining urban test cases.'''

    def afterSetUp(self):
        """
        """
        pass