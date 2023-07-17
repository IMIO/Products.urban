# -*- coding: utf-8 -*-
#
# File: UrbanEventType.py
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
from Products.urban.widget.select2widget import MultiSelect2Widget
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.urban.UrbanConfigurationValue import UrbanConfigurationValue
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *
from Products.urban.interfaces import IOptionalFields

##code-section module-header #fill in your manual code here
from plone import api
from Products.Archetypes.public import DisplayList
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.PageTemplates.Expressions import getEngine
from Products.urban.docgen.UrbanTemplate import IUrbanTemplate
from collective.datagridcolumns.TextAreaColumn import TextAreaColumn
from zope.i18n import translate

from zope.component import queryAdapter

import logging
logger = logging.getLogger('urban: UrbanEventType')

slave_fields_keyevent = (
    # if in a keyEvent, display a selectbox
    {
        'name': 'keyDates',
        'action': 'show',
        'hide_values': (True,),
    },
)

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
            columns={'fieldname': SelectColumn('FieldName', 'listTextFields'), 'text': TextAreaColumn('Text', rows=6, cols=60)},
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
    LinesField(
        name='eventTypeType',
        vocabulary_factory="eventTypeType",
        widget=MultiSelect2Widget(
            label='Eventtypetype',
            label_msgid='urban_label_eventTypeType',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='eventPortalType',
        vocabulary="listEventPortalTypes",
        default='UrbanEvent',
        widget=SelectionWidget(
            label='Eventportaltype',
            label_msgid='urban_label_eventPortalType',
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
        widget=MultiSelect2Widget(
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
    getattr(UrbanConfigurationValue, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class UrbanEventType(OrderedBaseFolder, UrbanConfigurationValue, BrowserDefaultMixin):
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

    def getEventType(self):
        return self.getEventTypeType()

    security.declarePublic('listOptionalFields')

    def listOptionalFields(self):
        """
         return a DisplayList of fields wich are marked as optional
        """
        from Products.urban.content.UrbanEventInquiry import UrbanEventInquiry_schema
        vocabulary = []
        fields = UrbanEventInquiry_schema.fields()
        additional_fields = queryAdapter(self, IOptionalFields)
        if additional_fields:
            fields += additional_fields.get()

        for field in fields:
            try:
                if field.optional:
                    vocabulary.append(
                        (
                            field.getName(),
                            translate(
                                field.widget.label,
                                'urban', default=field.getName(),
                                context=self.REQUEST
                            )
                        )
                    )
            except AttributeError:
                #most of time, the field has not the 'optional' attribute
                pass
        optional_fields = DisplayList(sorted(vocabulary, key=lambda name: name[1]))
        return optional_fields

    # Manually created methods

    security.declarePublic('listTextFields')

    def listTextFields(self):
        #we have to know from where the method has been called in order to know which text
        #fields to propose to be "default valued"
        from Products.urban.content.UrbanEventInquiry import UrbanEventInquiry_schema
        urbanevent_fields = UrbanEventInquiry_schema.fields()
        additional_fields = queryAdapter(self, IOptionalFields)
        if additional_fields:
            urbanevent_fields += additional_fields.get()

        blacklist = ['rights']
        available_fields = [field for field in urbanevent_fields if field.getType() == 'Products.Archetypes.Field.TextField' and field.getName() not in blacklist]
        vocabulary_fields = [
            (
                field.getName(),
                translate(
                    getattr(field.widget, 'label_msgid', field.widget.label),
                    'urban',
                    context=self.REQUEST,
                ),
            )
            for field in available_fields
        ]
        #return a vocabulary containing the names of all the text fields of the schema
        return DisplayList(sorted(vocabulary_fields, key=lambda name: name[1]))

    security.declarePublic('canBeCreatedInLicence')

    def canBeCreatedInLicence(self, obj):
        """
        Creation condition

        computed by evaluating the TAL expression stored in TALCondition field
        """
        res = True  # At least for now
        # Check condition
        TALCondition = self.getTALCondition().strip()
        if TALCondition:
            portal = getToolByName(self, 'portal_url').getPortalObject()
            data = {
                'nothing': None,
                'portal': portal,
                'object': obj,
                'event': self,
                'request': getattr(portal, 'REQUEST', None),
                'here': obj,
                'licence': obj,
            }
            ctx = getEngine().getContext(data)
            try:
                res = Expression(TALCondition)(ctx)
            except Exception, e:
                logger.warn("The condition '%s' defined for element at '%s' is wrong!  Message is : %s" % (TALCondition, obj.absolute_url(), e))
                res = False
        return res

    def checkCreationInLicence(self, obj):
        if not self.canBeCreatedInLicence(obj):
            raise ValueError(_("You can not create this UrbanEvent !"))

    security.declarePublic('listActivatedDates')

    def listActivatedDates(self):
        from Products.urban.content.UrbanEventInquiry import UrbanEventInquiry_schema

        activated_fields = self.getActivatedFields()
        activated_fields = type(activated_fields) == str and [activated_fields] or activated_fields
        activated_date_fields = []
        for field in UrbanEventInquiry_schema.getSchemataFields('default'):
            is_date_field = field.getType() == 'Products.Archetypes.Field.DateTimeField'
            if is_date_field:
                fieldname = field.getName()
                if getattr(field, 'optional', False) and fieldname in activated_fields:
                    activated_date_fields.append(
                        (
                            fieldname,
                            translate(
                                "urban_label_" + fieldname,
                                'urban',
                                default=fieldname,
                                context=self.REQUEST
                            )
                        )
                    )
        to_return = DisplayList(
            [('eventDate', self.getEventDateLabel().decode('utf-8'))] + activated_date_fields
        )
        return to_return

    security.declarePublic('getTemplates')

    def getTemplates(self):
        templates = [obj for obj in self.objectValues() if IUrbanTemplate.providedBy(obj)]
        return templates

    security.declarePublic('listEventPortalTypes')

    def listEventPortalTypes(self):
        portal_types = api.portal.get_tool('portal_types')
        event_types = DisplayList(
            [(k, _(k)) for k in portal_types.keys() if k.startswith('UrbanEvent') and not k.endswith('EventType')]
        )
        return event_types

    def getLinkedUrbanEvents(self):
        """
        Return all the urban events linked to this urban event type.
        """
        ref_catalog = api.portal.get_tool('reference_catalog')
        ref_brains = ref_catalog(targetUID=self.UID())
        urban_events = [ref_brain.getObject().getSourceObject() for ref_brain in ref_brains]
        return urban_events


registerType(UrbanEventType, PROJECTNAME)
# end of class UrbanEventType

##code-section module-footer #fill in your manual code here
##/code-section module-footer
