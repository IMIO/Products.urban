# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 by CommunesPlone
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = "plaintext"

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban import UrbanMessage as _
from Products.urban.UrbanEvent import UrbanEvent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.urban.config import PROJECTNAME


schema = Schema(
    (
        ReferenceField(
            name="linkedReport",
            widget=ReferenceBrowserWidget(
                visible={"edit": "invisible", "view": "invisible"},
                label=_("urban_label_linkedReport", default="Linkedreport"),
            ),
            allowed_types=("UrbanEventInspectionReport",),
            multiValued=0,
            relationship="linkedReport",
        ),
    ),
)


UrbanEventFollowUp_schema = (
    BaseSchema.copy() + getattr(UrbanEvent, "schema", Schema(())).copy() + schema.copy()
)


class UrbanEventFollowUp(UrbanEvent, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IUrbanEventFollowUp)

    meta_type = "UrbanEventFollowUp"
    _at_rename_after_creation = False

    schema = UrbanEventFollowUp_schema

    security.declarePublic("getFollowUpId")

    def getFollowUpId(self):
        """
        Returns the id of the term that is linked to the linked UrbanEventType
        """
        event_type = self.getUrbaneventtypes()
        if event_type:
            return event_type.getId()
        return ""


registerType(UrbanEventFollowUp, PROJECTNAME)
