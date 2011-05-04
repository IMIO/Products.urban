# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2011 by CommunesPlone
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('urban: setuphandlers')
from Products.urban.config import PROJECTNAME
from Products.urban.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
from Products.PageTemplates.GlobalTranslationService import getGlobalTranslationService
from Acquisition import aq_base
from Products.urban.config import TOPIC_TYPE
from Products.CMFCore.WorkflowCore import WorkflowException
from zExceptions import BadRequest
from Products.ZCatalog.Catalog import CatalogError
from Products.urban.config import URBAN_TYPES, PPNC_LAYERS
from zope.annotation.interfaces import IAnnotations
from plone.app.portlets.portlets import classic
service = getGlobalTranslationService()
##/code-section HEAD

def isNoturbanProfile(context):
    return context.readDataFile("urban_marker.txt") is None

def setupHideToolsFromNavigation(context):
    """hide tools"""
    if isNoturbanProfile(context): return
    # uncatalog tools
    site = context.getSite()
    toolnames = ['portal_urban']
    portalProperties = getToolByName(site, 'portal_properties')
    navtreeProperties = getattr(portalProperties, 'navtree_properties')
    if navtreeProperties.hasProperty('idsNotToList'):
        for toolname in toolnames:
            try:
                portal[toolname].unindexObject()
            except:
                pass
            current = list(navtreeProperties.getProperty('idsNotToList') or [])
            if toolname not in current:
                current.append(toolname)
                kwargs = {'idsNotToList': current}
                navtreeProperties.manage_changeProperties(**kwargs)



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNoturbanProfile(context): return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code

    if isNoturbanProfile(context): return
    site = context.getSite()

    #we need external edition so make sure it is activated
    site.portal_properties.site_properties.manage_changeProperties(ext_editor = True)

    #rearrange skins so the 'urban' layer is just after 'custom'...
    ps = site.portal_skins
    import string
    #skinname is like 'Plone Default'
    selections = ps._getSelections()
    for skinname in selections:
        sels = selections[skinname].split(',')
        new_sels = ['custom', 'urban', ]
        for sel in sels:
            if sel != 'custom' and sel != 'urban':
                new_sels.append(sel)
    #set the new_sels
    selections[skinname] = string.join(new_sels, ',')

    #install dependencies manually...
    quick_installer = site.portal_quickinstaller
    for dependency in DEPENDENCIES:
        if not dependency in quick_installer.listInstalledProducts():
            quick_installer.installProduct(dependency)

    #add metadata not added yet by PloneTask...
    try:
        site.portal_catalog.addColumn('getBeginDate')
        site.portal_catalog.addColumn('getEndDate')
    except CatalogError:
        #metadatas already exists, we pass...
        pass

    #add our own portal_types to portal_factory
    factory_tool = getToolByName(site, "portal_factory")
    alreadyRegTypes = factory_tool.getFactoryTypes()
    alreadyRegTypes['UrbanCertificateOne'] = 1
    alreadyRegTypes['NotaryLetter'] = 1
    alreadyRegTypes['Notary'] = 1
    alreadyRegTypes['Proprietary'] = 1
    alreadyRegTypes['Applicant'] = 1
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=alreadyRegTypes)

    addUrbanConfigs(context)
    addApplicationFolders(context)
    setDefaultApplicationSecurity(context)
    addGlobalFolders(context)
    addUrbanConfigsTopics(context)
    addUrbanGroups(context)
    adaptDefaultPortal(context)
    #refresh catalog after all these objects have been added...
    logger.info("Refresh portal_catalog : starting...")
    site.portal_catalog.refreshCatalog(clear=True)
    logger.info("Refresh portal_catalog : Done!")

    ann = IAnnotations(site)
    #clear all unused portlet
    for portlet in ann['plone.portlets.contextassignments']['plone.rightcolumn'].keys():
        del ann['plone.portlets.contextassignments']['plone.rightcolumn'][portlet]
    for portlet in ann['plone.portlets.contextassignments']['plone.leftcolumn'].keys():
        if portlet not in ('portlet_urban','login'):
            del ann['plone.portlets.contextassignments']['plone.leftcolumn'][portlet]
    #create portlet Firefox if not exist
    if not ann['plone.portlets.contextassignments']['plone.leftcolumn'].has_key('portlet_firefox'):
        ann['plone.portlets.contextassignments']['plone.leftcolumn']['portlet_firefox'] = classic.Assignment(template='portlet_firefox', macro="portlet")



##code-section FOOT
def addUrbanConfigs(context):
    """
      Add the different urban configs
    """
    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')

    for urban_type in URBAN_TYPES:
        if hasattr(tool, urban_type.lower()):
            continue
        configFolderid = tool.invokeFactory("Folder",id=urban_type.lower(),title=service.translate("urban","%s_urbanconfig_title" % urban_type.lower(),context=site,default=urban_type + 's'))
        configFolder = getattr(tool, configFolderid)
        configFolder.setConstrainTypesMode(1)
        configFolder.setLocallyAllowedTypes(['Folder'])
        configFolder.setImmediatelyAddableTypes(['Folder'])

        #we just created the urbanConfig, proceed with other parameters...
        #add UrbanEventTypes folder
        newFolderid = configFolder.invokeFactory("Folder",id="urbaneventtypes",title=service.translate("urban","urbaneventtypes_folder_title",context=site,default="UrbanEventTypes"))
        newFolder = getattr(configFolder, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanEventType'])
        newFolder.setImmediatelyAddableTypes(['UrbanEventType'])

        #add FolderManagers folder
        newFolderid = configFolder.invokeFactory("Folder",id="foldermanagers",title=service.translate("urban","foldermanagers_folder_title",context=site,default="FolderManagers"))
        newFolder = getattr(configFolder, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['FolderManager'])
        newFolder.setImmediatelyAddableTypes(['FolderManager'])
        if urban_type == 'ParcelOutLicence':
            newFolderid = configFolder.invokeFactory("Folder",id="lotusages",title=service.translate("urban","lotusages_folder_title",context=site,default="LotUsages"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="buildable",title=u"Lot bâtissable")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="greenzone",title=u"Espace vert")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="tosurrendertotown",title=u"Lot à rétrocéder à la commune")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="autre",title=u"Autre")
            newFolderid = configFolder.invokeFactory("Folder",id="equipmenttypes",title=service.translate("urban","folderequipmenttypes_folder_title",context=site,default="EquipmentTypes"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="telecom",title=u"Télécomunication")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="electricity",title=u"Electricité")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="gas",title=u"Gaz")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="teledistribution",title=u"Télédistribution")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="sewers",title=u"Egouttage")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="water",title=u"Eau")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="autre",title=u"Autre")

        if urban_type in ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter', ]:
            #we add the specific features folder
            newFolderid = configFolder.invokeFactory("Folder",id="specificfeatures",title=service.translate("urban","urban_label_specificFeatures",context=site,default="Specific features"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="reglement-regional-urbanisme",title=u"Règlement régional d'urbanisme")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="projet-expropriation",title=u"Projet d'expropriation")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="plan-remembrement",title=u"Plan de remembrement")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="ordonnance-insalubrite",title=u"Ordoncance d'insalubrité")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="legislation-monuments-desaffectes",title=u"Législation monuments désaffectés")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="tuyauterie-gaz-naturel",title=u"Prise souterraine tuyauterie gaz naturel (loi du 12 avril 1965)")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="site-natura-2000",title=u"Site Natura 2000")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="infractions-legislation-urbanisme",title=u"Infractions à la législation sur l'urbanisme ou droit de l'environnement connues")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="perimetre-art-136-136bis",title=u"Périmètre visés aux articles 136 et 136bis du CWATUPE")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="droit-preemption",title=u"Un droit de préemption (article 175 du CWATUPE)")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="liste-sauvegarde-art-193",title=u"Inscrit sur la liste des sauvegardes (article 193 du CWATUPE)")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="classe-art-196",title=u"Classé (article 196 du CWATUPE)")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-de-protection-art-209",title=u"Zone de protection (article 209 du CWATUPE)")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-inondable",title=u"Zone à risque inondable (plan P.L.U.I.E.S.)")

        if urban_type in ['Declaration', ]:
            """
            #add "Articles" folder
            """
            #add 'articles' folder
            newFolderid = configFolder.invokeFactory("Folder",id="articles",title=service.translate("urban","articles_folder_title",context=site,default="Articles"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_1",title=u"article 263 §1er 1° les aménagements conformes à la destination normale des cours et jardins")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_2",title=u"article 263 §1er 2° la pose ou l'enlèvement d'un car-port <30m²")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_3",title=u"article 263 §1er 3° l'ouverture ou la modification de baies")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_4",title=u"article 263 §1er 4° le remplacement de parements d'élévation/couverture de toiture par plus isolants")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_5a",title=u"article 263 §1er 5° a) la construction d'un volume secondaire en contiguïté <30m²")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_5b",title=u"article 263 §1er 5° b) la construction d'un volume secondaire isolé <30m²")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_6a",title=u"article 263 §1er 6° a) la construction d'un abri pour un ou des animaux")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_6b",title=u"article 263 §1er 6° b) la pose d'un rucher")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_6c",title=u"article 263 §1er 6° c) Clôtures/portiques/portillons")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_6d",title=u"article 263 §1er 6° d) Etang/piscine non couverte < 75m²")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_7",title=u"article 263 §1er 7° Démolition <30 m²")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_8a",title=u"article 263 §1er 8° a) les silos de stockage")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_8b",title=u"article 263 §1er 8° b) les dalles de fumière")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_8c",title=u"article 263 §1er 8° c) les citernes de récolte ou de stockage d'eau/effluents d'élevage")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_9",title=u"article 263 §1er 9° la culture de sapins de Noël")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="263_1_10",title=u"article 263 §1er 10° les miradors")

        if urban_type in ['BuildLicence', 'ParcelOutLicence', ]:
            """
            #add Recipients folder
            newFolderid = configFolder.invokeFactory("Folder",id="recipients",title=service.translate("urban","recipients_folder_title",context=site,default="Recipients"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['Recipient'])
            newFolder.setImmediatelyAddableTypes(['Recipient'])
            """
            #add "necessarydocuments" folder
            newFolderid = configFolder.invokeFactory("Folder",id="missingparts",title=service.translate("urban","missingparts_folder_title",context=site,default="Necessary documents"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            if urban_type in ['BuildLicence', ]:
                #necessary documents for BuildLicences
                newFolder.invokeFactory("UrbanVocabularyTerm",id="form_demande",title=u"Formulaire de demande (annexe 20) en 2 exemplaires")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="plan_travaux",title=u"Plan des travaux en 4 exemplaires")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="attestation_archi",title=u"Attestation de l'architecte (annexe 21) en 2 exemplaires")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="attestation_ordre_archi",title=u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="photos",title=u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="notice_environnement",title=u"Notice d'évaluation préalable incidences environnement (annexe 1C) en 2 exemplaires")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="plan_secteur",title=u"Une copie du plan de secteur")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="isolation",title=u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="peb",title=u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires")
            #add FolderCategories folder
            newFolderid = configFolder.invokeFactory("Folder",id="foldercategories",title=service.translate("urban","foldercategories_folder_title",context=site,default="FolderCategories"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            if urban_type in ['BuildLicence', ]:
                #categories for BuildLicences
                newFolder.invokeFactory("UrbanVocabularyTerm",id="uap",title=u"UAP (permis d'urbanisme avec avis préalable du FD)")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="udc",title=u"UDC (permis dans PCA, RCU, LOTISSEMENT, parfois avec demande de dérogation)")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="upp",title=u"UPP (petit permis délivré directement par le Collège)")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="pu",title=u"PU (demande de PERMIS UNIQUE)")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="art127",title=u"UCP (article 127)")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="inconnu",title=u"Inconnue")
            else:
                #categories for ParcelOutLicences
                newFolder.invokeFactory("UrbanVocabularyTerm",id="lap",title=u"LAP (permis de lotir avec avis préalable du FD)")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="lapm",title=u"LAP/M (modification du permis de lotir avec avis du FD)")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="ldc",title=u"LDC (permis de lotir dans un PCA, lotissement ou en décentralisation)")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="ldcm",title=u"LDC/M (modification du permis de lotir dans un PCA, RCU, LOTISSEMENT)")
            #add RoadTypes folder
            newFolderid = configFolder.invokeFactory("Folder",id="folderroadtypes",title=service.translate("urban","folderroadtypes_folder_title",context=site,default="FolderRoadTypes"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="com",title=u"Communale")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="priv",title=u"Privée")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="prov",title=u"Provinciale")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="reg",title=u"Régionale")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="vic",title=u"Vicinale")

            #add RoadEquipments folder
            newFolderid = configFolder.invokeFactory("Folder",id="folderroadequipments",title=service.translate("urban","folderroadequipments_folder_title",context=site,default="FolderRoadEquipments"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="eau",title=u"distribution d'eau")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="electricite",title=u"distribution électrique")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="epuration",title=u"canalisation reliée à une station d'épuration publique")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="nonepuration",title=u"canalisation non-reliée à une station d'épuration publique")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="egoutsep",title=u"réseau d'égoutage séparatif")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="pascollecteeaux",title=u"pas de canalisation de collecte des eaux")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="fosse",title=u"fossé")

            #add ProtectedBuildings folder
            newFolderid = configFolder.invokeFactory("Folder",id="folderprotectedbuildings",title=service.translate("urban","folderprotectedbuildings_folder_title",context=site,default="FolderProtectedBuildings"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="classe",title=u"classé ou assimilé")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zoneprotection",title=u"zone de protection")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="reprisinventaire",title=u"repris à l'inventaire")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="archeologique",title=u"à l'Atlas archéologique")

            #add Zones folder
            newFolderid = configFolder.invokeFactory("Folder",id="folderzones",title=service.translate("urban","folderzones_folder_title",context=site,default="FolderZones"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zh",title=u"zone d’habitat")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zhcr",title=u"zone d’habitat à caractère rural")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zspec",title=u"zone de services publics et d’équipements communautaires")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zcet",title=u"zone de centre d'enfouissement technique")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zl",title=u"zone de loisirs")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zaem",title=u"zones d’activité économique mixte")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zaei",title=u"zones d’activité économique industrielle")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zaesae",title=u"zones d’activité économique spécifique agro-économique")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zaesgd",title=u"zones d’activité économique spécifique grande distribution")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="ze",title=u"zone d’extraction")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zadci",title=u"zone d’aménagement différé à caractère industriel")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="za",title=u"zone agricole")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zf",title=u"zone forestière")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zev",title=u"zone d’espaces verts")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zn",title=u"zone naturelle")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zp",title=u"zone de parc")

            #add investigation articles folder
            #this is done by a method because the migrateBuildLicencesInvestigationArticles
            #migration step will use it too
            addInvestigationArticles(context, configFolder)

            #add RoadCoatings folder
            newFolderid = configFolder.invokeFactory("Folder",id="folderroadcoatings",title=service.translate("urban","folderroadcoatings_folder_title",context=site,default="FolderRoadCoatings"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="filetseau",title=u"Filets d'eau")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="bordures",title=u"Bordures")

            #add Makers folder
            newFolderid = configFolder.invokeFactory("Folder",id="foldermakers",title=service.translate("urban","foldermakers_folder_title",context=site,default="FolderMakers"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="spw-dgo1",title=u"SPW-DGO1", description=u'<p>Direction Générale opérationnelle<br />Département du réseau de Namur et du Luxembourg<br />District 131.12 - SPY<br />37, Route de Saussin<br />5190 Spy</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="dgrne",title=u"DGRNE", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="dnf",title=u"DNF", description=u'<p>39, Avenue Reine Astrid<br />5000 Namur</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="stp",title=u"Service Technique Provincial", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="pi",title=u"Prévention Incendie", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="bec",title=u"Bureau d'études communal", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="svp",title=u"Service Voyer Principal", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="agriculture",title=u"Agriculture", description=u'<p>Direction Générale opérationnelle<br />Agriculture, Ressources naturelles et Environnement<br />Service extérieur de Wavre<br />4, Avenue Pasteur<br />1300 Wavre</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="pn",title=u"Parc Naturel", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="crmsf",title=u"Commission Royale des Monuments, Sites et Fouilles", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="swde",title=u"SWDE", description=u'<p>14, Rue Joseph Saintraint<br />5000 Namur</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="ccatm",title=u"CCATM", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="inasep",title=u"INASEP", description=u'<p>1b, Rue des Viaux<br />5100 Naninne</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="belgacom",title=u"Belgacom", description=u'<p>60, Rue Marie Henriette<br />5000 Namur</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="spge",title=u"SPGE", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="cibe",title=u"CIBE/Vivaqua", description=u'<p>70, Rue aux Laines<br />1000 Bruxelles</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="sncb",title=u"SNCB", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="infrabel",title=u"Infrabel", description=u'<p>Infrastructure ferroviaire<br />2/003, Place des Guillemins<br />4000 Liège</p>')
            newFolder.invokeFactory("UrbanVocabularyTerm",id="voo",title=u"VOO", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')

            #add Delays folder
            newFolderid = configFolder.invokeFactory("Folder",id="folderdelays",title=service.translate("urban","folderdelays_folder_title",context=site,default="FolderDelays"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanDelay'])
            newFolder.setImmediatelyAddableTypes(['UrbanDelay'])
            newFolder.invokeFactory("UrbanDelay",id="30j",title=u"30 jours (article 107§1 / article 264)", deadLineDelay=30, alertDelay=20)
            newFolder.invokeFactory("UrbanDelay",id="70j",title=u"70 jours (article 107§1 / article 264)", deadLineDelay=70, alertDelay=20)
            newFolder.invokeFactory("UrbanDelay",id="75j",title=u"75 jours (article 107§2)", deadLineDelay=75, alertDelay=20)
            newFolder.invokeFactory("UrbanDelay",id="115j",title=u"115 jours (article 107§2)", deadLineDelay=115, alertDelay=20)
            newFolder.invokeFactory("UrbanDelay",id="art127",title=u"Article 127", deadLineDelay=0, alertDelay=20)
            newFolder.invokeFactory("UrbanDelay",id="inconnu",title=u"Inconnu", deadLineDelay=0, alertDelay=20)

            #add the derogations folder
            newFolderid = configFolder.invokeFactory("Folder",id="derogations",title=service.translate("urban","derogations_folder_title",context=site,default="Derogations"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="dero-ps",title=u"au Plan de secteur")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="dero-pca",title=u"au Plan Communal d'Aménagement")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="dero-rru",title=u"au Règlement Régional d'Urbanisme")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="dero-rcu",title=u"au Règlement Communal d'Urbanisme")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="dero-lot",title=u"au Lotissement")

            #add BuildWorkTypes folder
            newFolderid = configFolder.invokeFactory("Folder",id="folderbuildworktypes",title=service.translate("urban","folderbuildworktype_folder_title",context=site,default="FolderBuildWorkType"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="ncmu",title=u"Nouvelle construction - Maison unifamiliale")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="ncia",title=u"Nouvelle construction - Immeuble appartements")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="nca",title=u"Nouvelle construction - Autres")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="tmu",title=u"Transformation - maison unifamiliale")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="tia",title=u"Transformation - immeuble appartements")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="tab",title=u"Transformation - autre bâtiment")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="dg",title=u"Démolition - Général")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="lg",title=u"Lotissement - Général")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="tnbg",title=u"Transformation Non-bâti - Général")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="td",title=u"Taudis")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="integration",title=u"Intégration dans voirie publique")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="leasing",title=u"Leasing (pour mémoire SPF Finances)")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="autres",title=u"Autres")

            #add pashs folder
            newFolderid = configFolder.invokeFactory("Folder",id="pashs",title=service.translate("urban","pashs_folder_title",context=site,default="PASH"))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-epuration-collective",title=u"Zone d'épuration collective")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-transitoire",title=u"Zone transitoire")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-epuration-individuelle",title=u"Zone d'épuration individuelle")

def addInvestigationArticles(context, configFolder):
    """
      This method add default investigation articles
    """
    site = context.getSite()
    newFolderid = configFolder.invokeFactory("Folder",id="investigationarticles",title=service.translate("urban","investigationarticles_folder_title",context=site,default="Investigation articles"))
    newFolder = getattr(configFolder, newFolderid)
    newFolder.setConstrainTypesMode(1)
    newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
    newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-1",title=u"330 1°",description="<p>« la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins quatre niveaux ou douze mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-2",title=u"330 2°",description="<p>« (la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l’alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l’alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës – AGW du 23 décembre 1998, art 1er), la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-3",title=u"330 3°",description="<p> « la construction, la reconstruction d’un magasin ou la modification de la destination d’un bâtiment en magasin dont la surface nette de vente est supérieure à 400 m&sup2; ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-4",title=u"330 4°",description="<p> « la construction, la reconstruction de bureaux ou la modification de la destination d’un bâtiment en bureaux dont la superficie des planchers est supérieure à 650 m&sup2; ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-5",title=u"330 5°",description="<p> « la construction, la reconstruction ou la modification de la destination d’un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à 400 m&sup2; ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-6",title=u"330 6°",description="<p> « l’utilisation habituelle d’un terrain pour le dépôt d’un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-7",title=u"330 7°",description="<p> « les demandes de permis de lotir ou de permis d’urbanisme relatives à des constructions groupées visées à l’article 126 qui portent sur une superficie de 2 hectares et plus »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-8",title=u"330 8°",description="<p> « les demandes de permis de lotir ou de permis d’urbanisme relatives à des constructions groupées visées à l’article 126 qui peuvent comporter un ou plusieurs bâtiments visés aux 1°, 2°,3°, 4° et 5° »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-9",title=u"330 9°",description="<p> « les demandes de permis de lotir ou de permis d’urbanisme visées à l’article 128 »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-10",title=u"330 10°",description="<p> « les demandes de permis de lotir visées à l’article 97 »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-11",title=u"330 11°",description="<p> « les demandes de permis de lotir ou de permis d’urbanisme impliquant l’application des articles 110 à 113 »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-12",title=u"330 12°",description="<p> « les demandes de permis de lotir et les demandes de permis d’urbanisme relatives à la construction, la reconstruction ou la transformation d’un bâtiment qui se rapportent à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protection visée à l’article 205 (lire article 209) ou localisés dans un site mentionné à l’atlas visé à l’article 215 (lire article 233) »</p>")
    newFolder.invokeFactory("UrbanVocabularyTerm",id="330-13",title=u"330 13°",description="<p>« les voiries publiques de la Région classées en réseau interurbain (RESI) par l’arrêté ministériel du 11 août 1994. »</p>")

def addUrbanGroups(context):
    """
       Add a group of 'urban' application users... 
    """
    site = context.getSite()
    #add 2 groups
    #one with urban Readers
    site.portal_groups.addGroup("urban_readers", title="Urban Readers")
    #one with urban Editors
    site.portal_groups.addGroup("urban_editors", title="Urban Editors")

def setDefaultApplicationSecurity(context):
    """
       Set sharing on differents folders to access the application 
    """
    #we have to :
    #give the Reader role to the urban_readers and urban_editors groups on 
    #portal_urban and application folders 
    #give the Editor role on urban application folders
    site = context.getSite()
    #portal_urban local roles
    site.portal_urban.manage_addLocalRoles("urban_readers", ("Reader",))
    site.portal_urban.manage_addLocalRoles("urban_editors", ("Reader",))

    #application folders local roles
    #global application folder : "urban_readers" and "urban_editors" can read...
    if hasattr(site, "urban"):
        app_folder = getattr(site, "urban")
        app_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        app_folder.manage_addLocalRoles("urban_editors", ("Reader",))
        #set some hardcoded permissions
        #sharing is only managed by the 'Managers'
        app_folder.manage_permission('Sharing page: Delegate roles', ['Manager', ], acquire=0)
        #hide the 'Properties' tab to other roles than 'Manager'
        app_folder.manage_permission('Manage properties', ['Manager', ], acquire=0)

    #buildlicences folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "buildlicences"):
        b_folder = getattr(app_folder, "buildlicences")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            b_folder.manage_addProperty('urbanConfigId', 'buildlicence', 'string')
        except BadRequest:
            pass
        b_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        b_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #parceloutlicences application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "parceloutlicences"):
        p_folder = getattr(app_folder, "parceloutlicences")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'parceloutlicence', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #declarations application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "declarations"):
        p_folder = getattr(app_folder, "declarations")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'declaration', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #division application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "divisions"):
        p_folder = getattr(app_folder, "divisions")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'division', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #urbancertificatesones application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "urbancertificateones"):
        p_folder = getattr(app_folder, "urbancertificateones")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'urbancertificateone', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #urbancertificatetwos application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "urbancertificatetwos"):
        p_folder = getattr(app_folder, "urbancertificatetwos")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'urbancertificatetwo', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #notaryletters application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "notaryletters"):
        p_folder = getattr(app_folder, "notaryletters")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'notaryletter', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #environmentaldeclarations folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "environmentaldeclarations"):
        p_folder = getattr(app_folder, "environmentaldeclarations")
        #we add a property usefull for portal_urban.getUrbanConfig
        try:
            #we try in case we apply the profile again...
            p_folder.manage_addProperty('urbanConfigId', 'environmentaldeclaration', 'string')
        except BadRequest:
            pass
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #architects application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "architects"):
        p_folder = getattr(app_folder, "architects")
        app_folder.manage_permission('Add portal content', ['Manager', 'Contributor', 'Owner', 'Editor', ], acquire=0)
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #geometricians application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "geometricians"):
        p_folder = getattr(app_folder, "geometricians")
        app_folder.manage_permission('Add portal content', ['Manager', 'Contributor', 'Owner', 'Editor', ], acquire=0)
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #notaries application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "notaries"):
        p_folder = getattr(app_folder, "notaries")
        app_folder.manage_permission('Add portal content', ['Manager', 'Contributor', 'Owner', 'Editor', ], acquire=0)
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))

def addGlobalFolders(context):
    """
    Add folders with properties used by several licence types
    """
    site = context.getSite()
    tool = site.portal_urban

    #add global topics
    #a criterion can have 4 values if necessary
    topicsInfo = (
    # Last elements
    # displays the last elements at the root of the application (urban)
    ( 'search-last-elements',
    (  ('Type', 'ATPortalTypeCriterion', URBAN_TYPES, ''),
       ('path', 'ATPathCriterion', '', True),
    ), None, ['Title', 'CreationDate', 'Creator']
    ),
    # Architects
    # this will be used in the architects_folder_view
    ( 'searcharchitects',
    (  ('Type', 'ATPortalTypeCriterion', ['Architect',], ''),
    ), None, ['Title', 'Creator']
    ),
    # Geometricians
    # this will be used in the geometricians_folder_view
    ( 'searchgeometricians',
    (  ('Type', 'ATPortalTypeCriterion', ['Geometrician',], ''),
    ), None, ['Title', 'Creator']
    ),
    # Notariespersons_t
    # this will be used in the notaries_folder_view
    ( 'searchnotaries',
    (  ('Type', 'ATPortalTypeCriterion', ['Notary',], ''),
    ), None, ['Title', 'Creator']
    ),
    # Existing parcels
    ( 'searchportionsout',
    (  ('Type', 'ATPortalTypeCriterion', ['PortionOut',], ''),
       ('path', 'ATPathCriterion', '', False),
    ), None, ['Title', 'CreationDate', 'Creator']
    ),
    # Folder events
    ( 'searchurbanevents',
    (  ('Type', 'ATPortalTypeCriterion', ['UrbanEvent',], ''),
       ('path', 'ATPathCriterion', '', False),
    ), None, ['Title', 'getBeginDate', 'getEndDate', 'Creator']
    ),
    # Lots
    ( 'searchlots',
    (  ('Type', 'ATPortalTypeCriterion', ['Lot',], ''),
       ('path', 'ATPathCriterion', '', False),
    ), None, ['Title', 'Creator']
    ),
    # Equipments
    ( 'searchequipments',
    (  ('Type', 'ATPortalTypeCriterion', ['Equipment',], ''),
       ('path', 'ATPathCriterion', '', False),
    ), None, ['Title', 'Creator']
    ),
    # Linked documents
    ( 'searchlinkeddocuments',
    (  ('Type', 'ATPortalTypeCriterion', ['File',], ''),
       ('path', 'ATPathCriterion', '', False),
    ), None, ['Title', 'CreationDate', 'Creator']
    ),
    )

    if not hasattr(tool, "topics"):
        topicsFolderId = tool.invokeFactory("Folder",id="topics",title=service.translate("urban","topics",context=site,default="Topics"))
        topicsFolder = getattr(tool, topicsFolderId)
        #restrict the addable types to "ATTopic"
        #Add these searches for portal_urban
        topicsFolder.setConstrainTypesMode(1)
        topicsFolder.setLocallyAllowedTypes(['Topic'])
        topicsFolder.setImmediatelyAddableTypes(['Topic'])
    else:
        topicsFolder = getattr(tool, "topics")
    for topicId, topicCriteria, stateValues, topicViewFields in topicsInfo:
        if hasattr(topicsFolder, topicId):
            continue
        topicsFolder.invokeFactory('Topic', topicId)
        topic = getattr(topicsFolder, topicId)
        topic.setExcludeFromNav(True)
        topic.setTitle(topicId)
        for criterionName, criterionType, criterionValue, criterionExtraValue in topicCriteria:
            criterion = topic.addCriterion(field=criterionName,
                                            criterion_type=criterionType)
            criterion.setValue(criterionValue)
            #define if the ATPathCriterion must search into subfolders
            if criterionType == 'ATPathCriterion':
                criterion.setRecurse(criterionExtraValue)
            #add a property defining if the topic is relative to a BuildLicence or a ParcelOutLicence or a PortionOut
            if criterionType == 'ATPortalTypeCriterion':
                topic.manage_addProperty(TOPIC_TYPE, criterionValue, 'string')
        #add a review_state criterion if needed...
        if stateValues:
            stateCriterion = topic.addCriterion(field='review_state', criterion_type='ATListCriterion')
            stateCriterion.setValue(stateValues)
        topic.setTitle(service.translate("urban",topicId,context=site,default=topicId))
        topic.setLimitNumber(True)
        topic.setItemCount(20)
        #set the sort criterion as reversed
        if topicId in ['searcharchitects', 'searchgeometricians', 'searchnotaries', ]:
            #these topics are used for showing things
            topic.setSortCriterion('sortable_title', False)
        else:
            topic.setSortCriterion('created', True)
        topic.setCustomView(True)
        topic.setCustomViewFields(topicViewFields)
        topic.reindexObject()

    #add the pcas folder
    if not hasattr(tool, "pcas"):
        newFolderid = tool.invokeFactory("Folder",id="pcas",title=service.translate("urban","pcas_folder_title",context=site,default="PCAs"))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['PcaTerm'])
        newFolder.setImmediatelyAddableTypes(['PcaTerm'])
        newFolder.invokeFactory("PcaTerm",id="pca1",label=u"Plan communal d'aménagement 1", number='1', decreeDate="2009/01/01", decreeType="royal")
        newFolder.invokeFactory("PcaTerm",id="pca2",label=u"Plan communal d'aménagement 2", number='2', decreeDate="2008/06/23", decreeType="royal")
        newFolder.invokeFactory("PcaTerm",id="pca3",label=u"Plan communal d'aménagement 3", number='3', decreeDate="2001/12/13", decreeType="departmental")

    #add the parcelling folder
    if not hasattr(tool, "parcellings"):
        newFolderid = tool.invokeFactory("Folder",id="parcellings",title=service.translate("urban","parcellings_folder_title",context=site,default="Parcellings"))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['ParcellingTerm'])
        newFolder.setImmediatelyAddableTypes(['ParcellingTerm'])
        newFolder.invokeFactory("ParcellingTerm",id="p1",title=u"Lotissement 1 (André Ledieu - 01/01/2005 - 10)", label="Lotissement 1", subdividerName="André Ledieu", authorizationDate="2005/01/01", numberOfParcels=10)
        newFolder.invokeFactory("ParcellingTerm",id="p2",title=u"Lotissement 2 (Ets Tralala - 01/06/2007 - 8)", label="Lotissement 2", subdividerName="Ets Tralala", authorizationDate="2007/06/01", numberOfParcels=8)
        newFolder.invokeFactory("ParcellingTerm",id="p3",title=u"Lotissement 3 (SPRL Construction - 02/05/2001 - 15)", label="Lotissement 3", subdividerName="SPRL Construction", authorizationDate="2001/05/02", numberOfParcels=15)

    #add the streets folder
    if not hasattr(tool, "streets"):
        newFolderid = tool.invokeFactory("Folder",id="streets",title=service.translate("urban","streets_folder_title",context=site,default="Streets"))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['City'])
        newFolder.setImmediatelyAddableTypes(['City'])

    #add the additional_layers folder
    if not hasattr(tool, "additional_layers"):
        newFolderid = tool.invokeFactory("Folder",id="additional_layers",title=service.translate("urban","additonal_layers_folder_title",context=site,default="Additional layers"))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['Layer'])
        newFolder.setImmediatelyAddableTypes(['Layer'])
        #additional layers are added in the extra step "setupExtra"

    #add the persons_titles folder
    if not hasattr(tool, "persons_titles"):
        newFolderid = tool.invokeFactory("Folder",id="persons_titles",title=service.translate("urban","persons_titles_folder_title",context=site,default="Persons titles"))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])        
        newFolder.invokeFactory("UrbanVocabularyTerm",id="notitle",title=u"")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="madam",title=u"Madame")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="miss",title=u"Mademoiselle")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="mister",title=u"Monsieur")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="madam_and_mister",title=u"Monsieur et Madame")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="master",title=u"Maître")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="masters",title=u"Maîtres")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="misters",title=u"Messieurs")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ladies",title=u"Mesdames")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="consorts",title=u"Consorts")

    #add the persons_grades folder
    if not hasattr(tool, "persons_grades"):
        newFolderid = tool.invokeFactory("Folder",id="persons_grades",title=service.translate("urban","persons_grades_folder_title",context=site,default="Persons grades"))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])        
        newFolder.invokeFactory("UrbanVocabularyTerm",id='agent-accueil', title="Agent d'accueil"),
        newFolder.invokeFactory("UrbanVocabularyTerm",id='agent-administratif', title="Agent administratif"),
        newFolder.invokeFactory("UrbanVocabularyTerm",id='agent-technique', title="Agent technique"),
        newFolder.invokeFactory("UrbanVocabularyTerm",id='agent-traitant', title="Agent traitant"),
        newFolder.invokeFactory("UrbanVocabularyTerm",id='directeur-administratif', title="Directeur administratif"),
        newFolder.invokeFactory("UrbanVocabularyTerm",id='directeur-general', title="Directeur général"),
        newFolder.invokeFactory("UrbanVocabularyTerm",id='directeur-technique', title="Directeur technique"),
        newFolder.invokeFactory("UrbanVocabularyTerm",id='reponsable', title="Responsable du Service Urbanisme"),
        newFolder.invokeFactory("UrbanVocabularyTerm",id='responsable-accueil', title="Responsable d'accueil"),
        newFolder.invokeFactory("UrbanVocabularyTerm",id='responsable-administratif', title="Responsable administratif"),
        newFolder.invokeFactory("UrbanVocabularyTerm",id='responsable-technique', title="Responsable technique"),

    #add the decisions folder
    if not hasattr(tool, "decisions"):
        newFolderid = tool.invokeFactory("Folder",id="decisions",title=service.translate("urban","decisions_folder_title",context=site,default="Decisions"))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])        
        newFolder.invokeFactory("UrbanVocabularyTerm",id="favorable",title=u"Favorable")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="defavorable",title=u"Défavorable")

def addUrbanConfigsTopics(context):
    """
      Add the default topics of every urbanConfig
    """
    site = context.getSite()
    tool = site.portal_urban

    for urban_type in URBAN_TYPES:
        if not hasattr(tool, urban_type.lower()):
            continue
        urbanConfig = getattr(tool, urban_type.lower())
        topicsInfo = (
        #this will be used in the urban_view
        # Portlet search "every licences"
        ( 'searchalllicences',
        (  ('Type', 'ATPortalTypeCriterion', urban_type),
           ('path', 'ATPathCriterion', ''),
        ), None, ['Title', 'CreationDate', 'Creator']
        ),
        # Portlet search "in_progress licences"
        ( 'searchinprogresslicences',
        (  ('Type', 'ATPortalTypeCriterion', urban_type),
           ('path', 'ATPathCriterion', ''),
        ), ('in_progress', ), ['Title', 'CreationDate', 'Creator']
        ),
        # Portlet search "retired licences"
        ( 'searchretiredlicences',
        (  ('Type', 'ATPortalTypeCriterion', urban_type),
           ('path', 'ATPathCriterion', ''),
        ), ('retired', ), ['Title', 'CreationDate', 'Creator']
        ),
        # Portlet search "incomplete licences"
        ( 'searchincompletelicences',
        (  ('Type', 'ATPortalTypeCriterion', urban_type),
           ('path', 'ATPathCriterion', ''),
        ), ('incomplete', ), ['Title', 'CreationDate', 'Creator']
        ),
        # Portlet search "accepted licences"
        ( 'searchacceptedlicences',
        (  ('Type', 'ATPortalTypeCriterion', urban_type),
           ('path', 'ATPathCriterion', ''),
        ), ('accepted', ), ['Title', 'CreationDate', 'Creator']
        ),
        # Portlet search "refused licences"
        ( 'searchrefusedlicences',
        (  ('Type', 'ATPortalTypeCriterion', urban_type),
           ('path', 'ATPathCriterion', ''),
        ), ('refused', ), ['Title', 'CreationDate', 'Creator']
        ),
        )
        if not "topics" in urbanConfig.objectIds():
            topicsFolderId = urbanConfig.invokeFactory("Folder",id="topics",title=service.translate("urban","topics",context=site,default="Topics"))
            topicsFolder = getattr(urbanConfig, topicsFolderId)
            #restrict the addable types to "ATTopic"
            #Add these searches by meeting config
            topicsFolder.setConstrainTypesMode(1)
            topicsFolder.setLocallyAllowedTypes(['Topic'])
            topicsFolder.setImmediatelyAddableTypes(['Topic'])
            for topicId, topicCriteria, stateValues, topicViewFields in topicsInfo:
                topicsFolder.invokeFactory('Topic', topicId)
                topic = getattr(topicsFolder, topicId)
                topic.setExcludeFromNav(True)
                topic.setTitle(topicId)
                for criterionName, criterionType, criterionValue in topicCriteria:
                    criterion = topic.addCriterion(field=criterionName,
                                                    criterion_type=criterionType)
                    criterion.setValue([criterionValue])
                    #add a property defining if the topic is relative to a BuildLicence or a ParcelOutLicence or a PortionOut
                    if criterionType == 'ATPortalTypeCriterion':
                        topic.manage_addProperty(TOPIC_TYPE, criterionValue, 'string')
                #add a review_state criterion if needed...
                if stateValues:
                    stateCriterion = topic.addCriterion(field='review_state', criterion_type='ATListCriterion')
                    stateCriterion.setValue(stateValues)
                topic.setTitle(service.translate("urban","%s_%s"% (urban_type.lower(), topicId),context=site,default=topicId))
                topic.setLimitNumber(True)
                topic.setItemCount(20)
                #set the sort criterion as reversed
                topic.setSortCriterion('created', True)
                topic.setCustomView(True)
                topic.setCustomViewFields(topicViewFields)
                topic.reindexObject()

def adaptDefaultPortal(context):
    """
       Adapt some properties of the portal
    """
    #deactivate tabs auto generation in navtree_properties
    site = context.getSite()
    site.portal_properties.site_properties.disable_folder_sections = True
    #remove default created objects like events, news, ...
    try:
        site.manage_delObjects(ids=['events', ])
    except AttributeError:
        #the 'events' object does not exist...
        pass
    try:
        site.manage_delObjects(ids=['news', ])
    except AttributeError:
        #the 'news' object does not exist...
        pass

    #change the content of the front-page
    try:
        frontpage = getattr(site, 'front-page')
        frontpage.setTitle(service.translate("urban","front_page_title",context=site,default="urban"))
        frontpage.setDescription(service.translate("urban","front_page_descr",context=site,default="urban"))
        frontpage.setText(service.translate("urban","front_page_text",context=site,default="urban"))
        frontpage.reindexObject()
    except AttributeError:
        #the 'front-page' object does not exist...
        pass

    #hide de sendto action
    #set visible = 0
    site.portal_actions.document_actions.sendto.manage_changeProperties(visible = False)

def addApplicationFolders(context):
    """
    Add the application folders like 'urban' and 'architects' 
    """
    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')

    if not hasattr(aq_base(site), "urban"):
        newFolderid = site.invokeFactory("Folder",id="urban",title=service.translate("urban","urban",context=site,default="urban"))
        newFolder = getattr(site, newFolderid)
        newFolder.setLayout('urban_view')
    else:
        newFolder = getattr(site, 'urban')

    for urban_type in URBAN_TYPES:
        if not hasattr(newFolder, urban_type.lower() + 's'):
            site.portal_types["Large Plone Folder"].global_allow = 1
            newFolderid = newFolder.invokeFactory("Large Plone Folder",id=urban_type.lower() + 's',title=service.translate("urban",urban_type.lower() + 's',context=site,default=urban_type.lower() + 's'))
            site.portal_types["Large Plone Folder"].global_allow = 0
            newSubFolder = getattr(newFolder, newFolderid)
            newSubFolder.setConstrainTypesMode(1)
            newSubFolder.setLocallyAllowedTypes([urban_type])
            newSubFolder.setImmediatelyAddableTypes([urban_type])
            #set the layout to "urban_view"
            newSubFolder.setLayout('urban_view')
            #manage the 'Add' permissions...
            try:
                newSubFolder.manage_permission('urban: Add %s' % urban_type, ['Manager', 'Editor', ], acquire=0)
            except ValueError:
                #exception for some portal_types having a different meta_type
                if urban_type in ['UrbanCertificateOne', 'NotaryLetter', ]:
                    newSubFolder.manage_permission('urban: Add UrbanCertificateBase', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains architects
    if not hasattr(newFolder, "architects"):
        newFolderid = newFolder.invokeFactory("Folder",id="architects",title=service.translate("urban","architects_folder_title",context=site,default="Architects"))
        newSubFolder = getattr(newFolder, newFolderid)
        newSubFolder.setConstrainTypesMode(1)
        newSubFolder.setLocallyAllowedTypes(['Architect'])
        newSubFolder.setImmediatelyAddableTypes(['Architect'])
        newSubFolder.setLayout('architects_folder_view')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Architect', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains geometricians
    if not hasattr(newFolder, "geometricians"):
        newFolderid = newFolder.invokeFactory("Folder",id="geometricians",title=service.translate("urban","geometricians_folder_title",context=site,default="Geometricians"))
        newSubFolder = getattr(newFolder, newFolderid)
        newSubFolder.setConstrainTypesMode(1)
        newSubFolder.setLocallyAllowedTypes(['Geometrician'])
        newSubFolder.setImmediatelyAddableTypes(['Geometrician'])
        newSubFolder.setLayout('geometricians_folder_view')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Geometrician', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains notaries
    if not hasattr(newFolder, "notaries"):
        newFolderid = newFolder.invokeFactory("Folder",id="notaries",title=service.translate("urban","notaries_folder_title",context=site,default="Notaries"))
        newSubFolder = getattr(newFolder, newFolderid)
        newSubFolder.setConstrainTypesMode(1)
        newSubFolder.setLocallyAllowedTypes(['Notary'])
        newSubFolder.setImmediatelyAddableTypes(['Notary'])
        newSubFolder.setLayout('notaries_folder_view')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Contact', ['Manager', 'Editor', ], acquire=0)

    #add default links to searches
    search_links = [('searchbyparcel', 'urban_searchbyparcel'), ('searchbyapplicant', 'urban_searchbyapplicant?foldertypes=BuildLicence&foldertypes=Declaration&foldertypes=ParcelOutLicence'), ('searchbystreet', 'urban_searchbystreet?foldertypes=BuildLicence&foldertypes=Declaration&foldertypes=ParcelOutLicence'), ]
    for search_link in search_links:
        if not hasattr(newFolder, search_link[0]):
            #add a link and translate his title
            linkId = newFolder.invokeFactory("Link",id=search_link[0],title=service.translate("urban",'urban_%s_descr' % search_link[0],context=site,default=search_link[0]), remoteUrl=search_link[1])

def addTestObjects(context):
    """
       Add some users and objects for test purpose...
    """
    if context.readDataFile('urban_tests_marker.txt') is None:
        return

    #add some users, some architects and some foldermanagers...
    #add 2 users, one as reader and one as editor...
    site = context.getSite()

    try:
        site.portal_registration.addMember(id="urbanreader", password="urbanreader")
        site.portal_registration.addMember(id="urbaneditor", password="urbaneditor")
        #put users in the correct group
        site.acl_users.source_groups.addPrincipalToGroup("urbanreader", "urban_readers")
        site.acl_users.source_groups.addPrincipalToGroup("urbaneditor", "urban_editors")
    except:
        #if something wrong happens (one object already exists), we pass...
        pass

    #add some architects...
    urbanFolder = getattr(site, "urban")
    notFolder = getattr(urbanFolder, "architects")
    if not notFolder.objectIds():
        #create some architects using the Extensions.imports script
        from Products.urban.Extensions.imports import import_architects
        import_architects(context.getSite().portal_urban)

    #add some notaries...
    urbanFolder = getattr(site, "urban")
    notFolder = getattr(urbanFolder, "notaries")
    if not notFolder.objectIds():
        notFolder.invokeFactory("Notary",id="notary1",name1="NotaryName1", name2="NotarySurname1")
        notFolder.invokeFactory("Notary",id="notary2",name1="NotaryName2", name2="NotarySurname2")
        notFolder.invokeFactory("Notary",id="notary3",name1="NotaryName3", name2="NotarySurname3")
        logger.info("Notaries examples have been added")

    #add some geometricians...
    urbanFolder = getattr(site, "urban")
    geoFolder = getattr(urbanFolder, "geometricians")
    if not geoFolder.objectIds():
        geoFolder.invokeFactory("Geometrician",id="geometrician1",name1="GeometricianName1", name2="GeometricianSurname1")
        geoFolder.invokeFactory("Geometrician",id="geometrician2",name1="GeometricianName2", name2="GeometricianSurname2")
        geoFolder.invokeFactory("Geometrician",id="geometrician3",name1="GeometricianName3", name2="GeometricianSurname3")
        logger.info("Geometricians examples have been added")

    #add some folder managers in each urbanConfigs...
    urbanConfigIds = ['buildlicence', 'declaration', 'parceloutlicence', 'urbancertificateone', 'urbancertificatetwo', 'notaryletter', 'division', ]
    tool = site.portal_urban
    for urbanConfigId in urbanConfigIds:
        fmFolder = getattr(tool.getUrbanConfig(None, urbanConfigId=urbanConfigId), "foldermanagers")
        if not fmFolder.objectIds():
            fmFolder.invokeFactory("FolderManager",id="foldermanager1",name1="Dumont", name2="Jean", grade='agent-technique')
            fmFolder.invokeFactory("FolderManager",id="foldermanager2",name1="Schmidt", name2="Alain", grade='directeur-general')
            fmFolder.invokeFactory("FolderManager",id="foldermanager3",name1="Robert", name2="Patrick", grade='responsable-administratif')

    tool = site.portal_urban

    #create some streets using the Extensions.imports script
    if not tool.streets.objectIds('City'):
        from Products.urban.Extensions.imports import import_streets_fromfile
        import_streets_fromfile(tool)

    addUrbanEventTypes(context)

    #add some generic templates in configuration
    gen_temp = { 'templateHeader':'header.odt', 
                 'templateFooter':'footer.odt',
                 'templateReference':'reference.odt',
                 'templateSignatures':'signatures.odt',
                 'templateStatsINS':'statsins.odt'
                }

    for attribname in gen_temp.keys():
        try:
            fld = tool.getField(attribname)
            if not fld.getAccessor(tool)().size:
                filePath = '%s/templates/%s' % (context._profile_path, gen_temp[attribname])
                fileDescr = file(filePath, 'rb')
                fileContent = fileDescr.read()
                fld.getMutator(tool)(fileContent)
                fileDescr.close()
                fld.setContentType(tool, "application/vnd.oasis.opendocument.text")
                fld.setFilename(tool, gen_temp[attribname])
                logger.info("Generic template '%s' added: '%s'"%(attribname, gen_temp[attribname]))
        except IOError, msg:
            logger.error("Cannot open the file '%s': %s" %(filePath, msg))
        except Exception, msg:
            logger.warn("An error occured while processing the tool '%s' attribute: %s" % (attribname,msg))

def addUrbanEventTypes(context):
    """
      Helper method for easily adding urbanEventTypes
    """
    #add some UrbanEventTypes...
    #get the urbanEventTypes dict from the profile
    #get the name of the profile by taking the last part of the _profile_path
    profile_name = context._profile_path.split('/')[-1]
    from_string = "from Products.urban.profiles.%s.data import urbanEventTypes" % profile_name
    try:
        exec(from_string)
    except ImportError:
        return
    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')
    #add the UrbanEventType
    for urbanConfigId in urbanEventTypes:
        try:
            uetFolder = getattr(tool.getUrbanConfig(None, urbanConfigId=urbanConfigId), "urbaneventtypes")
        except AttributeError:
            #if we can not get the urbanConfig, we pass this one...
            logger.warn("An error occured while trying to get the '%s' urbanConfig" % urbanConfigId)
            continue
        for uet in urbanEventTypes[urbanConfigId]:
            try:
                loginfo = 'unknown'
                id = uet['id']
                loginfo = id
                #we pass every informations including the 'id' in the 'uet' dict
                newUetId = uetFolder.invokeFactory("UrbanEventType", **uet)
                newUet = getattr(uetFolder, newUetId)
                #add the Files in the UrbanEventType
                for template in uet['podTemplates']:
                    id = "%s.odt" % template['id']
                    loginfo = id
                    title = template['title']
                    filePath = '%s/templates/%s' % (context._profile_path, id)
                    fileDescr = file(filePath, 'rb')
                    fileContent = fileDescr.read()
                    newUetFileId = newUet.invokeFactory("File", id=id, title=title, file=fileContent)
                    newUetFile = getattr(newUet, newUetFileId)
                    newUetFile.setContentType("application/vnd.oasis.opendocument.text")
                    newUetFile.setFilename(id)
                    newUetFile.reindexObject()
            except Exception, msg:
                #there was an error, reinstalling?  reapplying?  we pass...
                logger.warn("An error occured while processing the '%s' UrbanEvent: '%s'" % (loginfo, msg))
                pass

def importStreets(context):
    #site = context.getSite()
    #cat = getToolByName(site, 'portal_catalog')
    #portal_url=getToolByName(site,'portal_url')
    #cities = [c.Title for c in cat(path=portal_url.getPortalPath()+'/portal_urban/streets/')]
    #streetsfolder=site.portal_urban.streets
    #filePath = '%s/streets.csv' % (context._profile_path)
    #fstreets=open (filePath,'r')
    #for line in fstreets.readlines():
    #    items=line.split(';')
    #    if not items[2] in cities:
    #        streetsfolder.invokeFactory("City",id=items[2].lower(),title=items[2],zipCode=items[1])
    #        cities = [c.Title for c in cat(path=portal_url.getPortalPath()+'/portal_urban/streets/')]
    #    cityfolder=getattr(streetsfolder,items[2].lower())
    #    newStreet=cityfolder.invokeFactory("Street",id=site.generateUniqueId('Street'),streetName=items[0],streetCode=items[3])
    #fstreets.close()
    pass

def setupExtra(context):
    if context.readDataFile('urban_extra_marker.txt') is None:
        return

    portal = context.getSite()

    #Setting the user password policy
    if portal.validate_email:
        portal.validate_email = False
        logger.info('user password policy, aka validate_email, set to False')
    else:
        logger.info('user password policy unchanged')

    #Configuring editor
    try:
        from Products.CPUtils.Extensions.utils import configure_fckeditor
        configure_fckeditor(portal, default=1, allusers=1, custom=1, nomerge=1)
        logger.info('FCKeditor installed, set by default and customised')
    except ImportError, msg:
        logger.info('Products CPUtils needeed to install and configure FCKeditor')

    #we add additional layers here because we take informations from portal_urban
    #that are set manually after install
    logger.info("Adding additional layers")
    portal_urban = getToolByName(portal, 'portal_urban')
    if not portal_urban:
        logger.error("Could not get the portal_urban tool!")
        return
    nis = portal_urban.getNISNum()
    if not nis:
        logger.error("No NIS defined in portal_urban!")
        return

    #we add the map coordinates
    if not portal_urban.getMapExtent() or portal_urban.getMapExtent().count(',') != 3:
        dic = portal_urban.queryDB("SELECT (Xmin(ext.extent) ||','|| Ymin(ext.extent)||','|| Xmax(ext.extent)||','|| Ymax(ext.extent)) as coord FROM (SELECT Extent(the_geom) FROM capa) AS ext;")
        if dic and dic[0].has_key('coord'):
            portal_urban.setMapExtent(dic[0]['coord'])

    if not hasattr(portal_urban, "additional_layers"):
        _ = service.translate
        logger.warning("No 'additonal_layers' folder found in portal_urban, we create it.")
        additional_layers_id = portal_urban.invokeFactory("Folder",id="additional_layers",title=service.translate("urban","additonal_layers_folder_title",context=portal,default="Additional layers"))
        additional_layers = getattr(portal_urban, additional_layers_id)
        additional_layers.setConstrainTypesMode(1)
        additional_layers.setLocallyAllowedTypes(['Layer'])
        additional_layers.setImmediatelyAddableTypes(['Layer'])        
    else:
        additional_layers = portal_urban.additional_layers

    if not hasattr(aq_base(additional_layers), 'ppnc'):
        if portal_urban.getMapExtent():
            (xmin, ymin, xmax, ymax) = portal_urban.getMapExtent().split(',')
            already_ppnc = False
            layers = PPNC_LAYERS.keys()
            layers.sort()
            for layer in layers:
                request = "SELECT Intersects(MakeBox2D(MakePoint(%f, %f),MakePoint(%f, %f)), MakeBox2D(MakePoint(%d,%d),MakePoint(%d,%d))) as intersect ;"%(float(xmin), float(ymin), float(xmax), float(ymax), PPNC_LAYERS[layer]['xmin'], PPNC_LAYERS[layer]['ymin'], PPNC_LAYERS[layer]['xmax'], PPNC_LAYERS[layer]['ymax'])
                dic = portal_urban.queryDB(request)
                if dic and dic[0].has_key('intersect') and dic[0]['intersect']:
                    if not already_ppnc:
                        additional_layers.invokeFactory("Layer", id="ppnc", title=u"PPNC", WMSUrl="http://cartopro1.wallonie.be/WMS/com.esri.wms.Esrimap/PPNC?", layers=layer, SRS="ESPG:31370", baseLayer=True)
                        already_ppnc = True
                        logger.info("Additional layer '%s' added with layer '%s'"%('ppnc', layer))
                    else:
                        logger.info("ALREADY found layer !")
                        additional_layers.invokeFactory("Layer", id=layer, title=layer.upper(), WMSUrl="http://cartopro1.wallonie.be/WMS/com.esri.wms.Esrimap/PPNC?", layers=layer, SRS="ESPG:31370", baseLayer=True)
                        additional_layers.ppnc.setTitle(additional_layers.ppnc.getLayers().upper())
                        additional_layers.ppnc.reindexObject()
                        logger.info("Additional layer '%s' added with layer '%s'"%(layer, layer))
                    
            if not hasattr(aq_base(additional_layers), 'ppnc'):
                logger.error("Additional layer '%s' added WITHOUT specific layer because no ppnc intersection found"%'ppnc')
                additional_layers.invokeFactory("Layer", id="ppnc", title=u"PPNC", WMSUrl="http://cartopro1.wallonie.be/WMS/com.esri.wms.Esrimap/PPNC?", layers='ppnc', SRS="ESPG:31370", baseLayer=True)
        else:
            logger.error("Additional layer '%s' not added because the mapExtent is not defined in portal_urban"%'ppnc')
    if not hasattr(aq_base(additional_layers), 'batiments'):
        additional_layers.invokeFactory("Layer",id="batiments",title=u"Bâtiments",layers="urban%s:cabu" % nis,SRS="ESPG:31370",transparent=True,visibility=True)
        logger.info("Additional layer '%s' added"%'batiments')
    if not hasattr(aq_base(additional_layers), 'num_maisons'):
        additional_layers.invokeFactory("Layer",id="num_maisons",title=u"N° de maison",layers="urban%s:canu" % nis,styles="HousesNum",SRS="ESPG:31370",transparent=True,visibility=True)
        logger.info("Additional layer '%s' added"%'num_maisons')

##/code-section FOOT
