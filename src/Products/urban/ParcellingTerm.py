# -*- coding: utf-8 -*-
#
# File: ParcellingTerm.py
#
# Copyright (c) 2013 by CommunesPlone
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
        required=True,
    ),
    StringField(
        name='subdividerName',
        widget=StringField._properties['widget'](
            label='Subdividername',
            label_msgid='urban_label_subdividerName',
            i18n_domain='urban',
        ),
        required=True,
    ),
    DateTimeField(
        name='authorizationDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            starting_year=1940,
            future_years=False,
            format="%d/%m/%Y",
            label='Authorizationdate',
            label_msgid='urban_label_authorizationDate',
            i18n_domain='urban',
        ),
    ),
    DateTimeField(
        name='approvalDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            starting_year=1940,
            future_years=False,
            format="%d/%m/%Y",
            label='Approvaldate',
            label_msgid='urban_label_approvalDate',
            i18n_domain='urban',
        ),
    ),
    IntegerField(
        name='numberOfParcels',
        widget=IntegerField._properties['widget'](
            label='Numberofparcels',
            label_msgid='urban_label_numberOfParcels',
            i18n_domain='urban',
        ),
        required=True,
        validators=('isInt',),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ParcellingTerm_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class ParcellingTerm(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IParcellingTerm)

    meta_type = 'ParcellingTerm'
    _at_rename_after_creation = True

    schema = ParcellingTerm_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()

    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title to set a clearly identify the buildlicence
        """
        parcel_baserefs = list(set(['"%s %s %s"' % (prc.getDivision(), prc.getSection(), prc.getRadical()) for prc in self.getParcels()]))
        if parcel_baserefs:
            refs = parcel_baserefs[0]
            for ref in parcel_baserefs[1:]:
                refs = '%s, %s' % (refs, ref)
        title = "%s (%s - %s - %s" % (self.getLabel(), self.getSubdividerName(), self.toLocalizedTime(self.getAuthorizationDate()).encode('utf8'), self.toLocalizedTime(self.getApprovalDate()).encode('utf8'))
        if refs:
            title = '%s - %s' % (title, refs)
        title = '%s)' % title
        self.setTitle(str(title))
        self.reindexObject()

    security.declarePublic('getParcels')
    def getParcels(self):
        """
           Return the list of parcels (portionOut) for the Licence
        """
        return self.objectValues('PortionOut')



registerType(ParcellingTerm, PROJECTNAME)
# end of class ParcellingTerm

##code-section module-footer #fill in your manual code here
##/code-section module-footer

