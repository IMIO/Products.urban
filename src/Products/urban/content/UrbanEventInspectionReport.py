# -*- coding: utf-8 -*-
#
# File: UrbanEventInspectionReport.py
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
from Products.urban import interfaces
from Products.urban.UrbanEvent import UrbanEvent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _
from Products.urban.config import EMPTY_VOCAB_VALUE

##code-section module-header #fill in your manual code here
from Products.MasterSelectWidget.MasterMultiSelectWidget import MasterMultiSelectWidget
from zope.i18n import translate

slave_fields_followup_proposition = (
    {
        'name': 'other_followup_proposition',
        'action': 'show',
        'toggle_method': 'showOtherFollowUp',
    },
)
##/code-section module-header

schema = Schema((
    DateTimeField(
        name='reportDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            label=_('urban_label_reportDate',
                    default='Reportdate'),
        ),
    ),
    TextField(
        name='report',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_report', default='Report'),
        ),
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/html',
    ),
    LinesField(
        name='followup_proposition',
        widget=MasterMultiSelectWidget(
            format='checkbox',
            slave_fields=slave_fields_followup_proposition,
            label=_('urban_label_followup_proposition', default='Followup_proposition'),
        ),
        multiValued=1,
        vocabulary='listFollowupPropositions',
    ),
    TextField(
        name='other_followup_proposition',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_other_followup_proposition', default='other_followup_proposition'),
        ),
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/html',
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanEventInspectionReport_schema = BaseFolderSchema.copy() + \
    getattr(UrbanEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class UrbanEventInspectionReport(BaseFolder, UrbanEvent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanEventInspectionReport)

    meta_type = 'UrbanEventInspectionReport'
    _at_rename_after_creation = True

    schema = UrbanEventInspectionReport_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Manually created methods

    security.declarePublic('listFloodingLevels')

    def listFollowupPropositions(self):
        """
          This vocabulary for field floodingLevel returns a list of
          flooding levels : no risk, low risk, moderated risk, high risk
        """
        vocab = (
            #we add an empty vocab value of type "choose a value"
            ('close', translate(_('close_inspection'), context=self.REQUEST)),
            ('notice', translate(_('formal_notice'), context=self.REQUEST)),
            ('notice_reminder', translate(_('formal_notice_reminder'), context=self.REQUEST)),
            ('last_notice_reminder', translate(_('formal_last_notice_reminder'), context=self.REQUEST)),
            ('minutes', translate(_('minutes'), context=self.REQUEST)),
            ('answer', translate(_('answer_to_plaintif'), context=self.REQUEST)),
            ('additional_information', translate(_('additional_information'), context=self.REQUEST)),
            ('FD_mail', translate(_('FD_information_mail'), context=self.REQUEST)),
            ('repair_mail', translate(_('repair_mail'), context=self.REQUEST)),
            ('other', translate(_('other'), context=self.REQUEST)),
        )
        return DisplayList(vocab)

    def showOtherFollowUp(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        show = 'other' in selection
        return show


registerType(UrbanEventInspectionReport, PROJECTNAME)
# end of class UrbanEventInspectionReport
