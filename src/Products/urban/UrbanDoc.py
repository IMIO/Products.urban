# -*- coding: utf-8 -*-
#
# File: UrbanDoc.py
#
# Copyright (c) 2013 by CommunesPlone
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

from plone.app.blob.content import ATBlob
from plone.app.blob.content import ATBlobSchema
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName
from Products.PageTemplates.Expressions import getEngine
import logging

logger = logging.getLogger('urban: UrbanDoc')
##/code-section module-header

schema = Schema((

    StringField(
        name='TALCondition',
        widget=StringField._properties['widget'](
            size=100,
            description=""""Enter a TAL condition that defines if the event type is applicable or not.  The parameters 'here', 'event', and 'licence'' are available""",
            description_msgid="tal_condition_urbandoc_descr",
            label='Talcondition',
            label_msgid='urban_label_TALCondition',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanDoc_schema = ATBlobSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanDoc(ATBlob):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanDoc)

    meta_type = 'UrbanDoc'
    _at_rename_after_creation = True

    schema = UrbanDoc_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def mayGenerateUrbanDoc(self, obj):
        """
        Creation condition

        computed by evaluating the TAL expression stored in TALCondition field
        """
        res = True # At least for now
        # Check condition
        TALCondition = self.getTALCondition().strip()
        if TALCondition:
            portal = getToolByName(self, 'portal_url').getPortalObject()
            licence = obj.aq_parent
            data = {
                'nothing':      None,
                'portal':       portal,
                'object':       licence,
                'event':        obj,
                'request':      getattr(portal, 'REQUEST', None),
                'here':         obj,
                'licence':      licence,
            }
            ctx = getEngine().getContext(data)
            try:
                res = Expression(TALCondition)(ctx)
            except Exception, e:
                logger.warn("The condition '%s' defined for element at '%s' is wrong!  Message is : %s" % (TALCondition, obj.absolute_url(), e))
                res = False
        return res



registerType(UrbanDoc, PROJECTNAME)
# end of class UrbanDoc

##code-section module-footer #fill in your manual code here
##/code-section module-footer

