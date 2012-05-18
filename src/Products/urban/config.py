# -*- coding: utf-8 -*-
#
# File: urban.py
#
# Copyright (c) 2012 by CommunesPlone
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
##code-section config-head #fill in your manual code here
##/code-section config-head


PROJECTNAME = "urban"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))
ADD_CONTENT_PERMISSIONS = {
    'GenericLicence': 'urban: Add GenericLicence',
    'Contact': 'urban: Add Contact',
    'Street': 'urban: Add Street',
    'UrbanEvent': 'urban: Add UrbanEvent',
    'UrbanEventType': 'urban: Add UrbanEventType',
    'Recipient': 'urban: Add Recipient',
    'BuildLicence': 'urban: Add BuildLicence',
    'ParcelOutLicence': 'urban: Add ParcelOutLicence',
    'Geometrician': 'urban: Add Geometrician',
    'FolderManager': 'urban: Add FolderManager',
    'UrbanVocabularyTerm': 'urban: Add UrbanVocabularyTerm',
    'PortionOut': 'urban: Add PortionOut',
    'RecipientCadastre': 'urban: Add RecipientCadastre',
    'Layer': 'urban: Add Layer',
    'Declaration': 'urban: Add Declaration',
    'ParcellingTerm': 'urban: Add ParcellingTerm',
    'PcaTerm': 'urban: Add PcaTerm',
    'City': 'urban: Add City',
    'UrbanCertificateBase': 'urban: Add UrbanCertificateBase',
    'UrbanCertificateTwo': 'urban: Add UrbanCertificateTwo',
    'EnvironmentalDeclaration': 'urban: Add EnvironmentalDeclaration',
    'Equipment': 'urban: Add Equipment',
    'Lot': 'urban: Add Lot',
    'Division': 'urban: Add Division',
    'UrbanDelay': 'urban: Add UrbanDelay',
    'Locality': 'urban: Add Locality',
    'LicenceConfig': 'urban: Add LicenceConfig',
    'PersonTitleTerm': 'urban: Add PersonTitleTerm',
    'Inquiry': 'urban: Add Inquiry',
    'UrbanEventInquiry': 'urban: Add UrbanEvent',
    'UrbanEventOpinionRequest': 'urban: Add UrbanEventOpinionRequest',
    'OrganisationTerm': 'urban: Add OrganisationTerm',
    'MiscDemand': 'urban: Add MiscDemand',
}

setDefaultRoles('urban: Add GenericLicence', ("Manager", "Contributor"))
setDefaultRoles('urban: Add Contact', ("Manager", "Contributor"))
setDefaultRoles('urban: Add Street', ("Manager", "Contributor"))
setDefaultRoles('urban: Add UrbanEvent', ("Manager", "Contributor"))
setDefaultRoles('urban: Add UrbanEventType', ("Manager", "Contributor"))
setDefaultRoles('urban: Add Recipient', ("Manager", "Contributor"))
setDefaultRoles('urban: Add BuildLicence', ("Manager", "Contributor"))
setDefaultRoles('urban: Add ParcelOutLicence', ("Manager", "Contributor"))
setDefaultRoles('urban: Add Geometrician', ("Manager", "Contributor"))
setDefaultRoles('urban: Add FolderManager', ("Manager", "Contributor"))
setDefaultRoles('urban: Add UrbanVocabularyTerm', ("Manager", "Contributor"))
setDefaultRoles('urban: Add PortionOut', ("Manager", "Contributor"))
setDefaultRoles('urban: Add RecipientCadastre', ("Manager", "Contributor"))
setDefaultRoles('urban: Add Layer', ("Manager", "Contributor"))
setDefaultRoles('urban: Add Declaration', ("Manager", "Contributor"))
setDefaultRoles('urban: Add ParcellingTerm', ("Manager", "Contributor"))
setDefaultRoles('urban: Add PcaTerm', ("Manager", "Contributor"))
setDefaultRoles('urban: Add City', ("Manager", "Contributor"))
setDefaultRoles('urban: Add UrbanCertificateBase', ("Manager", "Contributor"))
setDefaultRoles('urban: Add UrbanCertificateTwo', ("Manager", "Contributor"))
setDefaultRoles('urban: Add EnvironmentalDeclaration', ("Manager", "Contributor"))
setDefaultRoles('urban: Add Equipment', ("Manager", "Contributor"))
setDefaultRoles('urban: Add Lot', ("Manager", "Contributor"))
setDefaultRoles('urban: Add Division', ("Manager", "Contributor"))
setDefaultRoles('urban: Add UrbanDelay', ("Manager", "Contributor"))
setDefaultRoles('urban: Add Locality', ("Manager", "Contributor"))
setDefaultRoles('urban: Add LicenceConfig', ("Manager", "Contributor"))
setDefaultRoles('urban: Add PersonTitleTerm', ("Manager", "Contributor"))
setDefaultRoles('urban: Add Inquiry', ("Manager", "Contributor"))
setDefaultRoles('urban: Add UrbanEventOpinionRequest', ('Manager', 'Owner', 'Contributor'))
setDefaultRoles('urban: Add OrganisationTerm', ("Manager", "Contributor"))
setDefaultRoles('urban: Add MiscDemand', ("Manager", "Contributor"))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
STYLESHEETS = []
JAVASCRIPTS = []

#Add an empty value in vocabulary display proposing to choose a value and returning an error if not changed
ADD_EMPTY_VOCAB_VALUE = True
#topics
TOPIC_TYPE = "urban_topic_type"
#dependencies
DEPENDENCIES = []
#name of the folder created in a licence that will contain additional
#layers linked to the licence and used in the mapfile generation
ADDITIONAL_LAYERS_FOLDER="additional_layers"

#a list where first element is the meetingConfigId and the second, the meta_type name
URBAN_TYPES = ['BuildLicence','ParcelOutLicence','Declaration', 'Division', 'UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter', 'EnvironmentalDeclaration', 'MiscDemand', ]

#the different templates used to structure a document
GLOBAL_TEMPLATES = [
                    {'id':'header.odt', 'title':'Fichier d\'en-tête pour les modèles de document'},
                    {'id':'footer.odt', 'title':'Fichier de pied de page pour les modèles de document'},
                    {'id':'reference.odt', 'title':'Fichier gérant la zone \'Référence\' pour les modèles de document'},
                    {'id':'signatures.odt', 'title':'Fichier gérant les signatures pour les modèles de document'},
                    {'id':'statsins.odt', 'title':'Fichier modèle pour les statistiques INS'},
                    {'id':'styles.odt', 'title':'Fichier gérant les styles communs aux différents modèles de document'},
                   ]
#the different formats proposed for generating document
GENERATED_DOCUMENT_FORMATS = {'odt':'application/vnd.oasis.opendocument.text' ,'doc':'application/msword'}
#empty value used for listboxes
EMPTY_VOCAB_VALUE = 'choose_a_value'

PPNC_LAYERS = {
    'ppnc1' : {'xmin':40824, 'ymin':113446, 'xmax':139390, 'ymax':168195},
    'ppnc2' : {'xmin':122374, 'ymin':116510, 'xmax':218186, 'ymax':169730},
    'ppnc3' : {'xmin':202155, 'ymin':115165, 'xmax':302832, 'ymax':171088},
    'ppnc4' : {'xmin':95175, 'ymin':64858, 'xmax':196930, 'ymax':121379},
    'ppnc5' : {'xmin':191082, 'ymin':62858, 'xmax':300067, 'ymax':123394},
    'ppnc6' : {'xmin':176533, 'ymin':18317, 'xmax':270345, 'ymax':70426},
        }
#From Qgis
#PPNC : 27303,15803 : 311226,173511
#ppnc1: 40824,113446 : 139390,168195
#ppnc2: 122374,116510 : 218186,169730
#ppnc3: 202155,115165 : 302832,171088
#ppnc4: 95175,64858 : 196930,121379
#ppnc5: 191082,62858 : 300067,123394
#ppnc6: 176533,18317 : 270345,70426

equipmentAndRoadRequirementsDefaultValue = """
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
<p>11. En aucun cas la Ville de Mons ne pourra être tenue responsable du non respect du rapport de XXXX ainsi que du non respect des normes pour l’implantation dudit système, par le demandeur.  Nous rappelons au demandeur que le système de dispersion ne peut être à moins de 5m de toute zone capable de bâtisse et à moins de 3m de toute limite de propriété voisine et arbres.</p>
<p>12. En ce qui concerne le principe de dispersion, le demandeur réalisera à ses frais un test de conductivité hydraulique afin de s’assurer du système de dispersion à retenir ainsi que de son bon dimensionnement.  La Ville de Mons ne pourra être tenue responsable de tout problème lié au système de dispersion choisi par le demandeur.  Nous rappelons au demandeur que le système de dispersion ne peut être à moins de 5m de toute zone capable de bâtisse et à moins de 3m de toute limite de propriété voisine et arbres.</p>
<p>13. Le bâtiment étant existant, ce dernier doit être déjà raccordé à l’égout public, dès lors tout nouveau raccord à l’égout public devra clairement être justifié par le biais d’une demande d’autorisation séparée auprès de notre administration qui étudiera la motivation du demandeur. Il est à noter que ces travaux de raccord sont à charge du demandeur. (**) Art. R. 277 § 1<sup>er</sup></p>
<p>14. Le raccordement à cet endroit présente des risques d’inondation en cas de fortes pluies.  Le demandeur prend en charge les risques éventuels liés aux inondations ainsi que toutes les précautions inhérentes à ce type de raccordement.</p>
<p>15. Eaux de ruissellement du hall technique et des aires de manœuvres transiteront via séparateur d’hydrocarbure et débourbeur.</p>
<p>16. <span>La piscine doit être entretenue par filtre.  Le rejet des eaux excédentaires et des eaux de vidange se fera via une pompe dans le réseau existant de l’habitation privée jouxtant la piscine.</span></p>
<p>17. Vu l’espace réduit pour un système de dispersion performant, une fosse à vidanger est une solution envisageable dans l’attente d’un raccord au futur égout public. Néanmoins, nous attirons l’attention du demandeur sur le principe de la fosse à vidanger. Cette solution est accordée à titre exceptionnelle. Le demandeur veillera à entretenir et à vidanger à fréquence régulière sa fosse. La Ville de Mons ne pourra être tenu responsable de toute négligence de la part du demandeur à l’encontre de la fosse à vidanger et de la citerne à eaux de pluies. Le demandeur prendra toutes les mesures utiles et nécessaires ainsi que toutes les précautions inhérentes à ce système d’égouttage</p>
<p><b>(**) A.G.W. du 3 mars 2005 relatif au livre II du Code de l’Environnement contenant le Code de l’Eau (M.B. 12/04/2005 – err.21/06/2005), modifié par A.G.W. le 06 décembre 2006 (MB 17.01.2007) relatif au règlement général d’assainissement des eaux urbaines résiduaires.</b></p>
"""

technicalRemarksDefaultValue = """
<p>1. Les portes (de garage ou autres) et les fenêtres ne peuvent en s’ouvrant faire saillie sur le domaine public.</p>
<p>2. La Ville de Mons impose de signifier à l’entreprise engagée et au demandeur pour le présent permis de réaliser le nettoyage du trottoir et de la voirie vu que les travaux de XXXX engendreront de la poussière, des débris de briques, …  En cas de non application d’un tel système, la Ville de Mons se réserve le droit de sanctionner l’entreprise engagée et le demandeur par le biais de tous les recours légaux en la matière.</p>
<p>3. Si le présent permis nécessite une occupation (même partielle) du domaine public, l’entreprise engagée devra introduire au préalable une demande d’ordonnance de police auprès du Service « Réglementation de Police » pour être autorisée à occuper le domaine public nécessaire à l’emprise du chantier.</p>
<p>4. Il est imposé au demandeur de procéder à la réalisation d’un état des lieux contradictoire du domaine public (voirie + trottoir) existant le long du bien concerné et ce avant le début des travaux.  Cet état des lieux sera dressé par l’auteur de projet ou un géomètre-expert mandaté par le demandeur à cet effet.  L’état des lieux contradictoire sera déposé obligatoirement en trois exemplaires à l’Administration communale pour approbation.  Les frais de l’état des lieux sont à charge du demandeur.  A défaut d’état des lieux contradictoire, la Ville de Mons se réserve le droit de sanctionner le demandeur du présent permis par le biais de tous les recours légaux en la matière.</p>
<p>5. La voirie ainsi que le trottoir sont présumés en bon état sauf état des lieux à charge du demandeur.</p>
<p>6. La réfection ou la construction de trottoir, l’abaissement de bordures et le voûtement de fossé feront l’objet d’une demande d’autorisation séparée auprès de l’administration communale.  Ces travaux sont à charge du demandeur.</p>
<p>7. Le seuil de portes restera dans l’alignement de la façade actuelle.  Il ne sera pas toléré de débordement sur le domaine public.</p>
"""

claimsTextDefaultValue = """
Considérant que xxx réclamations écrites ont été introduites au cours de l'enquête émanant des riverains (xxx lettres identiques et xxx lettres individuelles);
Considérant que xxx réclamations orales ont été consignées dans le registre;
Considérant que ces réclamations portent principalement sur :
    * ...
    * ...
    * ...
Attendu qu'une réunion de clôture d'enquête à été organisée le xxx dans les bureaux du service de l'urbanisme de la Commune de Mons, conformément aux dispositions de l'article 340 du Code modifié;
Considérant qu'aucune personnes ne s'est présentée lors de cette réunion pour faire opposition;
Considérant que xxx personnes se sont présentées à cette réunion et ont émis les réclamations suivantes :
    * ...
    * ...
    * ...
"""

NULL_VALUE = "..."
##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from Products.urban.AppConfig import *
except ImportError:
    pass
