# -*- coding: utf-8 -*-
#
# File: urban.py
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


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from collections import OrderedDict
from ConfigParser import ConfigParser

from Products.CMFCore.permissions import setDefaultRoles

import os
import importlib

PROJECTNAME = "urban"
URBAN_CFG_DIR = "{}/var/urban".format(os.environ.get("PWD", os.getcwd()))


class ExternalConfig(object):
    """ """

    def __init__(self, config_name):
        self.parser = None
        self.sections = {}
        parser = ConfigParser()
        parser.read("{}/{}.cfg".format(URBAN_CFG_DIR, config_name))
        self.parser = parser
        for section in parser.sections():
            self.sections[section] = dict(self.parser.items(section))

    def __getattr__(self, attr_name):
        return self.section(attr_name)

    def section(self, section_name):
        return self.sections.get(section_name, {})


MAP_VIEWER_CFG = ExternalConfig("mapviewer")
URBANMAP_CFG = ExternalConfig("urbanmap")
NIS = URBANMAP_CFG.urbanmap.get("nis", "")

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ("Manager", "Owner", "Contributor"))
ADD_CONTENT_PERMISSIONS = {
    "Applicant": "urban: Add Applicant",
    "Article127": "urban: Add Article127",
    "BuildLicence": "urban: Add BuildLicence",
    "CODT_Article127": "urban: Add CODT_Article127",
    "CODT_BuildLicence": "urban: Add CODT_BuildLicence",
    "CODT_CommercialLicence": "urban: Add CODT_CommercialLicence",
    "CODT_IntegratedLicence": "urban: Add CODT_IntegratedLicence",
    "CODT_ParcelOutLicence": "urban: Add CODT_ParcelOutLicence",
    "CODT_UniqueLicence": "urban: Add CODT_UniqueLicence",
    "CODT_UrbanCertificateTwo": "urban: Add CODT_UrbanCertificateTwo",
    "CODT_UrbanCertificateBase": "urban: Add CODT_UrbanCertificateBase",
    "Contact": "urban: Add Contact",
    "Corporation": "urban: Add Corporation",
    "Couple": "urban: Add Couple",
    "City": "urban: Add City",
    "Claimant": "urban: Add Claimant",
    "ConfigTest": "urban: Add ConfigTest",
    "Declaration": "urban: Add Declaration",
    "Division": "urban: Add Division",
    "EnvClassOne": "urban: Add EnvClassOne",
    "EnvClassThree": "urban: Add EnvClassThree",
    "EnvClassTwo": "urban: Add EnvClassTwo",
    "EnvClassBordering": "urban: Add EnvClassBordering",
    "EnvironmentBase": "urban: Add EnvironmentBase",
    "EnvironmentLicence": "urban: Add EnvironmentLicence",
    "EnvironmentRubricTerm": "urban: Add EnvironmentRubricTerm",
    "FolderManager": "urban: Add FolderManager",
    "GenericLicence": "urban: Add GenericLicence",
    "Inquiry": "urban: Add Inquiry",
    "CODT_Inquiry": "urban: Add CODT_Inquiry",
    "CODT_UniqueLicenceInquiry": "urban: Add CODT_UniqueLicenceInquiry",
    "IntegratedLicence": "urban: Add IntegratedLicence",
    "LicenceConfig": "urban: Add LicenceConfig",
    "Locality": "urban: Add Locality",
    "MiscDemand": "urban: Add MiscDemand",
    "OpinionRequestEventType": "urban: Add OpinionRequestEventType",
    "OrganisationTerm": "urban: Add OrganisationTerm",
    "ParcelOutLicence": "urban: Add ParcelOutLicence",
    "PatrimonyCertificate": "urban: Add PatrimonyCertificate",
    "PcaTerm": "urban: Add PcaTerm",
    "PersonTitleTerm": "urban: Add PersonTitleTerm",
    "PreliminaryNotice": "urban: Add PreliminaryNotice",
    "ProjectMeeting": "urban: Add ProjectMeeting",
    "Recipient": "urban: Add Recipient",
    "RecipientCadastre": "urban: Add RecipientCadastre",
    "SpecificFeatureTerm": "urban: Add SpecificFeatureTerm",
    "Street": "urban: Add Street",
    "UniqueLicence": "urban: Add UniqueLicence",
    "UrbanEvent": "urban: Add UrbanEvent",
    "UrbanEventInquiry": "urban: Add UrbanEvent",
    "UrbanEventInquiry": "urban: Add UrbanEvent",
    "UrbanEventType": "urban: Add UrbanEventType",
    "UrbanVocabularyTerm": "urban: Add UrbanVocabularyTerm",
    "UrbanCertificateBase": "urban: Add UrbanCertificateBase",
    "UrbanCertificateTwo": "urban: Add UrbanCertificateTwo",
    "UrbanDelay": "urban: Add UrbanDelay",
    "UrbanEventOpinionRequest": "urban: Add UrbanEventOpinionRequest",
    "UrbanConfigurationValue": "urban: Add UrbanConfigurationValue",
    "ExplosivesPossession": "urban: Add ExplosivesPossession",
    "Inspection": "urban: Add Inspection",
    "RoadDecree": "urban: Add RoadDecree",
}

setDefaultRoles("urban: Add Applicant", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Article127", ("Manager", "Contributor"))
setDefaultRoles("urban: Add BuildLicence", ("Manager", "Contributor"))
setDefaultRoles("urban: Add City", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Claimant", ("Manager", "Contributor", "ClaimantEditor"))
setDefaultRoles("urban: Add CODT_Article127", ("Manager", "Contributor"))
setDefaultRoles("urban: Add CODT_BuildLicence", ("Manager", "Contributor"))
setDefaultRoles("urban: Add CODT_CommercialLicence", ("Manager", "Contributor"))
setDefaultRoles("urban: Add CODT_IntegratedLicence", ("Manager", "Contributor"))
setDefaultRoles("urban: Add CODT_NotaryLetter", ("Manager", "Contributor"))
setDefaultRoles("urban: Add CODT_ParcelOutLicence", ("Manager", "Contributor"))
setDefaultRoles("urban: Add CODT_UniqueLicence", ("Manager", "Contributor"))
setDefaultRoles("urban: Add CODT_UrbanCertificateOne", ("Manager", "Contributor"))
setDefaultRoles("urban: Add CODT_UrbanCertificateTwo", ("Manager", "Contributor"))
setDefaultRoles("urban: Add CODT_UrbanCertificateBase", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Contact", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Corporation", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Couple", ("Manager", "Contributor"))
setDefaultRoles("urban: Add ConfigTest", ("Manager",))
setDefaultRoles("urban: Add Declaration", ("Manager", "Contributor"))
setDefaultRoles("urban: Add EnvClassOne", ("Manager", "Contributor"))
setDefaultRoles("urban: Add EnvClassThree", ("Manager", "Contributor"))
setDefaultRoles("urban: Add EnvClassTwo", ("Manager", "Contributor"))
setDefaultRoles("urban: Add EnvClassBordering", ("Manager", "Contributor"))
setDefaultRoles("urban: Add EnvironmentBase", ("Manager", "Contributor"))
setDefaultRoles("urban: Add EnvironmentLicence", ("Manager", "Contributor"))
setDefaultRoles("urban: Add EnvironmentRubricTerm", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Division", ("Manager", "Contributor"))
setDefaultRoles("urban: Add FolderManager", ("Manager", "Contributor"))
setDefaultRoles("urban: Add GenericLicence", ("Manager", "Contributor"))
setDefaultRoles("urban: Add IntegratedLicence", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Inspection", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Inquiry", ("Manager", "Contributor"))
setDefaultRoles("urban: Add CODT_Inquiry", ("Manager", "Contributor"))
setDefaultRoles("urban: Add LicenceConfig", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Locality", ("Manager", "Contributor"))
setDefaultRoles("urban: Add MiscDemand", ("Manager", "Contributor"))
setDefaultRoles("urban: Add OpinionRequestEventType", ("Manager", "Contributor"))
setDefaultRoles("urban: Add OrganisationTerm", ("Manager", "Contributor"))
setDefaultRoles("urban: Add ParcelOutLicence", ("Manager", "Contributor"))
setDefaultRoles("urban: Add PatrimonyCertificate", ("Manager", "Contributor"))
setDefaultRoles("urban: Add PcaTerm", ("Manager", "Contributor"))
setDefaultRoles("urban: Add PersonTitleTerm", ("Manager", "Contributor"))
setDefaultRoles("urban: Add PreliminaryNotice", ("Manager", "Contributor"))
setDefaultRoles("urban: Add ProjectMeeting", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Recipient", ("Manager", "Contributor"))
setDefaultRoles("urban: Add RecipientCadastre", ("Manager", "Contributor", "Editor"))
setDefaultRoles("urban: Add SpecificFeatureTerm", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Street", ("Manager", "Contributor"))
setDefaultRoles("urban: Add Ticket", ("Manager", "Contributor"))
setDefaultRoles("urban: Add UrbanEvent", ("Manager", "Contributor"))
setDefaultRoles("urban: Add UniqueLicence", ("Manager", "Contributor"))
setDefaultRoles("urban: Add UrbanEventType", ("Manager", "Contributor"))
setDefaultRoles("urban: Add UrbanCertificateBase", ("Manager", "Contributor"))
setDefaultRoles("urban: Add UrbanCertificateTwo", ("Manager", "Contributor"))
setDefaultRoles("urban: Add UrbanDelay", ("Manager", "Contributor"))
setDefaultRoles("urban: Add UrbanEventOpinionRequest", ("Manager", "Contributor"))
setDefaultRoles("urban: Add UrbanConfigurationValue", ("Manager",))
setDefaultRoles("urban: Add UrbanVocabularyTerm", ("Manager", "Contributor"))
setDefaultRoles("urban: Add ExplosivesPossession", ("Manager", "Contributor"))
setDefaultRoles("urban: Add RoadDecree", ("Manager", "Contributor"))

product_globals = globals()

# name of the folder created in a licence that will contain additional
# layers linked to the licence and used in the mapfile generation
ADDITIONAL_LAYERS_FOLDER = "additional_layers"

# a list where first element is the meetingConfigId and the second, the meta_type name
URBAN_TYPES = [
    "BuildLicence",
    "CODT_BuildLicence",
    "Article127",
    "CODT_Article127",
    "CODT_CommercialLicence",
    "IntegratedLicence",
    "CODT_IntegratedLicence",
    "UniqueLicence",
    "CODT_UniqueLicence",
    "Declaration",
    "UrbanCertificateOne",
    "CODT_UrbanCertificateOne",
    "UrbanCertificateTwo",
    "CODT_UrbanCertificateTwo",
    "PreliminaryNotice",
    "PatrimonyCertificate",
    "EnvClassOne",
    "EnvClassTwo",
    "EnvClassThree",
    "EnvClassBordering",
    "ParcelOutLicence",
    "CODT_ParcelOutLicence",
    "MiscDemand",
    "Division",
    "NotaryLetter",
    "CODT_NotaryLetter",
    "ProjectMeeting",
    "ExplosivesPossession",
    # 'RoadDecree',
    "Inspection",
    "Ticket",
]

URBAN_TYPES_ACRONYM = {
    "BuildLicence": "P",
    "CODT_BuildLicence": "P",
    "Article127": "PA",
    "CODT_Article127": "PA",
    "CODT_CommercialLicence": "PIC",
    "IntegratedLicence": "PI",
    "CODT_IntegratedLicence": "PI",
    "UniqueLicence": "PU",
    "CODT_UniqueLicence": "PU",
    "Declaration": "D",
    "UrbanCertificateOne": "CU1",
    "CODT_UrbanCertificateOne": "CU1",
    "UrbanCertificateTwo": "CU2",
    "CODT_UrbanCertificateTwo": "CU2",
    "PreliminaryNotice": "AP",
    "PatrimonyCertificate": "CP",
    "EnvClassOne": "PE1",
    "EnvClassTwo": "PE2",
    "EnvClassThree": "DE",
    "EnvClassBordering": "PEL",
    "ParcelOutLicence": "PURB",
    "CODT_ParcelOutLicence": "PURB",
    "MiscDemand": "DD",
    "Division": "DIV",
    "NotaryLetter": "NOT",
    "CODT_NotaryLetter": "NOT",
    "ProjectMeeting": "R",
    "ExplosivesPossession": "EXP",
    "RoadDecree": "DV",
    "Inspection": "INSP",
    "Ticket": "PV",
}

URBAN_CWATUPE_TYPES = [
    "BuildLicence",
    "Article127",
    "IntegratedLicence",
    "UniqueLicence",
    "Declaration",
    "UrbanCertificateOne",
    "UrbanCertificateTwo",
    "PreliminaryNotice",
    "PatrimonyCertificate",
    "ParcelOutLicence",
    "MiscDemand",
    "Division",
    "NotaryLetter",
    "RoadDecree",
    "Inspection",
    "Ticket",
]

URBAN_CODT_TYPES = [
    "CODT_BuildLicence",
    "CODT_Article127",
    "CODT_CommercialLicence",
    "CODT_IntegratedLicence",
    "CODT_ParcelOutLicence",
    "CODT_UniqueLicence",
    "CODT_UrbanCertificateTwo",
    "CODT_UrbanCertificateOne",
    "CODT_NotaryLetter",
    "ProjectMeeting",
    "MiscDemand",
    "PreliminaryNotice",
    "PatrimonyCertificate",
    "Division",
    "RoadDecree",
    "Inspection",
    "Ticket",
]

URBAN_ENVIRONMENT_TYPES = [
    "EnvClassOne",
    "EnvClassTwo",
    "EnvClassThree",
    "ExplosivesPossession",
    "EnvClassBordering",
]

LICENCE_FINAL_STATES = [
    "accepted",
    "refused",
    "retired",
    "abandoned",
    "inacceptable",
    "need_parceloutlicence",
    "ended",
]

VOCABULARY_TYPES = [
    "UrbanVocabularyTerm",
    "PcaTerm",
    "UrbanDelay",
    "EventConfig",
    "OpinionEventConfig",
    "PersonTitleTerm",
    "OrganisationTerm",
]

# all types that can be used as a licence applicant
APPLICANTS_TYPES = [
    "Applicant",
    "Proprietary",
    "Corporation",
    "CorporationProprietary",
    "Tenant",
    "Plaintiff",
    "Couple",
]

# the different templates used to structure a document
GLOBAL_TEMPLATES = {
    ".": [],
    "urbantemplates": [
        {"id": "logo.odt", "portal_type": "SubTemplate", "title": "Logo urbanisme"},
        {
            "id": "header.odt",
            "portal_type": "SubTemplate",
            "title": "En-tête urbanisme",
        },
        {
            "id": "footer.odt",
            "portal_type": "SubTemplate",
            "title": "Pied de page urbanisme",
        },
        {
            "id": "reference.odt",
            "portal_type": "SubTemplate",
            "title": "'Référence' urbanisme",
        },
        {
            "id": "signatures.odt",
            "portal_type": "SubTemplate",
            "title": "Signatures urbanisme",
        },
        {
            "id": "publipostage.odt",
            "portal_type": "MailingLoopTemplate",
            "title": "Publipostage urbanisme",
        },
    ],
    "environmenttemplates": [
        {"id": "logo.odt", "portal_type": "SubTemplate", "title": "Logo environnement"},
        {
            "id": "header.odt",
            "portal_type": "SubTemplate",
            "title": "En-tête environnement",
        },
        {
            "id": "footer.odt",
            "portal_type": "SubTemplate",
            "title": "Pied de page environnement",
        },
        {
            "id": "reference.odt",
            "portal_type": "SubTemplate",
            "title": "'Référence' environnement",
        },
        {
            "id": "signatures.odt",
            "portal_type": "SubTemplate",
            "title": "Signatures environnement",
        },
        {
            "id": "publipostage.odt",
            "portal_type": "MailingLoopTemplate",
            "title": "Publipostage environnement",
        },
    ],
}

URBAN_EVENT_TYPES = [
    "UrbanEvent",
    "UrbanEventInquiry",
    "UrbanEventOpinionRequest",
    "UrbanEventAnnouncement",
    "UrbanEventCollege",
    "UrbanEventFollowUp",
    "UrbanEventMayor",
    "UrbanEventInspectionReport",
    "UrbanEventNotificationCollege",
]

DASHBOARD_TEMPLATES = {
    ".": [
        {
            "id": "statsins.odt",
            "portal_type": "DashboardPODTemplate",
            "title": "Statistiques INS",
        },
        {
            "id": "listing-general.ods",
            "portal_type": "DashboardPODTemplate",
            "title": "Listing des permis",
            "use_objects": True,
        },
        # {
        # 'id': 'folderlisting.odt',
        # 'portal_type': 'DashboardPODTemplate',
        # 'title': 'Liste',
        # },
    ],
}
# the different formats proposed for generating document
GENERATED_DOCUMENT_FORMATS = {
    "odt": "application/vnd.oasis.opendocument.text",
    "doc": "application/msword",
}
# empty value used for listboxes
EMPTY_VOCAB_VALUE = "choose_a_value"

PPNC_LAYERS = {
    "ppnc1": {"xmin": 40824, "ymin": 113446, "xmax": 139390, "ymax": 168195},
    "ppnc2": {"xmin": 122374, "ymin": 116510, "xmax": 218186, "ymax": 169730},
    "ppnc3": {"xmin": 202155, "ymin": 115165, "xmax": 302832, "ymax": 171088},
    "ppnc4": {"xmin": 95175, "ymin": 64858, "xmax": 196930, "ymax": 121379},
    "ppnc5": {"xmin": 191082, "ymin": 62858, "xmax": 300067, "ymax": 123394},
    "ppnc6": {"xmin": 176533, "ymin": 18317, "xmax": 270345, "ymax": 70426},
}

DefaultTexts = {
    "BuildLicence": {
        "equipmentAndRoadRequirements": """
        <p>1. Aucun descendant d’eaux pluviales ne pourra faire saillie sur le domaine public.  Ils seront intégrés dans la maçonnerie de façade.  Ils seront munis d’un dauphin en fonte d’une hauteur de 1 mètre à partir du sol.  Ils seront raccordés au réseau privatif du bâtiment car aucun rejet d’eaux pluviales sur le domaine public n’est autorisé. Cette donnée technique n’est d’application que si le projet prévoit des descendants d’eaux pluviales en façade à rue.</p>
        <p>2. Reprise de l’extension du réseau d’égouttage sur le réseau existant du bâtiment.</p>
        <p>3. L’égout public n’aboutissant pas encore à une station d’épuration collective, les eaux usées transiteront via fosse septique by passable d’une capacité minimale de 3000 litres, rejet vers égout public. (**) Art. R.277§4</p>
        <p>4. Eaux pluviales via citerne de 10m³ avec trop-plein vers tranchée drainante / vers égout public.</p>
        <p>5. Le niveau de la sortie des eaux sera tel que le raccordement au futur égout public devra être réalisable via une chambre de prélèvement situé en domaine privé, à la limite du domaine public.</p>
        <p>6. Le raccordement à l’égout public fera l’objet d’une demande d’autorisation séparée auprès de l’administration communale.  Il est à noter que ces travaux sont à charge du demandeur.  Il est également rappelé que, l’évacuation des eaux urbaines résiduaires doit se faire soit gravitairement, soit par système de pompage. (**) Art. R.277 § 3</p>
        <p>7. Le demandeur réalisera l’obstruction du raccordement à l’égout public des bâtiments démolis et ce afin d’éviter toutes intrusions de boue, de terre, de déchets… dans l’égouttage public.  La condamnation du raccord particulier abandonné se fera à la limite du domaine public et du domaine privé par un bouchon.</p>
        <p>8. Toute nouvelle habitation doit être équipée d’un système séparant l’ensemble des eaux pluviales des eaux usées. Toutes nouvelle habitation située le long d’une voirie non encore égouttée, doit être équipée d’une fosse sceptique by-passable d’une capacité de 3000 litres. La fosse septique by-passable est implantée préférentiellement entre l’habitation et le futur réseau d’égouttage de manière à faciliter le raccordement ultérieur au futur égout public. Les eaux usées en sortie de la fosse septique seront évacuées vers XXXX. (**) Art. R. 277 § 4</p>
        <p>9. Toute nouvelle habitation construite en zone soumise au régime d’assainissement collectif le long d’une voirie non encore équipée d’égouts doit être équipée d’origine d’un système d’épuration répondant aux conditions définies dans les arrêtés pris en exécution du décret du 11 mars 1999 relatif au permis d’environnement, lorsqu’il est d’ores et déjà établi le coût du raccordement à un égout futur serait excessif en vertu du 1<sup>er</sup> Art. R. 278 (**)</p>
        <p>10. En ce qui concerne le système dispersant, nous rappelons au demandeur que le XXXX a procédé à un test de percolation.  Nous nous référons aux conclusions dudit rapport y relatif de XXXX qui préconisait l’emploi d’un YYYYY pour la dispersion des eaux usées traitées et de pluies.  L’implantation du système de dispersion par le demandeur se fera suivant les normes en vigueur.</p>
        <p>11. En aucun cas la Ville de XXX ne pourra être tenue responsable du non respect du rapport de XXXX ainsi que du non respect des normes pour l’implantation dudit système, par le demandeur.  Nous rappelons au demandeur que le système de dispersion ne peut être à moins de 5m de toute zone capable de bâtisse et à moins de 3m de toute limite de propriété voisine et arbres.</p>
        <p>12. En ce qui concerne le principe de dispersion, le demandeur réalisera à ses frais un test de conductivité hydraulique afin de s’assurer du système de dispersion à retenir ainsi que de son bon dimensionnement.  La Ville de XXX ne pourra être tenue responsable de tout problème lié au système de dispersion choisi par le demandeur.  Nous rappelons au demandeur que le système de dispersion ne peut être à moins de 5m de toute zone capable de bâtisse et à moins de 3m de toute limite de propriété voisine et arbres.</p>
        <p>13. Le bâtiment étant existant, ce dernier doit être déjà raccordé à l’égout public, dès lors tout nouveau raccord à l’égout public devra clairement être justifié par le biais d’une demande d’autorisation séparée auprès de notre administration qui étudiera la motivation du demandeur. Il est à noter que ces travaux de raccord sont à charge du demandeur. (**) Art. R. 277 § 1<sup>er</sup></p>
        <p>14. Le raccordement à cet endroit présente des risques d’inondation en cas de fortes pluies.  Le demandeur prend en charge les risques éventuels liés aux inondations ainsi que toutes les précautions inhérentes à ce type de raccordement.</p>
        <p>15. Eaux de ruissellement du hall technique et des aires de manœuvres transiteront via séparateur d’hydrocarbure et débourbeur.</p>
        <p>16. <span>La piscine doit être entretenue par filtre.  Le rejet des eaux excédentaires et des eaux de vidange se fera via une pompe dans le réseau existant de l’habitation privée jouxtant la piscine.</span></p>
        <p>17. Vu l’espace réduit pour un système de dispersion performant, une fosse à vidanger est une solution envisageable dans l’attente d’un raccord au futur égout public. Néanmoins, nous attirons l’attention du demandeur sur le principe de la fosse à vidanger. Cette solution est accordée à titre exceptionnelle. Le demandeur veillera à entretenir et à vidanger à fréquence régulière sa fosse. La Ville de XXX ne pourra être tenu responsable de toute négligence de la part du demandeur à l’encontre de la fosse à vidanger et de la citerne à eaux de pluies. Le demandeur prendra toutes les mesures utiles et nécessaires ainsi que toutes les précautions inhérentes à ce système d’égouttage</p>
        <p><b>(**) A.G.W. du 3 mars 2005 relatif au livre II du Code de l’Environnement contenant le Code de l’Eau (M.B. 12/04/2005 – err.21/06/2005), modifié par A.G.W. le 06 décembre 2006 (MB 17.01.2007) relatif au règlement général d’assainissement des eaux urbaines résiduaires.</b></p>
        """,
        "technicalRemarks": """
        <p>1. Les portes (de garage ou autres) et les fenêtres ne peuvent en s’ouvrant faire saillie sur le domaine public.</p>
        <p>2. La Ville de XXX impose de signifier à l’entreprise engagée et au demandeur pour le présent permis de réaliser le nettoyage du trottoir et de la voirie vu que les travaux de XXXX engendreront de la poussière, des débris de briques, …  En cas de non application d’un tel système, la Ville de XXX se réserve le droit de sanctionner l’entreprise engagée et le demandeur par le biais de tous les recours légaux en la matière.</p>
        <p>3. Si le présent permis nécessite une occupation (même partielle) du domaine public, l’entreprise engagée devra introduire au préalable une demande d’ordonnance de police auprès du Service « Réglementation de Police » pour être autorisée à occuper le domaine public nécessaire à l’emprise du chantier.</p>
        <p>4. Il est imposé au demandeur de procéder à la réalisation d’un état des lieux contradictoire du domaine public (voirie + trottoir) existant le long du bien concerné et ce avant le début des travaux.  Cet état des lieux sera dressé par l’auteur de projet ou un géomètre-expert mandaté par le demandeur à cet effet.  L’état des lieux contradictoire sera déposé obligatoirement en trois exemplaires à l’Administration communale pour approbation.  Les frais de l’état des lieux sont à charge du demandeur.  A défaut d’état des lieux contradictoire, la Ville de XXX se réserve le droit de sanctionner le demandeur du présent permis par le biais de tous les recours légaux en la matière.</p>
        <p>5. La voirie ainsi que le trottoir sont présumés en bon état sauf état des lieux à charge du demandeur.</p>
        <p>6. La réfection ou la construction de trottoir, l’abaissement de bordures et le voûtement de fossé feront l’objet d’une demande d’autorisation séparée auprès de l’administration communale.  Ces travaux sont à charge du demandeur.</p>
        <p>7. Le seuil de portes restera dans l’alignement de la façade actuelle.  Il ne sera pas toléré de débordement sur le domaine public.</p>
        """,
    }
}


NULL_VALUE = "..."


def registerClasses():
    """ArchGenXML generated code does not register Archetype classes at the
    right moment since model adaptations have been implemented. This method
    allows to perform class registration at the right moment."""
    import Products.Archetypes
    from Products.Archetypes.atapi import registerType

    global ADD_CONTENT_PERMISSIONS
    classNames = ADD_CONTENT_PERMISSIONS.keys()
    for name in classNames:
        try:
            exec "import Products.urban.%s as module" % name
        except ImportError:
            module = getattr(importlib.import_module("Products.urban"), name)
        klass = getattr(module, name)
        key = "urban.%s" % name
        if key in Products.Archetypes.ATToolModule._types:
            # Unregister the class
            del Products.Archetypes.ATToolModule._types[key]
        delattr(klass, "__ac_permissions__")
        registerType(klass, PROJECTNAME)
