# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2008 by CommunesPlone
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

# ------------------------------------------------------------------------------
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.PloneTask.Task import Task
from Products.PloneTask.interfaces import ITaskCustom
# ------------------------------------------------------------------------------
class CustomTask(Task):
    '''Adapter that adapts a task implementing ITask to the
       interface ITaskCustom.'''

    implements(ITaskCustom)
    security = ClassSecurityInfo()

    def __init__(self, item):
        self.context = item

    security.declarePublic('isClosed')
    def isClosed(self):
        '''Check if a task is closed...'''
        #closed if the state is 'closed'... ;-)
        metaType = self.context.meta_type
        if metaType == "UrbanEvent":
            if self.context.portal_workflow.getInfoFor(self.context, 'review_state') == "closed":
                return True
            else:
                return False
        elif metaType == "BuildLicence":
            if self.context.portal_workflow.getInfoFor(self.context, 'review_state') in ['accepted', 'refused', ]:
                return True
            else:
                return False

# ------------------------------------------------------------------------------
InitializeClass(CustomTask)
# ------------------------------------------------------------------------------
