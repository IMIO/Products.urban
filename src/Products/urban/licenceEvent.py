# -*- coding: utf-8 -*-
#
# File: licenceEvent.py
#
# Copyright (c) 2007 by CommunesPlone
# Generator: ArchGenXML Version 1.5.3 dev/svn
#            http://plone.org/products/archgenxml
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

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='eventDate',
        widget=CalendarWidget(
            label='Eventdate',
            label_msgid='urban_label_eventDate',
            i18n_domain='urban',
        )
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

licenceEvent_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class licenceEvent(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'licenceEvent'

    meta_type = 'licenceEvent'
    portal_type = 'licenceEvent'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 1
    #content_icon = 'licenceEvent.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "licenceEvent"
    typeDescMsgId = 'description_edit_licenceevent'

    _at_rename_after_creation = True

    schema = licenceEvent_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(licenceEvent, PROJECTNAME)
# end of class licenceEvent

##code-section module-footer #fill in your manual code here
##/code-section module-footer



