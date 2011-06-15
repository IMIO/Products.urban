# -*- coding: utf-8 -*-
#
# File: FolderManager.py
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
from Contact import Contact
from zope.i18n import translate as _
from Products.urban.utils import setRawSchema
##/code-section module-header

schema = Schema((

    StringField(
        name='initials',
        widget=StringField._properties['widget'](
            label='Initials',
            label_msgid='urban_label_initials',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='grade',
        widget=SelectionWidget(
            format='select',
            label='Grade',
            label_msgid='urban_label_grade',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        vocabulary='listGrades',
    ),
    StringField(
        name='ploneUserId',
        widget=StringField._properties['widget'](
            label='Ploneuserid',
            label_msgid='urban_label_ploneUserId',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setRawSchema(schema)
##/code-section after-local-schema

FolderManager_schema = Contact.schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
FolderManager_schema.moveField('initials', before='street')
FolderManager_schema.moveField('grade', before='street')
##/code-section after-schema

class FolderManager(BaseContent, Contact, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IFolderManager)

    meta_type = 'FolderManager'
    _at_rename_after_creation = True

    schema = FolderManager_schema

    ##code-section class-header #fill in your manual code here
    del schema['title']
    archetype_name = 'FolderManager'
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('Title')
    def Title(self):
        """
          Return a correctly formatted title
        """
        return self.getName1() + " " + self.getName2() + " (" + self.displayValue(self.listGrades(),self.getGrade()) + ")"

    security.declarePublic('listGrades')
    def listGrades(self):
        """
          Return a list of available grades from the configuration
        """
        return DisplayList(self.portal_urban.listVocabulary('persons_grades', self, inUrbanConfig=False))



registerType(FolderManager, PROJECTNAME)
# end of class FolderManager

##code-section module-footer #fill in your manual code here
##/code-section module-footer

