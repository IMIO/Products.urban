# -*- coding: utf-8 -*-
#
# File: LicenceConfig.py
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
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import (
    ReferenceBrowserWidget,
)
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate
from Products.Archetypes.public import DisplayList
from collective.datagridcolumns.TextAreaColumn import TextAreaColumn
from Products.DataGridField.DataGridField import FixedRow
from Products.DataGridField.FixedColumn import FixedColumn
from Products.DataGridField.CheckboxColumn import CheckboxColumn
from Products.urban.config import VOCABULARY_TYPES
from Products.urban.utils import getLicenceSchema
from Products.urban import UrbanMessage as _
from zope.interface import Interface
from Products.PageTemplates.Expressions import getEngine
from Products.CMFCore.Expression import Expression
from plone import api
from DateTime import DateTime
from zope.interface import implementedBy
from zope.component import getGlobalSiteManager

##/code-section module-header

schema = Schema(
    (
        StringField(
            name="licencePortalType",
            widget=StringField._properties["widget"](
                label="Licenceportaltype",
                label_msgid="urban_label_licencePortalType",
                i18n_domain="urban",
            ),
            mode="r",
        ),
        LinesField(
            name="usedAttributes",
            widget=InAndOutWidget(
                description="Select the optional fields you want to use. Multiple selection or deselection when clicking with CTRL",
                description_msgid="urban_descr_usedAttributes",
                size="30",
                label="Usedattributes",
                label_msgid="urban_label_usedAttributes",
                i18n_domain="urban",
            ),
            schemata="public_settings",
            multiValued=True,
            vocabulary="listUsedAttributes",
        ),
        DataGridField(
            name="tabsConfig",
            widget=DataGridWidget(
                columns={
                    "display": CheckboxColumn("Display"),
                    "value": FixedColumn("Value"),
                    "display_name": Column("Name"),
                },
                label="Tabsconfig",
                label_msgid="urban_label_tabsConfig",
                i18n_domain="urban",
            ),
            fixed_rows="getTabsConfigRows",
            allow_insert=False,
            allow_reorder=True,
            allow_oddeven=True,
            allow_delete=False,
            schemata="public_settings",
            columns=(
                "display",
                "value",
                "display_name",
            ),
        ),
        BooleanField(
            name="useTabbingForDisplay",
            default=True,
            widget=BooleanField._properties["widget"](
                label="Usetabbingfordisplay",
                label_msgid="urban_label_useTabbingForDisplay",
                i18n_domain="urban",
            ),
            schemata="public_settings",
        ),
        BooleanField(
            name="useTabbingForEdit",
            default=True,
            widget=BooleanField._properties["widget"](
                label="Usetabbingforedit",
                label_msgid="urban_label_useTabbingForEdit",
                i18n_domain="urban",
            ),
            schemata="public_settings",
        ),
        DataGridField(
            name="textDefaultValues",
            allow_oddeven=True,
            widget=DataGridWidget(
                columns={
                    "fieldname": SelectColumn("FieldName", "listTextFields"),
                    "text": TextAreaColumn("Text", rows=30, cols=60),
                },
                label="Textdefaultvalues",
                label_msgid="urban_label_textDefaultValues",
                i18n_domain="urban",
            ),
            schemata="public_settings",
            columns=("fieldname", "text"),
            validators=("isTextFieldConfigured",),
        ),
        DataGridField(
            name="warnings",
            allow_oddeven=True,
            widget=DataGridWidget(
                columns={
                    "condition": SelectColumn("Condition", "listWarningConditions"),
                    "message": TextAreaColumn("Message", rows=6, cols=60),
                    "level": SelectColumn("Level", "listWarningLevels"),
                },
                label="Warnings",
                label_msgid="urban_label_warnings",
                i18n_domain="urban",
            ),
            schemata="public_settings",
            columns=("condition", "message", "level"),
            default=[],
        ),
        StringField(
            name="referenceTALExpression",
            default="python: 'XXX/' + date.strftime('%Y') + '/' + numerotation",
            widget=StringField._properties["widget"](
                size=100,
                label="Referencetalexpression",
                label_msgid="urban_label_referenceTALExpression",
                i18n_domain="urban",
            ),
            schemata="public_settings",
        ),
        StringField(
            name="numerotationSource",
            widget=SelectionWidget(
                label="Numerotation source",
                label_msgid="urban_label_numerotationsource",
                i18n_domain="urban",
            ),
            vocabulary="listLicenceConfigs",
            default_method="default_numerotation_source",
            schemata="public_settings",
        ),
        StringField(
            name="numerotation",
            default=0,
            widget=StringField._properties["widget"](
                label="Numerotation",
                label_msgid="urban_label_numerotation",
                i18n_domain="urban",
            ),
            schemata="public_settings",
        ),
        StringField(
            name="reference_regex",
            default=".*/(\d*)/(\d*).*",
            widget=StringField._properties["widget"](
                label="Reference_regex",
                label_msgid="urban_label_reference_regex",
                i18n_domain="urban",
            ),
            schemata="public_settings",
        ),
        ReferenceField(
            name="default_foldermanager",
            widget=ReferenceBrowserWidget(
                allow_browse=False,
                base_query="get_authorized_folder_managers_base_query",
                show_results_without_query=True,
                wild_card_search=True,
                allow_search=False,
                label=_("urban_label_default_foldermanagers", default="Foldermanagers"),
            ),
            relationship="licenceFolderManagers",
            required=False,
            schemata="public_settings",
            multiValued=True,
            allowed_types=("FolderManager",),
        ),
        LinesField(
            name="states_to_end_all_events",
            widget=InAndOutWidget(
                description="Select the licence states who will close all urban events",
                description_msgid="urban_descr_states_to_end_all_events",
                size=10,
                label="States_to_end_all_events",
                label_msgid="urban_label_states_to_end_all_events",
                i18n_domain="urban",
            ),
            schemata="public_settings",
            multiValued=True,
            vocabulary_factory="urban.licence_state",
        ),
        LinesField(
            name="states_to_end_all_tasks",
            widget=InAndOutWidget(
                description="Select the licence states who will close all schedule tasks",
                description_msgid="urban_descr_states_to_end_all_tasks",
                size=10,
                label="States_to_end_all_tasks",
                label_msgid="urban_label_states_to_end_all_tasks",
                i18n_domain="urban",
            ),
            schemata="schedule",
            multiValued=True,
            vocabulary_factory="urban.licence_state",
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

LicenceConfig_schema = BaseFolderSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
LicenceConfig_schema["licencePortalType"].widget.visible = False
for f in LicenceConfig_schema.filterFields(schemata="default"):
    f.widget.visible = {"edit": "invisible"}
for f in LicenceConfig_schema.filterFields(schemata="metadata"):
    f.widget.visible = {"edit": "invisible"}
##/code-section after-schema


class LicenceConfig(BaseFolder, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ILicenceConfig)

    meta_type = "LicenceConfig"
    _at_rename_after_creation = True

    schema = LicenceConfig_schema

    security.declarePublic("getEventConfigs")

    def getEventConfigs(self):
        event_configs = self.eventconfigs.objectValues()
        return event_configs

    def getEnabledEventConfigs(self):
        event_configs = [
            cfg
            for cfg in self.getEventConfigs()
            if api.content.get_state(cfg) == "enabled"
        ]
        return event_configs

    security.declarePublic("getEventTypesByInterface")

    def getEventTypesByInterface(self, interface):
        """
        Return all the UrbanEventTypes having interface 'interface'
        in their eventTypeType field
        """
        if issubclass(interface, Interface):
            interface = interface.__identifier__

        eventtypes = self.eventconfigs.objectValues()
        to_return = [uet for uet in eventtypes if interface in uet.getEventType()]
        return to_return

    security.declarePrivate("listUsedAttributes")

    def listUsedAttributes(self):
        """
        Return the available optional fields
        """
        res = []
        abr = {
            "urban_description": "(recap)",
            "urban_location": "(urb) ",
            "urban_road": "(voi) ",
            "urban_inquiry": "(enq) ",
            "urban_analysis": "(analyse) ",
            "urban_advices": "(avis) ",
            "urban_habitation": "(log) ",
            "urban_environment": "(environnement) ",
            "urban_peb": "(peb) ",
            "urban_patrimony": "(patrimoine) ",
            "urban_inspection": "(inspection) ",
        }
        if not getLicenceSchema(self.getLicencePortalType()):
            return DisplayList()
        for field in getLicenceSchema(self.getLicencePortalType()).fields():
            if hasattr(field, "optional"):
                tab = field.schemata
                if field.schemata in abr.keys() and field.widget.visible:
                    tab = abr[tab]
                    res.append(
                        (
                            field.getName(),
                            "%s%s"
                            % (
                                tab,
                                translate(
                                    getattr(
                                        field.widget, "label_msgid", field.widget.label
                                    ),
                                    domain=getattr(field.widget, "i18n_domain", None),
                                    default=field.widget.label,
                                    context=self.REQUEST,
                                ),
                            ),
                        )
                    )
        return DisplayList(tuple(res)).sortedByValue()

    def listLicenceConfigs(self):
        """ """
        portal_urban = api.portal.get_tool("portal_urban")
        res = [(c.id, c.Title()) for c in portal_urban.get_all_licence_configs()]
        return DisplayList(tuple(res)).sortedByValue()

    security.declarePublic("getNumerotation")

    def getNumerotation(self):
        """ """
        config_id = self.getNumerotationSource()
        if config_id:
            portal_urban = api.portal.get_tool("portal_urban")
            config = getattr(portal_urban, config_id)
            return config.getField("numerotation").get(config)
        else:
            return self.getField("numerotation").get(self)

    def generateReference(self, licence, **kwargs):
        """
        Generates a reference based on the numerotationTALExpression
        """
        # we get a field like UrbanCertificateBaseNumerotation on self
        # to get the last numerotation for this kind of licence
        lastValue = self.getNumerotation()
        if str(lastValue).isdigit():
            lastValue = int(lastValue)
            lastValue = lastValue + 1

        # evaluate the numerotationTALExpression and pass it obj, lastValue and self
        data = {
            "obj": licence,
            "tool": api.portal.get_tool("portal_urban"),
            "numerotation": str(lastValue),
            "portal": api.portal.getSite(),
            "date": DateTime(),
        }
        data.update(kwargs)
        res = ""
        try:
            ctx = getEngine().getContext(data)
            res = Expression(self.getReferenceTALExpression())(ctx)
        except Exception:
            pass
        return res

    security.declarePublic("getActiveTabs")

    def getActiveTabs(self):
        """
        Return the tabs in use
        """
        return [tab for tab in self.getTabsConfig() if tab["display"]]

    security.declarePrivate("getTabsConfigRows")

    def getTabsConfigRows(self):
        """ """
        default_names = {
            "description": "Récapitulatif",
            "advices": "Avis",
            "inquiry": "Publicité",
            "analysis": "Analyse Urbanisme",
            "environment": "Analyse Environnement",
            "location": "Aspects légaux",
            "road": "Voirie",
            "habitation": "Logement",
            "peb": "PEB",
            "patrimony": "Patrimoine",
            "inspection": "Inspection",
        }
        minimum_tabs_config = ["description", "analysis", "location", "road"]
        certificatebase_tabs_config = [
            "description",
            "analysis",
            "location",
            "road",
            "patrimony",
        ]
        inquiry_tabs_config = [
            "description",
            "advices",
            "inquiry",
            "analysis",
            "location",
            "road",
        ]
        codt_inquiry_tabs_config = [
            "description",
            "advices",
            "inquiry",
            "analysis",
            "location",
            "road",
            "patrimony",
        ]
        buildlicence_tabs_config = [
            "description",
            "advices",
            "inquiry",
            "analysis",
            "location",
            "road",
            "habitation",
            "peb",
        ]
        codt_buildlicence_tabs_config = [
            "description",
            "advices",
            "inquiry",
            "analysis",
            "location",
            "road",
            "habitation",
            "peb",
            "patrimony",
        ]
        uniquelicence_tabs_config = [
            "description",
            "advices",
            "inquiry",
            "analysis",
            "environment",
            "location",
            "road",
            "habitation",
            "peb",
        ]
        codt_uniquelicence_tabs_config = [
            "description",
            "advices",
            "inquiry",
            "analysis",
            "environment",
            "location",
            "road",
            "habitation",
            "peb",
            "patrimony",
        ]
        env_advice_tabs_config = [
            "description",
            "advices",
            "analysis",
            "environment",
            "location",
            "road",
        ]
        env_inquiry_tabs_config = [
            "description",
            "advices",
            "inquiry",
            "analysis",
            "environment",
            "location",
            "road",
        ]
        inspection_tabs_config = ["description", "advices", "inspection", "location"]
        ticket_tabs_config = ["description", "inspection", "location"]

        types = {
            "buildlicence": buildlicence_tabs_config,
            "article127": buildlicence_tabs_config,
            "uniquelicence": uniquelicence_tabs_config,
            "integratedlicence": buildlicence_tabs_config,
            "parceloutlicence": inquiry_tabs_config,
            "urbancertificatetwo": buildlicence_tabs_config,
            "codt_buildlicence": codt_buildlicence_tabs_config,
            "codt_article127": codt_buildlicence_tabs_config,
            "codt_parceloutlicence": codt_inquiry_tabs_config,
            "codt_uniquelicence": codt_uniquelicence_tabs_config,
            "codt_commerciallicence": codt_buildlicence_tabs_config,
            "codt_integratedlicence": codt_uniquelicence_tabs_config,
            "codt_urbancertificatetwo": codt_buildlicence_tabs_config,
            "codt_urbancertificateone": certificatebase_tabs_config,
            "codt_notaryletter": certificatebase_tabs_config,
            "envclassthree": env_advice_tabs_config,
            "envclassone": env_inquiry_tabs_config,
            "envclasstwo": env_inquiry_tabs_config,
            "explosivespossession": [
                "description",
                "advices",
                "inquiry",
                "environment",
            ],
            "envclassbordering": env_inquiry_tabs_config,
            "inspection": inspection_tabs_config,
            "ticket": ticket_tabs_config,
            "roaddecree": buildlicence_tabs_config,
            "division": certificatebase_tabs_config,
        }
        licence_type = self.id

        def makeRow(tabname):
            return FixedRow(
                keyColumn="value",
                initialData={
                    "display": "1",
                    "value": tabname,
                    "display_name": default_names[tabname],
                },
            )

        return [
            makeRow(tabname) for tabname in types.get(licence_type, minimum_tabs_config)
        ]

    security.declarePublic("getIconURL")

    def getIconURL(self):
        portal_types = getToolByName(self, "portal_types")
        if self.getLicencePortalType() and hasattr(
            portal_types, self.getLicencePortalType()
        ):
            icon = "%s.png" % self.getLicencePortalType()
        else:
            icon = "LicenceConfig.png"
        portal_url = getToolByName(self, "portal_url")
        return portal_url() + "/" + icon

    security.declarePublic("listTextFields")

    def listTextFields(self):
        # we have to know from where the method has been called in order to know which text
        # fields to propose to be "default valued"
        licence_type = self.getLicencePortalType()
        licence_schema = getLicenceSchema(licence_type)
        abr = {
            "urban_peb": "(peb) ",
            "urban_location": "(urb) ",
            "urban_road": "(voi) ",
            "urban_inquiry": "(enq) ",
            "urban_advices": "(avis) ",
            "urban_analysis": "(analyse) ",
            "urban_environment": "(environnement) ",
            "urban_description": "",
            "urban_patrimony": "(patrimoine) ",
            "urban_inspection": "(inspection) ",
        }
        available_fields = [
            field
            for field in licence_schema.fields()
            if field.getType() == "Products.Archetypes.Field.TextField"
            and field.getName() != "rights"
        ]
        vocabulary_fields = [
            (
                field.getName(),
                "%s %s"
                % (
                    translate(
                        getattr(field.widget, "label_msgid", field.widget.label),
                        "urban",
                        context=self.REQUEST,
                    ),
                    abr[field.schemata],
                ),
            )
            for field in available_fields
        ]
        # return a vocabulary containing the names of all the text fields of the schema
        return DisplayList(sorted(vocabulary_fields, key=lambda name: name[1]))

    security.declarePublic("listWarningConditions")

    def listWarningConditions(self):
        licence_type = self.getLicencePortalType()
        archetype_tool = api.portal.get_tool("archetype_tool")
        klass = None
        for type_info in archetype_tool.listRegisteredTypes():
            if type_info["name"] == licence_type:
                klass = type_info.get("klass", None)
                break
        gsm = getGlobalSiteManager()

        terms = set([])
        for scheduled_interface in implementedBy(klass):
            for adapter in gsm.registeredAdapters():
                implements = issubclass(
                    adapter.provided, interfaces.IUrbanWarningCondition
                )
                specific_enough = issubclass(scheduled_interface, adapter.required[0])
                if implements and specific_enough:
                    terms.add((adapter.name, _(adapter.name)))
        return DisplayList(sorted(list(terms), key=lambda name: name[1]))

    security.declarePublic("listWarningLevels")

    def listWarningLevels(self):
        terms = [
            ("info", translate("Info", "plone", context=self.REQUEST)),
            ("warning", translate("Warning", "plone", context=self.REQUEST)),
            ("error", translate("Error", "plone", context=self.REQUEST)),
        ]
        return DisplayList(terms)

    def default_numerotation_source(self):
        return self.id

    security.declarePublic("get_authorized_folder_managers_base_query")

    def get_authorized_folder_managers_base_query(self):
        """
        Return the folder were are stored folder managers
        """
        portal = api.portal.get_tool("portal_url").getPortalObject()
        rootPath = "/".join(portal.getPhysicalPath())
        urban_tool = api.portal.get_tool("portal_urban")
        ids = []
        for foldermanager in urban_tool.foldermanagers.objectValues():
            if self.id in map(str.lower, foldermanager.getManageableLicences()):
                ids.append(foldermanager.getId())
        dict = {}
        dict["path"] = {"query": "%s/portal_urban/foldermanagers" % (rootPath)}
        dict["id"] = ids
        return dict

    def get_vocabulary_folders(self):
        voc_types = set(VOCABULARY_TYPES)
        folders = [
            ob
            for ob in self.objectValues()
            if hasattr(ob, "immediatelyAddableTypes")
            and voc_types.intersection(set(ob.immediatelyAddableTypes))
        ]
        return folders


registerType(LicenceConfig, PROJECTNAME)
# end of class LicenceConfig

##code-section module-footer #fill in your manual code here
##/code-section module-footer
