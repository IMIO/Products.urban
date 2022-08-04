# -*- coding: utf-8 -*-
#
# File: Locality.py
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
from Acquisition import aq_inner, aq_parent
from Products.CMFCore import permissions
##/code-section module-header

schema = Schema((

    StringField(
        name='localityName',
        widget=StringField._properties['widget'](
            label='Localityname',
            label_msgid='urban_label_localityName',
            i18n_domain='urban',
        ),
        required=True,
    ),
    TextField(
        name='alsoCalled',
        allowable_content_types=('text/plain',),
        widget=RichWidget(
            description='Enter the different kind of spelling for this locality',
            description_msgid="alsocalled_descr",
            label='Alsocalled',
            label_msgid='urban_label_alsoCalled',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_output_type='text/x-html-safe',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Locality_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
del Locality_schema['title']
##/code-section after-schema

class Locality(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ILocality)

    meta_type = 'Locality'
    _at_rename_after_creation = True

    schema = Locality_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('Title')
    def Title(self):
        """
           Update the title to clearly identify the locality in the city
        """
        #format is "title (cityZipeCode - cityTitle)"
        city = self.getParentNode()
        title = "%s (%s - %s)" % (self.getLocalityName(), city.getZipCode(), city.Title())
        return str(title)

    security.declareProtected(permissions.View, 'SearchableText')
    def SearchableText(self):
        """
          Override to take Title into account
        """
        return self.Title() + self.getRawAlsoCalled()

    security.declareProtected(permissions.View, 'getStreetName')
    def getStreetName(self):
        """
          Returns the street name that is behing the localityName here
        """
        return self.getLocalityName()

    security.declareProtected(permissions.View, 'getStreetCode')
    def getStreetCode(self):
        """
          Returns en empty street code
        """
        return 0

    def getCity(self):
        """
          Returns the city
        """
        return aq_parent(aq_inner(self))



registerType(Locality, PROJECTNAME)
# end of class Locality

##code-section module-footer #fill in your manual code here
##/code-section module-footer

