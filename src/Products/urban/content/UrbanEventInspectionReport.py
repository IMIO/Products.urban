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
__docformat__ = "plaintext"

from AccessControl import ClassSecurityInfo
from Products.urban.widget.select2widget import MultiSelect2Widget
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.UrbanEvent import UrbanEvent
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _
from Products.urban.utils import WIDGET_DATE_END_YEAR

from Products.MasterSelectWidget.MasterMultiSelectWidget import MasterMultiSelectWidget
from zope.i18n import translate

slave_fields_followup_proposition = (
    {
        "name": "other_followup_proposition",
        "action": "show",
        "toggle_method": "showOtherFollowUp",
    },
)

schema = Schema(
    (
        DateTimeField(
            name="reportDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_reportDate", default="Reportdate"),
            ),
        ),
        TextField(
            name="report",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_report", default="Report"),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        TextField(
            name="proofs",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_proofs", default="Proofs"),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="offense_articles",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_offense_articles", default="Offense_articles"),
            ),
            multiValued=True,
            vocabulary=UrbanVocabulary("offense_articles"),
            default_method="getDefaultValue",
        ),
        TextField(
            name="offense_articles_details",
            widget=RichWidget(
                label=_(
                    "urban_label_offense_articles_details",
                    default="Offense_articles_details",
                ),
            ),
            allowable_content_types=("text/html",),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        LinesField(
            name="followup_proposition",
            widget=MasterMultiSelectWidget(
                format="checkbox",
                slave_fields=slave_fields_followup_proposition,
                label=_(
                    "urban_label_followup_proposition", default="Followup_proposition"
                ),
            ),
            multiValued=1,
            vocabulary="listFollowupPropositions",
        ),
        TextField(
            name="other_followup_proposition",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_other_followup_proposition",
                    default="other_followup_proposition",
                ),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
        ),
        StringField(
            name="delay",
            widget=StringField._properties["widget"](
                size=15,
                label=_("urban_label_delay", default="Delay"),
            ),
            default="0",
            validators=("isInteger",),
            optional=True,
        ),
    ),
)


UrbanEventInspectionReport_schema = (
    BaseFolderSchema.copy()
    + getattr(UrbanEvent, "schema", Schema(())).copy()
    + schema.copy()
)


class UrbanEventInspectionReport(BaseFolder, UrbanEvent, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IUrbanEventInspectionReport)

    meta_type = "UrbanEventInspectionReport"
    _at_rename_after_creation = False

    schema = UrbanEventInspectionReport_schema

    security.declarePublic("listFollowupPropositions")

    def listFollowupPropositions(self):
        """
        This vocabulary for field floodingLevel returns a list of
        flooding levels : no risk, low risk, moderated risk, high risk
        """
        voc = UrbanVocabulary(
            "eventconfigs", vocType="FollowUpEventConfig", value_to_use="title"
        )
        config_voc = voc.getDisplayList(self)
        full_voc = [
            ("close", translate(_("close_inspection"), context=self.REQUEST)),
            ("ticket", translate(_("ticket"), context=self.REQUEST)),
            ("stop_worksite", translate(_("stop_worksite"), context=self.REQUEST)),
        ]
        for key in config_voc.keys():
            full_voc.append((key, config_voc.getValue(key)))
        return DisplayList(full_voc)

    def get_regular_followup_propositions(self):
        """ """
        ignore = ["ticket", "close"]
        follow_ups = [
            fw_up for fw_up in self.getFollowup_proposition() if fw_up not in ignore
        ]
        return follow_ups

    def showOtherFollowUp(self, *values):
        selection = [v["val"] for v in values if v["selected"]]
        show = "other" in selection
        return show


registerType(UrbanEventInspectionReport, PROJECTNAME)
