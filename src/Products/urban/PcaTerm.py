# -*- coding: utf-8 -*-
#
# File: PcaTerm.py
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
from Products.PageTemplates.GlobalTranslationService import getGlobalTranslationService
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            visible=False,
            label='Title',
            label_msgid='urban_label_title',
            i18n_domain='urban',
        ),
        accessor="Title",
    ),
    StringField(
        name='label',
        widget=StringField._properties['widget'](
            label='Label',
            label_msgid='urban_label_label',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='number',
        widget=StringField._properties['widget'](
            label='Number',
            label_msgid='urban_label_number',
            i18n_domain='urban',
        ),
        required=True,
    ),
    DateTimeField(
        name='decreeDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            starting_year=1950,
            future_years=False,
            label='Decreedate',
            label_msgid='urban_label_decreeDate',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='decreeType',
        widget=SelectionWidget(
            label='Decreetype',
            label_msgid='urban_label_decreeType',
            i18n_domain='urban',
        ),
        vocabulary='listDecreeTypes',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PcaTerm_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PcaTerm(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IPcaTerm)

    meta_type = 'PcaTerm'
    _at_rename_after_creation = True

    schema = PcaTerm_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('listDecreeTypes')
    def listDecreeTypes(self):
        """
          Return a list of decree types
        """
        service = getGlobalTranslationService()
        _ = service.translate
        lst=[
             ['royal', _("urban", 'decree_type_royal', context=self, default="Royal")],
             ['departmental', _("urban", 'decree_type_departmental', context=self, default="Departmental")],
              ]
        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    # Manually created methods

    security.declarePublic('Title')
    def Title(self):
        """
           Override the Title method to display several data
        """
        title = "%s (%s - %s - %s)" % (unicode(str(self.getLabel()), 'utf8'), unicode(str(self.getNumber()), 'utf-8'), self.toLocalizedTime(self.getDecreeDate()), self.displayValue(self.listDecreeTypes(), self.getDecreeType()))
        return title



registerType(PcaTerm, PROJECTNAME)
# end of class PcaTerm

##code-section module-footer #fill in your manual code here
##/code-section module-footer

