# -*- coding: utf-8 -*-
#
# File: Lot.py
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
from Products.urban.utils import setRawSchema
##/code-section module-header

schema = Schema((

    StringField(
        name='surface',
        widget=StringField._properties['widget'](
            label='Surface',
            label_msgid='urban_label_surface',
            i18n_domain='urban',
        ),
    ),
    LinesField(
        name='usage',
        widget=MultiSelectionWidget(
            label_msgid="urban_label_lotusage",
            label='Usage',
            i18n_domain='urban',
        ),
        multiValued=True,
        vocabulary='listUsages',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setRawSchema(schema)
##/code-section after-local-schema

Lot_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Lot(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ILot)

    meta_type = 'Lot'
    _at_rename_after_creation = True

    schema = Lot_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('listUsages')
    def listUsages(self):
        """
          Return a list usages from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('lotusages', self))



registerType(Lot, PROJECTNAME)
# end of class Lot

##code-section module-footer #fill in your manual code here
##/code-section module-footer

