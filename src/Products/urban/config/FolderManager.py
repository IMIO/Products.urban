# -*- coding: utf-8 -*-
#
# File: FolderManager.py
#
# Copyright (c) 2014 by CommunesPlone
# Generator: ArchGenXML Version 2.7
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
        vocabulary=UrbanVocabulary('persons_grades', inUrbanConfig=False),
    ),
    StringField(
        name='ploneUserId',
        widget=StringField._properties['widget'](
            label='Ploneuserid',
            label_msgid='urban_label_ploneUserId',
            i18n_domain='urban',
        ),
    ),
    LinesField(
        name='manageableLicences',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Manageablelicences',
            label_msgid='urban_label_manageableLicences',
            i18n_domain='urban',
        ),
        multiValued=True,
        vocabulary='listLicenceTypes',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

FolderManager_schema = Contact.schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
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
    ##/code-section class-header

    # Methods

registerType(FolderManager, PROJECTNAME)
# end of class FolderManager

##code-section module-footer #fill in your manual code here
##/code-section module-footer

