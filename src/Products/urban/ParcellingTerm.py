# -*- coding: utf-8 -*-

# [DX] TO DELETE > 2.5 [DX]

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.utils import WIDGET_DATE_END_YEAR
from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema(
    (
        StringField(
            name="title",
            widget=StringField._properties["widget"](
                visible=False,
                label="Title",
                label_msgid="urban_label_title",
                i18n_domain="urban",
            ),
            accessor="Title",
        ),
        StringField(
            name="label",
            widget=StringField._properties["widget"](
                label="Label",
                label_msgid="urban_label_label",
                i18n_domain="urban",
            ),
            required=True,
        ),
        StringField(
            name="subdividerName",
            widget=StringField._properties["widget"](
                label="Subdividername",
                label_msgid="urban_label_subdividerName",
                i18n_domain="urban",
            ),
            required=True,
        ),
        DateTimeField(
            name="authorizationDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                starting_year=1940,
                ending_year=WIDGET_DATE_END_YEAR,
                future_years=False,
                format="%d/%m/%Y",
                label="Authorizationdate",
                label_msgid="urban_label_authorizationDate",
                i18n_domain="urban",
            ),
        ),
        DateTimeField(
            name="approvalDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                starting_year=1940,
                ending_year=WIDGET_DATE_END_YEAR,
                future_years=False,
                format="%d/%m/%Y",
                label="Approvaldate",
                label_msgid="urban_label_approvalDate",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="communalReference",
            widget=StringField._properties["widget"](
                label="Communalreference",
                label_msgid="urban_label_CommunalReference",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="DGO4Reference",
            widget=StringField._properties["widget"](
                label="Dgo4reference",
                label_msgid="urban_label_DGO4Reference",
                i18n_domain="urban",
            ),
        ),
        IntegerField(
            name="numberOfParcels",
            widget=IntegerField._properties["widget"](
                label="Numberofparcels",
                label_msgid="urban_label_numberOfParcels",
                i18n_domain="urban",
            ),
            required=True,
            validators=("isInt",),
        ),
        TextField(
            name="changesDescription",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label="Changesdescription",
                label_msgid="urban_label_changesDescription",
                i18n_domain="urban",
            ),
            default_output_type="text/x-html-safe",
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ParcellingTerm_schema = BaseFolderSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class ParcellingTerm(BaseFolder, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IParcellingTerm)

    meta_type = "ParcellingTerm"
    _at_rename_after_creation = True

    schema = ParcellingTerm_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("updateTitle")

    def updateTitle(self):
        """
        Update the title to set a clearly identify the buildlicence
        """
        parcel_baserefs = list(
            set(
                [
                    u'"%s %s %s"'
                    % (prc.getDivision(), prc.getSection(), prc.getRadical())
                    for prc in self.getParcels()
                ]
            )
        )
        refs = u""
        if parcel_baserefs:
            refs = parcel_baserefs[0]
            for ref in parcel_baserefs[1:]:
                refs = u"%s, %s" % (refs, ref)
        title = u"%s (%s" % (
            self.getLabel().decode("utf-8"),
            self.getSubdividerName().decode("utf-8"),
        )

        auth_date = self.getAuthorizationDate()
        if auth_date:
            title = u"%s - %s" % (title, auth_date.strftime("%d/%m/%Y"))

        approval_date = self.getApprovalDate()
        if approval_date:
            title = u"%s - %s" % (title, approval_date.strftime("%d/%m/%Y"))

        if refs:
            title = u"%s - %s" % (title, refs)

        title = u"%s)" % title
        self.setTitle(title.encode("utf-8"))
        self.reindexObject()

    security.declarePublic("getParcels")

    def getParcels(self):
        """
        Return the list of parcels for the Licence
        """
        return [obj for obj in self.objectValues() if obj.portal_type == "Parcel"]


registerType(ParcellingTerm, PROJECTNAME)
# end of class ParcellingTerm

##code-section module-footer #fill in your manual code here
##/code-section module-footer
