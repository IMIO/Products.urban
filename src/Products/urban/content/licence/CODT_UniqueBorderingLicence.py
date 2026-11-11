# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from Products.DataGridField.Column import Column
from Products.urban import interfaces
from Products.urban import UrbanMessage as _
from Products.urban.config import *
from Products.urban.content.licence.CODT_UniqueLicence import CODT_UniqueLicence
from Products.urban.utils import setOptionalAttributes
from zope.interface import implements

from zope.i18n import translate

optional_fields = []

schema = Schema(
    (
        DataGridField(
            name="workLocations",
            schemata="urban_description",
            widget=DataGridWidget(
                columns={"number": Column("Number"), "street": Column("Street")},
                label=_("urban_label_workLocations", default="Work locations"),
            ),
            allow_oddeven=True,
            columns=("number", "street"),
        ),
        StringField(
            name="zipcode",
            schemata="urban_description",
            widget=StringField._properties["widget"](
                label=_("urban_label_zipcode", default="Zipcode"),
            ),
        ),
        StringField(
            name="city",
            schemata="urban_description",
            widget=StringField._properties["widget"](
                label=_("urban_label_city", default="City"),
            ),
        ),
        DataGridField(
            name="manualParcels",
            schemata="urban_description",
            widget=DataGridWidget(
                columns={
                    "ref": Column("Référence cadastrale"),
                    "capakey": Column("Capakey"),
                },
                label=_("urban_label_manualParcels", default="Manualparcels"),
            ),
            allow_oddeven=True,
            columns=("ref", "capakey"),
        ),
    ),
)

setOptionalAttributes(schema, optional_fields)

CODT_UniqueBorderingLicence_schema = (
    BaseFolderSchema.copy()
    + getattr(CODT_UniqueLicence, "schema", Schema(())).copy()
    + schema.copy()
)


class CODT_UniqueBorderingLicence(BaseFolder, CODT_UniqueLicence, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ICODT_UniqueBorderingLicence)

    meta_type = "CODT_UniqueBorderingLicence"
    _at_rename_after_creation = True

    schema = CODT_UniqueBorderingLicence_schema

    security.declarePublic("getDefaultWorkLocationSignaletic")

    def getDefaultWorkLocationSignaletic(self, auto_back_to_the_line=False):
        """
        Returns a string reprensenting the different worklocations
        """
        signaletic = ""

        for wl in self.getWorkLocations():
            streetName = wl["street"]
            number = wl["number"]
            city = self.getCity()
            zipcode = self.getZipcode()
            if signaletic:
                signaletic += " %s " % translate(
                    "and", "urban", context=self.REQUEST
                ).encode("utf8")
            if number:
                signaletic += "%s %s à %s %s" % (
                    streetName,
                    number.encode("utf8"),
                    zipcode,
                    city,
                )
            else:
                signaletic += "%s - %s %s" % (streetName, zipcode, city)
            if auto_back_to_the_line:
                signaletic += "\n"

        return signaletic

    security.declarePublic("getDefaultStreetAndNumber")

    def getDefaultStreetAndNumber(self, separator=""):
        """
        Returns a string reprensenting the different streets and numbers
        """
        signaletic = ""

        for wl in self.getWorkLocations():
            street = wl["street"]
            number = wl["number"]
            if number:
                signaletic = "{} {}{} {}".format(signaletic, street, separator, number)
            else:
                signaletic = "{} {}".format(signaletic, street)

        return signaletic


registerType(CODT_UniqueBorderingLicence, PROJECTNAME)


def finalizeSchema(schema):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("city", after="workLocations")
    schema.moveField("zipcode", after="city")
    schema.moveField("manualParcels", after="zipcode")
    schema.moveField("foldermanagers", after="manualParcels")
    schema.moveField("description", after="additionalLegalConditions")
    schema.moveField("missingPartsDetails", after="missingParts")
    return schema


finalizeSchema(CODT_UniqueBorderingLicence_schema)
