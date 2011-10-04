# -*- coding: utf-8 -*-
#
# File: UrbanEventType.py
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
from Products.urban.UrbanDelay import UrbanDelay
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
import logging
logger = logging.getLogger('urban: UrbanEventType')
from Products.CMFPlone.i18nl10n import utranslate
from Products.CMFCore.Expression import Expression, createExprContext
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

    StringField(
        name='TALCondition',
        widget=StringField._properties['widget'](
            size=100,
            description=""""Enter a TAL condition that defines if the event type is applicable or not.  The parameters 'here' and 'member' are available""",
            description_msgid="tal_condition_descr",
            label='Talcondition',
            label_msgid='urban_label_TALCondition',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='eventDateLabel',
        default='Date',
        widget=StringField._properties['widget'](
            label='Eventdatelabel',
            label_msgid='urban_label_eventDateLabel',
            i18n_domain='urban',
        ),
        required=True,
    ),
    StringField(
        name='activatedFields',
        widget=InAndOutWidget(
            label='Activatedfields',
            label_msgid='urban_label_activatedFields',
            i18n_domain='urban',
        ),
        vocabulary='listOptionalFields',
    ),
    BooleanField(
        name='showTitle',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Showtitle',
            label_msgid='urban_label_showTitle',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='eventTypeType',
        vocabulary_factory="eventTypeType",
        widget=SelectionWidget(
            label='Eventtypetype',
            label_msgid='urban_label_eventTypeType',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='specialFunctionName',
        widget=StringField._properties['widget'](
            label='Specialfunctionname',
            label_msgid='urban_label_specialFunctionName',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='specialFunctionUrl',
        widget=StringField._properties['widget'](
            label='Specialfunctionurl',
            label_msgid='urban_label_specialFunctionUrl',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanEventType_schema = BaseFolderSchema.copy() + \
    getattr(UrbanDelay, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanEventType(BaseFolder, UrbanDelay, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IUrbanEventType)

    meta_type = 'UrbanEventType'
    _at_rename_after_creation = True

    schema = UrbanEventType_schema

    ##code-section class-header #fill in your manual code here
    aliases = {
        '(Default)'  : 'base_view',
        'view'       : '(Default)',
        'edit'       : 'base_edit',
        'index.html' : '(Default)',
        'properties' : 'base_metadata',
        'sharing'    : '',
        }
    ##/code-section class-header

    # Methods

    security.declarePublic('listOptionalFields')
    def listOptionalFields(self):
        """
         return a DisplayList of fields wich are marked as optional
        """
        from Products.urban.UrbanEvent import UrbanEvent_schema
        lst = []
        for field in UrbanEvent_schema.fields():
            try:
                if field.optional == True:
                    lst.append((field.getName(), utranslate(msgid="urban_label_" + field.getName(), domain='urban', default=field.getName(), context=self)))
            except AttributeError:
                #most of time, the field has not the 'optional' attribute
                pass
        return DisplayList(lst)

    # Manually created methods

    security.declarePublic('listEventTypeTypes')
    def listEventTypeTypes(self):
        """
         return a DisplayList of eventtype type
        """
        lst=[]
        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic('isApplicable')
    def isApplicable(self, obj):
        """
          Check if the TAL condition linked to this UrbanEventType is True
        """
        res = True # At least for now
        # Check condition
        TALCondition = self.getTALCondition().strip()
        if TALCondition:
            portal = getToolByName(self, 'portal_url').getPortalObject()
            ctx = createExprContext(obj.getParentNode(), portal, obj)
            try:
                res = Expression(TALCondition)(ctx)
            except Exception, e:
                logger.warn("The condition '%s' defined for element at '%s' is wrong!" % (TALCondition, obj.absolute_url()))
                res = False
        return res



registerType(UrbanEventType, PROJECTNAME)
# end of class UrbanEventType

##code-section module-footer #fill in your manual code here
##/code-section module-footer

