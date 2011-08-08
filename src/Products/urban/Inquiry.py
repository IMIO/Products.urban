# -*- coding: utf-8 -*-
#
# File: Inquiry.py
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
from zope.i18n import translate
from OFS.ObjectManager import BeforeDeleteException
from Products.CMFPlone import PloneMessageFactory as _
##/code-section module-header

schema = Schema((

    LinesField(
        name='derogation',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Derogation',
            label_msgid='urban_label_derogation',
            i18n_domain='urban',
        ),
        multiValued=1,
        vocabulary='listDerogations',
    ),
    TextField(
        name='derogationDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Derogationdetails',
            label_msgid='urban_label_derogationDetails',
            i18n_domain='urban',
        ),
        default_output_type='text/plain',
        default_content_type='text/plain',
    ),
    LinesField(
        name='investigationArticles',
        widget=MultiSelectionWidget(
            label='Investigationarticles',
            label_msgid='urban_label_investigationArticles',
            i18n_domain='urban',
        ),
        multiValued=True,
        vocabulary='listInvestigationArticles',
    ),
    DateTimeField(
        name='investigationStart',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            label='Investigationstart',
            label_msgid='urban_label_investigationStart',
            i18n_domain='urban',
        ),
    ),
    DateTimeField(
        name='investigationEnd',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            label='Investigationend',
            label_msgid='urban_label_investigationEnd',
            i18n_domain='urban',
        ),
    ),
    TextField(
        name='investigationDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Investigationdetails',
            label_msgid='urban_label_investigationDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_output_type='text/html',
    ),
    TextField(
        name='investigationReasons',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Investigationreasons',
            label_msgid='urban_label_investigationReasons',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_output_type='text/html',
    ),
    LinesField(
        name='solicitOpinionsTo',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Solicitopinionsto',
            label_msgid='urban_label_solicitOpinionsTo',
            i18n_domain='urban',
        ),
        multiValued=1,
        vocabulary='listMakers',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Inquiry_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Inquiry_schema['title'].widget.visible = False
##/code-section after-schema

class Inquiry(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IInquiry)

    meta_type = 'Inquiry'
    _at_rename_after_creation = True

    schema = Inquiry_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePrivate('manage_beforeDelete')
    def manage_beforeDelete(self, item, container):
        """
          We can not remove an Inquiry if a linked UrbanEventInquiry exists
        """
        linkedUrbanEventInquiry = self.getLinkedUrbanEventInquiry()
        if linkedUrbanEventInquiry:
            raise BeforeDeleteException, 'cannot_remove_inquiry_linkedurbaneventinquiry'
        BaseContent.manage_beforeDelete(self, item, container)

    security.declarePublic('getLinkedUrbanEventInquiry')
    def getLinkedUrbanEventInquiry(self):
        """
          Return the linked UrbanEventInquiry object if exists
        """
        brefs = self.getBRefs('linkedInquiry')
        if brefs:
            return brefs[0]
        else:
            return None

    def _getSelfPosition(self):
        """
          Return the position of the self between every Inquiry objects
        """
        #get the existing Inquiries
        #getInquiries is a method of GenericLicence
        #so by acquisition, we get it on the parent or we get it on self
        #as GenericLicence heritates from Inquiry
        inquiries = self.getInquiries()
        selfUID = self.UID()
        i = 0
        for inquiry in inquiries:
            if inquiry.UID() == selfUID:
                break
            i = i + 1
        return i

    security.declarePublic('generateInquiryTitle')
    def generateInquiryTitle(self):
        """
          Generates a title for the inquiry
        """
        #we need to generate the title as the number of the inquiry is into it
        position = self._getSelfPosition()
        return translate('inquiry_title_and_number', 'urban', mapping={'number': position+1}, context=self.REQUEST)



registerType(Inquiry, PROJECTNAME)
# end of class Inquiry

##code-section module-footer #fill in your manual code here
##/code-section module-footer

