# -*- coding: utf-8 -*-
#
# File: UrbanEventType.py
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
from Products.urban.config.UrbanDelay import UrbanDelay
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *

##code-section module-header #fill in your manual code here
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
    LinesField(
        name='activatedFields',
        widget=InAndOutWidget(
            label='Activatedfields',
            label_msgid='urban_label_activatedFields',
            i18n_domain='urban',
        ),
        multiValued=1,
        vocabulary='listOptionalFields',
    ),
    DataGridField(
        name='textDefaultValues',
        widget=DataGridWidget(
            columns={'fieldname' : SelectColumn('FieldName', 'listTextFields'), 'text' : TextAreaColumn('Text', rows=6, cols=60)},
            label='Textdefaultvalues',
            label_msgid='urban_label_textDefaultValues',
            i18n_domain='urban',
        ),
        allow_oddeven=True,
        columns=('fieldname', 'text'),
        validators=('isTextFieldConfigured',),
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
    BooleanField(
        name='isKeyEvent',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_keyevent,
            label='Iskeyevent',
            label_msgid='urban_label_isKeyEvent',
            i18n_domain='urban',
        ),
    ),
    LinesField(
        name='keyDates',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Keydates',
            label_msgid='urban_label_keyDates',
            i18n_domain='urban',
        ),
        multiValued=True,
        vocabulary='listActivatedDates',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanEventType_schema = OrderedBaseFolderSchema.copy() + \
    getattr(UrbanDelay, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanEventType(OrderedBaseFolder, UrbanDelay, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanEventType)

    meta_type = 'UrbanEventType'
    _at_rename_after_creation = True

    schema = UrbanEventType_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('listOptionalFields')
    def listOptionalFields(self):
        """
        """
        pass

registerType(UrbanEventType, PROJECTNAME)
# end of class UrbanEventType

##code-section module-footer #fill in your manual code here
##/code-section module-footer

