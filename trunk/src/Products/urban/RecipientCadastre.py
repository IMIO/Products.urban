# -*- coding: utf-8 -*-
#
# File: RecipientCadastre.py
#
# Copyright (c) 2015 by CommunesPlone
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
        name='name',
        widget=StringField._properties['widget'](
            label='Name',
            label_msgid='urban_label_name',
            i18n_domain='urban',
        ),
        required=True,
    ),
    StringField(
        name='adr1',
        widget=StringField._properties['widget'](
            label='Adr1',
            label_msgid='urban_label_adr1',
            i18n_domain='urban',
        ),
        required=True,
    ),
    StringField(
        name='adr2',
        widget=StringField._properties['widget'](
            label='Adr2',
            label_msgid='urban_label_adr2',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='street',
        widget=StringField._properties['widget'](
            label='Street',
            label_msgid='urban_label_street',
            i18n_domain='urban',
        ),
        required=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

RecipientCadastre_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
RecipientCadastre_schema['title'].widget.visible = False
RecipientCadastre_schema['adr2'].widget.visible = False
##/code-section after-schema

class RecipientCadastre(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IRecipientCadastre)

    meta_type = 'RecipientCadastre'
    _at_rename_after_creation = True

    schema = RecipientCadastre_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def getParcels(self):
        """
          Return contained Parcels...
        """
        return self.objectValues("PortionOut")

    def getParcelsForDisplay(self):
        """
          Return contained Parcels for being displayed...
        """
        res = []
        for parcel in self.getParcels():
            res.append(parcel.Title())
        return '<br />'.join(res)

    def getRecipientAddress(self):
        return self.getAdr1()+' '+self.getAdr2()



registerType(RecipientCadastre, PROJECTNAME)
# end of class RecipientCadastre

##code-section module-footer #fill in your manual code here
##/code-section module-footer

