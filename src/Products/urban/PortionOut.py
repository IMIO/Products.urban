# -*- coding: utf-8 -*-
# [DX] TO DELETE > 2.5 [DX]

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = "plaintext"

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import DisplayList
from Products.urban.interfaces import IGenericLicence
from Products.urban import services

##/code-section module-header

schema = Schema(
    (
        StringField(
            name="divisionCode",
            widget=StringField._properties["widget"](
                visible={"edit": "hidden", "view": "visible"},
                label="Divisioncode",
                label_msgid="urban_label_divisionCode",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="division",
            widget=SelectionWidget(
                format="select",
                label="Division",
                label_msgid="urban_label_division",
                i18n_domain="urban",
            ),
            enforceVocabulary=True,
            vocabulary="listDivisionNames",
        ),
        StringField(
            name="section",
            widget=StringField._properties["widget"](
                label="Section",
                label_msgid="urban_label_section",
                i18n_domain="urban",
            ),
            required=True,
            validators=("isValidSection",),
        ),
        StringField(
            name="radical",
            widget=StringField._properties["widget"](
                label="Radical",
                label_msgid="urban_label_radical",
                i18n_domain="urban",
            ),
            validators=("isValidRadical",),
        ),
        StringField(
            name="bis",
            widget=StringField._properties["widget"](
                label="Bis",
                label_msgid="urban_label_bis",
                i18n_domain="urban",
            ),
            validators=("isValidBis",),
        ),
        StringField(
            name="exposant",
            widget=StringField._properties["widget"](
                label="Exposant",
                label_msgid="urban_label_exposant",
                i18n_domain="urban",
            ),
            validators=("isValidExposant",),
        ),
        StringField(
            name="puissance",
            widget=StringField._properties["widget"](
                label="Puissance",
                label_msgid="urban_label_puissance",
                i18n_domain="urban",
            ),
            validators=("isValidPuissance",),
        ),
        BooleanField(
            name="partie",
            default=False,
            widget=BooleanField._properties["widget"](
                label="Partie",
                label_msgid="urban_label_partie",
                i18n_domain="urban",
            ),
        ),
        BooleanField(
            name="isOfficialParcel",
            default=True,
            widget=BooleanField._properties["widget"](
                visible={"edit": "hidden", "view": "visible"},
                label="Isofficialparcel",
                label_msgid="urban_label_isOfficialParcel",
                i18n_domain="urban",
            ),
        ),
        BooleanField(
            name="outdated",
            default=False,
            widget=BooleanField._properties["widget"](
                visible={"edit": "hidden", "view": "visible"},
                label="Outdated",
                label_msgid="urban_label_outdated",
                i18n_domain="urban",
            ),
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PortionOut_schema = BaseSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
PortionOut_schema["title"].widget.visible = False
##/code-section after-schema


class PortionOut(BaseContent, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IPortionOut)

    meta_type = "PortionOut"
    _at_rename_after_creation = True

    schema = PortionOut_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def updateTitle(self):
        """
        Set a correct title if we use invokeFactory
        """
        division = self.getDivisionName() or ""
        division = division.encode("utf-8")
        section = self.getSection()
        radical = self.getRadical()
        bis = self.getBis()
        exposant = self.getExposant()
        puissance = self.getPuissance()
        generatedTitle = (
            str(division)
            + " "
            + str(section)
            + " "
            + str(radical)
            + " "
            + str(bis)
            + " "
            + str(exposant)
            + " "
            + str(puissance)
        )
        generatedTitle = generatedTitle.strip()
        if self.getPartie():
            generatedTitle = generatedTitle + " (partie)"
        self.setTitle(generatedTitle)
        self.reindexObject()

    security.declarePublic("at_post_create_script")

    def at_post_create_script(self):
        """
        Post create hook...
        XXX This should be replaced by a zope event...
        """
        self.updateTitle()
        # after creation, reindex the parent so the parcelInfosIndex is OK
        self.aq_inner.aq_parent.reindexObject()

    security.declarePublic("at_post_edit_script")

    def at_post_edit_script(self):
        """
        Post edit hook...
        XXX This should be replaced by a zope event...
        """
        self.updateTitle()
        # after creation, reindex the parent so the parcelInfosIndex is OK
        self.aq_inner.aq_parent.reindexObject()

    security.declarePublic("reference_as_dict")

    def reference_as_dict(self, with_empty_values=False):
        """
        Return this parcel reference defined values as a dict.
        By default only return parts of the reference with defined values.
        If with_empty_values is set to True, also return empty values.
        """
        references = {
            "division": self.getDivisionCode(),
            "section": self.getSection(),
            "radical": self.getRadical(),
            "bis": self.getBis(),
            "exposant": self.getExposant(),
            "puissance": self.getPuissance(),
        }
        if not with_empty_values:
            references = dict([(k, v) for k, v in references.iteritems() if v])

        return references

    security.declarePublic("getDivisionName")

    def getDivisionName(self):
        return self.listDivisionNames().getValue(self.getDivision())

    security.declarePublic("getDivisionAlternativeName")

    def getDivisionAlternativeName(self):
        return self.listDivisionAlternativeNames().getValue(self.getDivision())

    security.declarePublic("listDivisionAlternativeNames")

    def listDivisionAlternativeNames(self):
        return self._listDivisionNames(name="alternative_name")

    security.declarePublic("listDivisionNames")

    def listDivisionNames(self):
        return self._listDivisionNames(name="name")

    def _listDivisionNames(self, name="name"):
        urban_tool = getToolByName(self, "portal_urban")
        divisions = urban_tool.getDivisionsRenaming()
        return DisplayList(
            [
                (str(div["division"]), unicode(div[name].decode("utf-8")))
                for div in divisions
            ]
        )

    security.declarePublic("getRelatedLicences")

    def getRelatedLicences(self, licence_type=""):
        catalog = getToolByName(self, "portal_catalog")
        licence = self.aq_parent
        capakey = self.get_capakey()
        brains = []
        if licence_type:
            brains = catalog(portal_type=licence_type, parcelInfosIndex=capakey)
        else:
            brains = catalog(parcelInfosIndex=capakey)
        return [brain for brain in brains if brain.id != licence.id]

    security.declarePublic("getCSSClass")

    def getCSSClass(self):
        if self.getOutdated():
            return "outdated_parcel"
        elif not self.getIsOfficialParcel():
            return "manual_parcel"
        return ""

    def get_capakey(self):
        capakey = "%s%s%04d/%02d%s%03d" % (
            self.getDivisionCode(),
            self.getSection(),
            int(self.getRadical() or 0),
            int(self.getBis() or 0),
            self.getExposant() or "_",
            int(self.getPuissance() or 0),
        )
        return capakey

    @property
    def capakey(self):
        return self.get_capakey()

    security.declarePublic("get_historic")

    def get_historic(self):
        """
        Return the "parcel historic" object of this parcel
        """
        session = services.cadastre.new_session()
        historic = session.query_parcel_historic(self.capakey)
        session.close()
        return historic


registerType(PortionOut, PROJECTNAME)
# [DX] TO DELETE > 2.5 [DX]
