# -*- coding: utf-8 -*-
#
# File: PortionOut.py
#
# Copyright (c) 2011 by CommunesPlone
# Generator: ArchGenXML Version 2.5
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
        name='divisionCode',
        widget=StringField._properties['widget'](
            label='Divisioncode',
            label_msgid='urban_label_divisionCode',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='division',
        widget=StringField._properties['widget'](
            label='Division',
            label_msgid='urban_label_division',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='section',
        widget=StringField._properties['widget'](
            label='Section',
            label_msgid='urban_label_section',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='radical',
        widget=StringField._properties['widget'](
            label='Radical',
            label_msgid='urban_label_radical',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='bis',
        widget=StringField._properties['widget'](
            label='Bis',
            label_msgid='urban_label_bis',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='exposant',
        widget=StringField._properties['widget'](
            label='Exposant',
            label_msgid='urban_label_exposant',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='puissance',
        widget=StringField._properties['widget'](
            label='Puissance',
            label_msgid='urban_label_puissance',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='partie',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Partie',
            label_msgid='urban_label_partie',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PortionOut_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
PortionOut_schema['title'].visible = False
##/code-section after-schema

class PortionOut(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IPortionOut)

    meta_type = 'PortionOut'
    _at_rename_after_creation = True

    schema = PortionOut_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def updateTitle(self):
        """
          Set a correct title if we use invokeFactory
        """
        division = self.getDivision()
        section = self.getSection()
        radical = self.getRadical()
        bis = self.getBis()
        exposant = self.getExposant()
        puissance = self.getPuissance()
        generatedTitle= str(division) +' '+ str(section) +' '+ str(radical) +' '+ str(bis) +' '+ str(exposant) + ' ' + str(puissance)
        generatedTitle=generatedTitle.strip()
        if self.getPartie():
            generatedTitle=generatedTitle+' (partie)'
        self.setTitle(generatedTitle)
        self.reindexObject()

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()
        #after creation, reindex the parent so the parcelInfosIndex is OK
        self.aq_inner.aq_parent.reindexObject()

    security.declarePublic('at_post_edit_script')
    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()
        #after creation, reindex the parent so the parcelInfosIndex is OK
        self.aq_inner.aq_parent.reindexObject()



registerType(PortionOut, PROJECTNAME)
# end of class PortionOut

##code-section module-footer #fill in your manual code here
##/code-section module-footer

