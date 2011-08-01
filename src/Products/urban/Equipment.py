# -*- coding: utf-8 -*-
#
# File: Equipment.py
#
# Copyright (c) 2011 by CommunesPlone
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

    StringField(
        name='EquipmentType',
        widget=SelectionWidget(
            label='Equipmenttype',
            label_msgid='urban_label_EquipmentType',
            i18n_domain='urban',
        ),
        vocabulary='listEquipmentType',
    ),
    DateTimeField(
        name='launchDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            label='Launchdate',
            label_msgid='urban_label_launchDate',
            i18n_domain='urban',
        ),
    ),
    TextField(
        name='description',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Description',
            label_msgid='urban_label_description',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        accessor="Description",
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Equipment_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Equipment_schema['title'].widget.visible = False
Equipment_schema['title'].required = False
##/code-section after-schema

class Equipment(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IEquipment)

    meta_type = 'Equipment'
    _at_rename_after_creation = True

    schema = Equipment_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('listEquipmentType')
    def listEquipmentType(self):
        """
         Return the list of equipment types defined in portal_urban
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('equipmenttypes', self))

    def updateTitle(self):
        """
          Set a correct title if we use invokeFactory
        """
        self.setTitle(self.displayValue(self.listEquipmentType(), self.getEquipmentType())
)
        self.reindexObject()

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()

    security.declarePublic('at_post_edit_script')
    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()



registerType(Equipment, PROJECTNAME)
# end of class Equipment

##code-section module-footer #fill in your manual code here
##/code-section module-footer

