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
from Acquisition import aq_base
from Products.urban.config import TOPIC_TYPE
from zExceptions import BadRequest
from Products.ZCatalog.Catalog import CatalogError
from Products.urban.config import URBAN_TYPES, PPNC_LAYERS
from Products.urban.interfaces import ILicenceContainer
from zope.interface import alsoProvides
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
from zope import event
from Products.Archetypes.event import ObjectInitializedEvent
from exportimport import addUrbanEventTypes
from exportimport import addGlobalTemplates
from Products.urban.utils import generatePassword
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
    typesToRegister = {
                       'Architect': 1,
                       'UrbanCertificateOne': 1,
                       'NotaryLetter': 1,
                       'Notary': 1,
                       'Proprietary': 1,
                       'Applicant': 1,
                       'Claimant': 1,
                      }
    alreadyRegTypes.update(typesToRegister)
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=alreadyRegTypes)

    #to be removed after deletion of class Architect
    architect_type = site.portal_types.Architect
    architect_type.content_meta_type = "Contact"
    architect_type.factory = "addContact"

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



##code-section FOOT
def _(msgid, domain, context):
    translation_domain = queryUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, target_language='fr', default='')

def addUrbanConfigs(context):
    """
      Add the different urban configs
    """
    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')

    for urban_type in URBAN_TYPES:
        licenceConfigId = urban_type.lower()
        if not hasattr(aq_base(tool), licenceConfigId):
            configFolderid = tool.invokeFactory("LicenceConfig",id=licenceConfigId,title=_("%s_urbanconfig_title" % urban_type.lower(), 'urban', context=site.REQUEST))
            configFolder = getattr(tool, configFolderid)
            configFolder.licence_portal_type = urban_type
            configFolder.setUsedAttributes(configFolder.listUsedAttributes().keys())
            configFolder.reindexObject()
        else:
            configFolder = getattr(tool, licenceConfigId)

        #we just created the urbanConfig, proceed with other parameters...
        #parameters for every LicenceConfigs
        #add UrbanEventTypes folder
        if not hasattr(aq_base(configFolder), 'urbaneventtypes'):
            newFolderid = configFolder.invokeFactory("Folder",id="urbaneventtypes",title=_("urbaneventtypes_folder_title", 'urban', context=site.REQUEST))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanEventType'])
            newFolder.setImmediatelyAddableTypes(['UrbanEventType'])

        #add TownshipFolderCategories folder
        if not hasattr(aq_base(configFolder), 'townshipfoldercategories'):
            newFolderid = configFolder.invokeFactory("Folder",id="townshipfoldercategories",title=_("townshipfoldercategories_folder_title", 'urban', context=site.REQUEST))
            newFolder = getattr(configFolder, newFolderid)
            newFolder.setConstrainTypesMode(1)
            newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
            newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
            newFolder.invokeFactory("UrbanVocabularyTerm",id="abattre",title=u"Abattre")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="abri-animaux",title=u"Abri pour animaux")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="abri-jardin",title=u"Abri de jardin")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="car-port",title=u"Car-port")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="changement-de-destination",title=u"Changement de destination")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="clotures-murs",title=u"Clôtures et murs")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="commerce",title=u"Commerce")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="demolition",title=u"Démolition")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="divers",title=u"Divers")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="enseigne",title=u"Enseigne")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="immeuble-appartements",title=u"Construction d'un immeuble à appartements")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="modification-relief",title=u"Modification du relief du sol")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="module-electrite",title=u"Modules de production d'électricité ou de chaleur")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="nouvelle-habitation",title=u"Construction d'une nouvelle habitation")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="nouveau-logement",title=u"Création d'un nouveau logement dans un bâtiment existant")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="parking",title=u"Parking")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="piscine",title=u"Piscine")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="recouvrement-toiture",title=u"Remplacement de parement de façade ou de recouvrement de toiture")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="transformation",title=u"Transformation d'une habitation existante")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="transformation-facade",title=u"Transformation d'une façade")
            newFolder.invokeFactory("UrbanVocabularyTerm",id="veranda",title=u"Véranda")

        #add FolderCategories folder
        if urban_type in ['BuildLicence', 'ParcelOutLicence', 'UrbanCertificateOne', 'UrbanCertificateTwo', 'Declaration']:
            if not hasattr(aq_base(configFolder), 'foldercategories'):
                newFolderid = configFolder.invokeFactory("Folder",id="foldercategories",title=_("foldercategories_folder_title", 'urban', context=site.REQUEST))
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
                elif urban_type in ['ParcelOutLicence', ]:
                    #categories for ParcelOutLicences
                    newFolder.invokeFactory("UrbanVocabularyTerm",id="lap",title=u"LAP (permis de lotir avec avis préalable du FD)")
                    newFolder.invokeFactory("UrbanVocabularyTerm",id="lapm",title=u"LAP/M (modification du permis de lotir avec avis du FD)")
                    newFolder.invokeFactory("UrbanVocabularyTerm",id="ldc",title=u"LDC (permis de lotir dans un PCA, lotissement ou en décentralisation)")
                    newFolder.invokeFactory("UrbanVocabularyTerm",id="ldcm",title=u"LDC/M (modification du permis de lotir dans un PCA, RCU, LOTISSEMENT)")
                #categories for UrbanCertificateOnes
                elif urban_type in ['UrbanCertificateOne', ]:
                    newFolder.invokeFactory("UrbanVocabularyTerm",id="cu1",title=u"CU1 (certificat d'urbanisme 1)")
                #categories for UrbanCertificateTwos
                elif urban_type in ['UrbanCertificateTwo', ]:
                    newFolder.invokeFactory("UrbanVocabularyTerm",id="cu2",title=u"CU2 (certificat d'urbanisme 2)")
                #categories for Declarations
                elif urban_type in ['Declaration', ]:
                        newFolder.invokeFactory("UrbanVocabularyTerm",id="dup",title=u"DUP (Déclaration Urbanistique Préalable)")

        if urban_type == 'ParcelOutLicence':
            if not hasattr(aq_base(configFolder), 'lotusages'):
                newFolderid = configFolder.invokeFactory("Folder",id="lotusages",title=_("lotusages_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                newFolder.setConstrainTypesMode(1)
                newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
                newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
                newFolder.invokeFactory("UrbanVocabularyTerm",id="buildable",title=u"Lot bâtissable")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="greenzone",title=u"Espace vert")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="tosurrendertotown",title=u"Lot à rétrocéder à la commune")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="autre",title=u"Autre")
            if not hasattr(aq_base(configFolder), 'equipmenttypes'):
                newFolderid = configFolder.invokeFactory("Folder",id="equipmenttypes",title=_("folderequipmenttypes_folder_title", 'urban', context=site.REQUEST))
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
            if not hasattr(aq_base(configFolder), 'specificfeatures'):
                newFolderid = configFolder.invokeFactory("Folder",id="specificfeatures",title=_("urban_label_specificFeatures", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                newFolder.setConstrainTypesMode(1)
                newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
                newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
                newFolder.invokeFactory("UrbanVocabularyTerm",id="schema-developpement-espace-regional",title=u"Option particulière du schéma de développement de l'espace régional", description="<p>fait l'objet d'une option particulière du schéma de développement de l'espace régional, à savoir ...;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="situe-en-zone",title=u"Situé en Zone [...]", description="<p>est situé en ZONE XXX au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="plan-de-secteur",title=u"Plan de secteur", description="<p>est situé - dans un périmètre ... - en zone ... au projet - de révision du - de - plan de secteur de ... adopté par ... du ...;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="plan-communal-ammenagement",title=u"En Plan Communal d'Aménagement", description="<p>est situé en zone ... dans le périmètre du plan communal d'aménagement ... approuvé par ... du ... et qui n'a pas cessé de produire ses effets pour le bien précité;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="plan-communal-ammenagement-revision",title=u"En Plan Communal d'Aménagement (révision)", description="<p>est situé en zone ... dans le périmètre du projet - de révision du - de - plan communal d'aménagement ... approuvé par ... du ...;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="perimetre-lotissement",title=u"Dans un lot dans le périmètre d'un lotissement", description="<p>est situé sur le lot n° ... dans le périmètre du lotissement ... non périmé autorisé par ... du ...;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc",title=u"Schéma de structure communal", description="<p> est situé en zone ... au schéma de structure communal adopté par ... du ...;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-revision",title=u"Schéma de structure communal (révision)", description="<p> est situé en zone ... au projet de - révision du - de - schéma de structure communal adopté par ... du ...;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="rcu",title=u"Règlement communal d'urbanisme", description="<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme ... est applicable;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="rcu-approuve",title=u"Règlement communal d'urbanisme (approuvé)", description="<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé par ... du ... est applicable;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="rcu-revision",title=u"Règlement communal d'urbanisme (révision)", description="<p>est situé sur le territoire ou la partie du territoire communal visé(e) par le projet - de révision du - de - règlement communal d'urbanisme approuvé par ... du ...;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="rcu-approuve-provisoirement",title=u"Règlement communal d'urbanisme (approuvé provisoirement)", description="<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé provisoirement par ... du ... est applicable;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="rcu-unite-paysagere-urbaine",title=u"Règlement communal d'urbanisme (Unité paysagère urbaine)", description="<p>est situé en unité paysagère urbaine de bâtisse en ordre continu Art.15 au règlement communal d'urbanisme en vigueur;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="natura-2000",title=u"Site Natura 2000", description="<p>est situé dans le périmètre d'un site Natura 2000 visé par l'article 1bis alinéa unique 18° de la loi du 12 juillet 1973 sur la conservation de la nature, modifié par le décret du 6 décembre 2001 relatif à la conservation des sites Natura 2000 ainsi que de la faune et de la flore sauvages;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="natura-2000-art6",title=u"Natura 2000 (article 6 de la loi du 12 juillet 1973)", description="<p>est situé dans le périmètre d'un territoire désigné en vertu de l'article 6 de la loi du 12 juillet 1973 sur la conservation de la nature, modifié par le décret du 6 décembre 2001 relatif à la conservation des sites Natura 2000 ainsi que de la faune et de la flore sauvages;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-prise-eau",title=u"Zone de prise d'eau", description="<p>est situé dans une zone de prise d'eau, de prévention ou de surveillance au sens du décret du 30 avril 1990 relatif à la protection et l'exploitation des eaux souterraines et des eaux potabilisables modifié la dernière fois par le décret du 15 avril 1999 relatif au cycle de l'eau et instituant une société publique de gestion de l'eau;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="plan-expropriation",title=u"Plan d'expropriation", description="<p> est situé dans les limites d'un plan d'expropriation approuvé par ... du ... ; le pouvoir expropriant est : ...;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="droit-de-preemption",title=u"Droit de préemption", description="<p>est situé dans un périmètre d'application du droit de préemption arrêté par ... du ...; le(s) bénéficiaires(s) du droit de préemption est (sont) : ...;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="perimetre-site-desaffecte",title=u"Périmètre site désaffecté", description="<p>est situé dans le périmètre du site d'activité économique désaffecté suivant : ...;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="revitalisation-urbaine",title=u"Revitalisation urbaine", description="<p>est situé dans un périmètre de revitalisation urbaine;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="renovation-urbaine",title=u"Rénovation urbaine", description="<p>est situé dans un périmètre de rénovation urbaine;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="classe",title=u"Classé (article 196 du CWATUPE)", description="<p>est - inscrit sur la liste de sauvegarde visée à l'article 193 - classé en application de l'article 196 - situé dans une zone de protection visée à l'article 209 - localisé dans un site repris à l'inventaire des sites archéologiques visés à l'article 233 - du Code précité;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="raccordable-egout",title=u"Raccordable à l'égout", description="<p>est actuellement raccordable à l'égout selon les normes fixées par le Service Technique Communal;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="raccordable-egout-prevision",title=u"Raccordable à l'égout (prévision)", description="<p>sera raccordable àl'égout selon les prévisions actuelles;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-faiblement-habitee",title=u"Zone faiblement habitée (épuration individuelle)", description="<p>est situé dans une des zones faiblement habitée qui ne seront pas pourvue d'égout et qui feront l'objet d'une épuration individuelle;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="voirie-suffisamment-equipee",title=u"Voirie suffisamment équipée", description="<p>bénéficie d'un accès à une voirie suffisamment équipée en eau, électricité, pourvue d'un revêtement solide et d'une largeur suffisante compte tenu de la situation des lieux;</p>")
                setHTMLContentType(newFolder, 'description')

            #we add the custom township specific features folder
            if not hasattr(aq_base(configFolder), 'townshipspecificfeatures'):
                newFolderid = configFolder.invokeFactory("Folder",id="townshipspecificfeatures",title=_("urban_label_townshipSpecificFeatures", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                newFolder.setConstrainTypesMode(1)
                newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
                newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
                newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-a-risque",title=u"Se trouve dans une zone à risque", description="<p>se trouve dans une zone à risque (faible moyen élevé) dans la cartographie Aléa d'inondation par débordement de cours d'eau - dressée dans le cadre du plan P.L.U.I.E.S et annexée à l'arrêté du Gouvernement Wallon, adopté en date du 13 juillet 2008;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="insalubrite",title=u"Est frappé d'un Arrêté d'insalubrité", description="<p>est frappé d'un Arrêté d'insalubrité OU d'un permis de location datant du [...] - Le futur acquéreur est invité à prendre contact avec le Service Logement Salubrité (tél. : [...]) pour de plus amples informations;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="infraction-urbanistique",title=u"Infraction urbanistique", description="<p>fait l'objet d'une infraction urbanistique reconnue par notre Administration communale portant sur [...];</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="cu1",title=u"Certificat d'Urbanisme 1 dans les deux ans", description="<p>a fait l'objet, dans les deux dernières années, d'un Certificat d'Urbanisme n°1 datant du [...] et portant la référence [...];</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="permis-urbanisme",title=u"Permis d'Urbanisme depuis 1976", description="<p>a fait l'objet depuis 1976 d'un permis d'urbanisme daté de [...] pour [...] - REFUS/ACCEPTE - Réf.: [...];</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="reconnaissance-economique",title=u"Périmètre de reconnaissance économique", description="<p>est repris dans un périmètre de reconnaissance économique;</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="site-seveso",title=u"A moins de 2000m d'un site SEVESO", description="<p>est situé à moins de 2000m d'un site classé SEVESO à savoir [...];</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="gestion-des-sols",title=u"Gestion des sols", description="<p>état des sols, nous ne sommes pas en mesure de déterminer si le bien est ou pas inscrit dans la banque de données au sens de l'article 10 du décret du 5 décembre 2008 relatif à la gestion des sols (Décret du 05 décembre 2008, art.89, al.2)</p>")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="galeries-minieres",title=u"Galeries minières", description="<p>est situé dans une région traversée par de nombreuses galeries minières et nous ne sommes pas en mesure de déterminer l'état de celle-ci, veuillez donc prendre vos renseignements aurpès du SPW - Département de l'Environnement et de l'Eau - " \
                                                                                                                             "Direction des risques industriels, géologique et miniers - Cellules sous-sol/géologique - Avenue Prince de Liège, 15 à 5100 Jambes;  Le bien est situé sur une zone de consultation en liaison avec les gisements et puits de mine;</p>")

        if urban_type in ['BuildLicence', 'ParcelOutLicence', 'UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter', ]:
            if not hasattr(aq_base(configFolder), 'missingparts'):
                #add "missingparts" folder
                newFolderid = configFolder.invokeFactory("Folder",id="missingparts",title=_("missingparts_folder_title", 'urban', context=site.REQUEST))
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
                if urban_type in ['UrbanCertificateOne', 'UrbanCertificateTwo', ]:
                    #necessary documents for UrbanCertificates
                    newFolder.invokeFactory("UrbanVocabularyTerm",id="form_demande",title=u"Formulaire de demande (formulaire 1A) en 3 exemplaires")
                    newFolder.invokeFactory("UrbanVocabularyTerm",id="extrait_cadastral",title=u"Extrait cadastral en 3 exemplaires")

            if not hasattr(aq_base(configFolder), 'folderprotectedbuildings'):
                #add ProtectedBuildings folder
                newFolderid = configFolder.invokeFactory("Folder",id="folderprotectedbuildings",title=_("folderprotectedbuildings_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                newFolder.setConstrainTypesMode(1)
                newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
                newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
                newFolder.invokeFactory("UrbanVocabularyTerm",id="classe",title=u"classé ou assimilé")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="zoneprotection",title=u"zone de protection")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="reprisinventaire",title=u"repris à l'inventaire")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="archeologique",title=u"à l'Atlas archéologique")

        if urban_type in ['BuildLicence', 'ParcelOutLicence', ]:
            #add investigation articles folder
            #this is done by a method because the migrateBuildLicencesInvestigationArticles
            #migration step will use it too
            addInvestigationArticles(context, configFolder)
            if not hasattr(aq_base(configFolder), 'foldermakers'):
                #add Makers folder
                newFolderid = configFolder.invokeFactory("Folder",id="foldermakers",title=_("foldermakers_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                newFolder.setConstrainTypesMode(1)
                newFolder.setLocallyAllowedTypes(['OrganisationTerm'])
                newFolder.setImmediatelyAddableTypes(['OrganisationTerm'])
                newFolder.invokeFactory("OrganisationTerm",id="service-pop",title=u"Service population", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                newFolder.invokeFactory("OrganisationTerm",id="spw-dgo1",title=u"SPW-DGO1", description=u'<p>Direction Générale opérationnelle<br />Département du réseau de Namur et du Luxembourg<br />District 131.12 - SPY<br />37, Route de Saussin<br />5190 Spy</p>')
                newFolder.invokeFactory("OrganisationTerm",id="dgrne",title=u"DGRNE", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                newFolder.invokeFactory("OrganisationTerm",id="dnf",title=u"DNF", description=u'<p>39, Avenue Reine Astrid<br />5000 Namur</p>')
                newFolder.invokeFactory("OrganisationTerm",id="stp",title=u"Service Technique Provincial", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                newFolder.invokeFactory("OrganisationTerm",id="pi",title=u"Prévention Incendie", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                newFolder.invokeFactory("OrganisationTerm",id="bec",title=u"Bureau d'études communal", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                newFolder.invokeFactory("OrganisationTerm",id="svp",title=u"Service Voyer Principal", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                newFolder.invokeFactory("OrganisationTerm",id="agriculture",title=u"Agriculture", description=u'<p>Direction Générale opérationnelle<br />Agriculture, Ressources naturelles et Environnement<br />Service extérieur de Wavre<br />4, Avenue Pasteur<br />1300 Wavre</p>')
                newFolder.invokeFactory("OrganisationTerm",id="pn",title=u"Parc Naturel", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                newFolder.invokeFactory("OrganisationTerm",id="crmsf",title=u"Commission Royale des Monuments, Sites et Fouilles", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                newFolder.invokeFactory("OrganisationTerm",id="swde",title=u"SWDE", description=u'<p>14, Rue Joseph Saintraint<br />5000 Namur</p>')
                newFolder.invokeFactory("OrganisationTerm",id="ccatm",title=u"CCATM", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                newFolder.invokeFactory("OrganisationTerm",id="inasep",title=u"INASEP", description=u'<p>1b, Rue des Viaux<br />5100 Naninne</p>')
                newFolder.invokeFactory("OrganisationTerm",id="belgacom",title=u"Belgacom", description=u'<p>60, Rue Marie Henriette<br />5000 Namur</p>')
                newFolder.invokeFactory("OrganisationTerm",id="spge",title=u"SPGE", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                newFolder.invokeFactory("OrganisationTerm",id="cibe",title=u"CIBE/Vivaqua", description=u'<p>70, Rue aux Laines<br />1000 Bruxelles</p>')
                newFolder.invokeFactory("OrganisationTerm",id="sncb",title=u"SNCB", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                newFolder.invokeFactory("OrganisationTerm",id="infrabel",title=u"Infrabel", description=u'<p>Infrastructure ferroviaire<br />2/003, Place des Guillemins<br />4000 Liège</p>')
                newFolder.invokeFactory("OrganisationTerm",id="voo",title=u"VOO", description=u'<p>1, Rue xxx<br />xxxx Commune</p>')
                #now, we need to specify that the description's mimetype is 'text/html'
                setHTMLContentType(newFolder, 'description')

            if not hasattr(aq_base(configFolder), 'folderdelays'):
                #add Delays folder
                newFolderid = configFolder.invokeFactory("Folder",id="folderdelays",title=_("folderdelays_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                newFolder.setConstrainTypesMode(1)
                newFolder.setLocallyAllowedTypes(['UrbanDelay'])
                newFolder.setImmediatelyAddableTypes(['UrbanDelay'])
                newFolder.invokeFactory("UrbanDelay",id="30j",title=u"30 jours", deadLineDelay=30, alertDelay=20)
                newFolder.invokeFactory("UrbanDelay",id="70j",title=u"70 jours", deadLineDelay=70, alertDelay=20)
                newFolder.invokeFactory("UrbanDelay",id="75j",title=u"75 jours", deadLineDelay=75, alertDelay=20)
                newFolder.invokeFactory("UrbanDelay",id="115j",title=u"115 jours", deadLineDelay=115, alertDelay=20)
                newFolder.invokeFactory("UrbanDelay",id="230j",title=u"230 jours", deadLineDelay=230, alertDelay=20)
                newFolder.invokeFactory("UrbanDelay",id="art127",title=u"Article 127", deadLineDelay=0, alertDelay=20)
                newFolder.invokeFactory("UrbanDelay",id="inconnu",title=u"Inconnu", deadLineDelay=0, alertDelay=20)

            if not hasattr(aq_base(configFolder), 'derogations'):
                #add the derogations folder
                newFolderid = configFolder.invokeFactory("Folder",id="derogations",title=_("derogations_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                newFolder.setConstrainTypesMode(1)
                newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
                newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
                newFolder.invokeFactory("UrbanVocabularyTerm",id="dero-ps",title=u"au Plan de secteur")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="dero-pca",title=u"au Plan Communal d'Aménagement")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="dero-rru",title=u"au Règlement Régional d'Urbanisme")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="dero-rcu",title=u"au Règlement Communal d'Urbanisme")
                newFolder.invokeFactory("UrbanVocabularyTerm",id="dero-lot",title=u"au Lotissement")

            if not hasattr(aq_base(configFolder), 'folderbuildworktypes'):
                #add BuildWorkTypes folder
                newFolderid = configFolder.invokeFactory("Folder",id="folderbuildworktypes",title=_("folderbuildworktype_folder_title", 'urban', context=site.REQUEST))
                newFolder = getattr(configFolder, newFolderid)
                newFolder.setConstrainTypesMode(1)
                newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
                newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
                newFolder.invokeFactory("UrbanVocabularyTerm",id="ncmu",title=u"Nouvelle construction - Maison unifamiliale", extraValue='N_UNI')
                newFolder.invokeFactory("UrbanVocabularyTerm",id="ncia",title=u"Nouvelle construction - Immeuble appartements", extraValue='N_APPART')
                newFolder.invokeFactory("UrbanVocabularyTerm",id="nca",title=u"Nouvelle construction - Autres", extraValue='N_AUT')
                newFolder.invokeFactory("UrbanVocabularyTerm",id="tmu",title=u"Transformation - maison unifamiliale", extraValue='T_UNI')
                newFolder.invokeFactory("UrbanVocabularyTerm",id="tia",title=u"Transformation - immeuble appartements", extraValue='T_APPART')
                newFolder.invokeFactory("UrbanVocabularyTerm",id="tab",title=u"Transformation - autre bâtiment", extraValue='T_AUT')
                newFolder.invokeFactory("UrbanVocabularyTerm",id="dg",title=u"Démolition - Général", extraValue='DEM')
                newFolder.invokeFactory("UrbanVocabularyTerm",id="lg",title=u"Lotissement - Général", extraValue='LOT')
                newFolder.invokeFactory("UrbanVocabularyTerm",id="tnbg",title=u"Transformation Non-bâti - Général", extraValue='T_NBAT')
                newFolder.invokeFactory("UrbanVocabularyTerm",id="td",title=u"Taudis", extraValue='TAUDIS')
                # !!! NOT SURE ABOUT  extraValue='INT' . TO BE CHECKED AND CORRECTED !!!
                newFolder.invokeFactory("UrbanVocabularyTerm",id="integration",title=u"Intégration dans voirie publique", extraValue='INT')
                newFolder.invokeFactory("UrbanVocabularyTerm",id="leasing",title=u"Leasing (pour mémoire SPF Finances)", extraValue='LEASING')
                newFolder.invokeFactory("UrbanVocabularyTerm",id="autres",title=u"Autres", extraValue='AUTRE')

def addInvestigationArticles(context, configFolder):
    """
      This method add default investigation articles
    """
    site = context.getSite()

    if not hasattr(aq_base(configFolder), 'investigationarticles'):
        newFolderid = configFolder.invokeFactory("Folder",id="investigationarticles",title=_("investigationarticles_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(configFolder, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-1",title=u"330 1° - « [...] bâtiments dont la hauteur est d’au moins quatre niveaux ou douze mètres sous corniche et [...] »", description="<p>« la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins quatre niveaux ou douze mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", extraValue="330 1°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-2",title=u"330 2° - « [...] bâtiment dont la profondeur, mesurée [...] est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments [...] »", description="<p>« la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l’alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l’alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës (AGW du 23 décembre 1998, art 1er), la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", extraValue="330 2°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-3",title=u"330 3° - « [...] un magasin [...] dont la surface nette de vente est supérieure à 400 m² [...] »", description="<p>« la construction, la reconstruction d’un magasin ou la modification de la destination d’un bâtiment en magasin dont la surface nette de vente est supérieure à 400 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", extraValue="330 3°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-4",title=u"330 4° - « [...] de bureaux [...] dont la superficie des planchers est supérieure à 650 m² [...] »", description="<p>« la construction, la reconstruction de bureaux ou la modification de la destination d’un bâtiment en bureaux dont la superficie des planchers est supérieure à 650 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", extraValue="330 4°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-5",title=u"330 5° - « [...] bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à 400 m² [...] »", description="<p>« la construction, la reconstruction ou la modification de la destination d’un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à 400 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", extraValue="330 5°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-6",title=u"330 6° - « l’utilisation habituelle d’un terrain pour le dépôt d’un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets »", description="<p>« l’utilisation habituelle d’un terrain pour le dépôt d’un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets »</p>", extraValue="330 6°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-7",title=u"330 7° - « [...] permis de lotir ou de permis d’urbanisme [...] constructions groupées visées à l’article 126 qui portent sur une superficie de 2 hectares et plus »", description="<p>« les demandes de permis de lotir ou de permis d’urbanisme relatives à des constructions groupées visées à l’article 126 qui portent sur une superficie de 2 hectares et plus »</p>", extraValue="330 7°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-8",title=u"330 8° - « [...] permis de lotir ou de permis d’urbanisme [...] constructions groupées visées à l’article 126 qui peuvent comporter un ou plusieurs bâtiments visés aux 1°, 2°,3°, 4° et 5° »", description="<p>« les demandes de permis de lotir ou de permis d’urbanisme relatives à des constructions groupées visées à l’article 126 qui peuvent comporter un ou plusieurs bâtiments visés aux 1°, 2°,3°, 4° et 5° »</p>", extraValue="330 8°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-9",title=u"330 9° - « les demandes de permis de lotir ou de permis d’urbanisme visées à l’article 128 »", description="<p>« les demandes de permis de lotir ou de permis d’urbanisme visées à l’article 128 »</p>", extraValue="330 9°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-10",title=u"330 10° - « les demandes de permis de lotir visées à l’article 97 »", description="<p>« les demandes de permis de lotir visées à l’article 97 »</p>", extraValue="330 10°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-11",title=u"330 11° - « les demandes de permis de lotir ou de permis d’urbanisme impliquant l’application des articles 110 à 113 »", description="<p>« les demandes de permis de lotir ou de permis d’urbanisme impliquant l’application des articles 110 à 113 »</p>", extraValue="330 11°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-12",title=u"330 12° - « [...] permis de lotir et les demandes de permis d’urbanisme [...] d’un bâtiment qui se rapportent à des biens immobiliers inscrits sur la liste de sauvegarde [...] »", description="<p>« les demandes de permis de lotir et les demandes de permis d’urbanisme relatives à la construction, la reconstruction ou la transformation d’un bâtiment qui se rapportent à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protection visée à l’article 205 (lire article 209) ou localisés dans un site mentionné à l’atlas visé à l’article 215 (lire article 233) »</p>", extraValue="330 12°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="330-13",title=u"330 13° - « les voiries publiques de la Région classées en réseau interurbain (RESI) par l’arrêté ministériel du 11 août 1994 »" ,description="<p>« les voiries publiques de la Région classées en réseau interurbain (RESI) par l’arrêté ministériel du 11 août 1994 »</p>", extraValue="330 13°")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="334-2",title=u"334 2° - « Dès le lendemain du jour où il est en possession de l’accusé de réception et jusqu’au jour de la clôture de l’enquête publique [...]»" ,description="<p>« Dès le lendemain du jour où il est en possession de l’accusé de réception et jusqu’au jour de la clôture de l’enquête publique, le demandeur est tenu d’afficher sur le terrain faisant l’objet de la demande : 2° dans les cas visés à l’article 330, 1° à 5°, et 12°, ou lorsque la dérogation porte sur le gabarit d’un bâtiment, une vue axonométrique du projet et des bâtiments contigus »</p>", extraValue="334 2°")
        #now, we need to specify that the description's mimetype is 'text/html'
        setHTMLContentType(newFolder, 'description')

def addUrbanGroups(context):
    """
       Add a group of 'urban' application users...
    """
    site = context.getSite()
    #add 3 groups
    #one with urban Managers
    site.portal_groups.addGroup("urban_managers", title="Urban Managers")
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
    site.portal_urban.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
    site.portal_urban.manage_addLocalRoles("urban_readers", ("Reader",))
    site.portal_urban.manage_addLocalRoles("urban_editors", ("Reader",))

    #application folders local roles
    #global application folder : "urban_readers" and "urban_editors" can read...
    if hasattr(site, "urban"):
        app_folder = getattr(site, "urban")
        app_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
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
        b_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
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
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
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
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
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
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
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
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
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
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
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
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
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
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #architects application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "architects"):
        p_folder = getattr(app_folder, "architects")
        app_folder.manage_permission('Add portal content', ['Manager', 'Contributor', 'Owner', 'Editor', ], acquire=0)
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #geometricians application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "geometricians"):
        p_folder = getattr(app_folder, "geometricians")
        app_folder.manage_permission('Add portal content', ['Manager', 'Contributor', 'Owner', 'Editor', ], acquire=0)
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
        p_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        p_folder.manage_addLocalRoles("urban_editors", ("Editor",))
    #notaries application folder : "urban_readers" can read and "urban_editors" can edit...
    if hasattr(app_folder, "notaries"):
        p_folder = getattr(app_folder, "notaries")
        app_folder.manage_permission('Add portal content', ['Manager', 'Contributor', 'Owner', 'Editor', ], acquire=0)
        p_folder.manage_addLocalRoles("urban_managers", ("Contributor", "Reviewer", "Editor", "Reader",))
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
    )

    #add globaltemplates folder
    if not hasattr(tool, "globaltemplates"):
        globaltemplatesFolderid = tool.invokeFactory("Folder",id="globaltemplates",
                                                     title=_("globaltemplates_folder_title", 'urban', context=site.REQUEST))
        globaltemplatesFolder = getattr(tool, globaltemplatesFolderid)
        globaltemplatesFolder.setConstrainTypesMode(1)
        globaltemplatesFolder.setLocallyAllowedTypes(['File'])
        globaltemplatesFolder.setImmediatelyAddableTypes(['File'])

    #add foldermanagers folder
    if not hasattr(tool, "foldermanagers"):
        foldermanagersFolderid = tool.invokeFactory("Folder",id="foldermanagers",
                                                    title=_("foldermanagers_folder_title", 'urban', context=site.REQUEST))
        foldermanagersFolder = getattr(tool, foldermanagersFolderid)
        foldermanagersFolder.setConstrainTypesMode(1)
        foldermanagersFolder.setLocallyAllowedTypes(['FolderManager'])
        foldermanagersFolder.setImmediatelyAddableTypes(['FolderManager'])

    if not hasattr(tool, "topics"):
        topicsFolderId = tool.invokeFactory("Folder",id="topics",title=_("topics", 'urban', context=site.REQUEST))
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
        topic.setTitle(_(topicId, 'urban', context=site.REQUEST))
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
        newFolderid = tool.invokeFactory("Folder",id="pcas",title=_("pcas_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['PcaTerm'])
        newFolder.setImmediatelyAddableTypes(['PcaTerm'])
        newFolder.invokeFactory("PcaTerm",id="pca1",label=u"Plan communal d'aménagement 1", number='1', decreeDate="2009/01/01", decreeType="royal")
        newFolder.invokeFactory("PcaTerm",id="pca2",label=u"Plan communal d'aménagement 2", number='2', decreeDate="2008/06/23", decreeType="royal")
        newFolder.invokeFactory("PcaTerm",id="pca3",label=u"Plan communal d'aménagement 3", number='3', decreeDate="2001/12/13", decreeType="departmental")

    #add the parcelling folder
    if not hasattr(tool, "parcellings"):
        newFolderid = tool.invokeFactory("Folder",id="parcellings",title=_("parcellings_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['ParcellingTerm'])
        newFolder.setImmediatelyAddableTypes(['ParcellingTerm'])
        newFolder.invokeFactory("ParcellingTerm",id="p1",title=u"Lotissement 1 (André Ledieu - 01/01/2005 - 10)", label="Lotissement 1", subdividerName="André Ledieu", authorizationDate="2005/01/01", approvaleDate="2005/01/12", numberOfParcels=10)
        newFolder.invokeFactory("ParcellingTerm",id="p2",title=u"Lotissement 2 (Ets Tralala - 01/06/2007 - 8)", label="Lotissement 2", subdividerName="Ets Tralala", authorizationDate="2007/06/01", approvaleDate="2007/06/12", numberOfParcels=8)
        newFolder.invokeFactory("ParcellingTerm",id="p3",title=u"Lotissement 3 (SPRL Construction - 02/05/2001 - 15)", label="Lotissement 3", subdividerName="SPRL Construction", authorizationDate="2001/05/02", approvaleDate="2001/05/10", numberOfParcels=15)

    #add the streets folder
    if not hasattr(tool, "streets"):
        newFolderid = tool.invokeFactory("Folder",id="streets",title=_("streets_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['City'])
        newFolder.setImmediatelyAddableTypes(['City'])

    if not hasattr(tool, "pashs"):
        #add pashs folder
        newFolderid = tool.invokeFactory("Folder",id="pashs",title=_("pashs_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-epuration-collective",title=u"Zone d'épuration collective")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-transitoire",title=u"Zone transitoire")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="zone-epuration-individuelle",title=u"Zone d'épuration individuelle")

    #add global folderroadtypes folder
    if not hasattr(tool, "folderroadtypes"):
        newFolderid = tool.invokeFactory("Folder",id="folderroadtypes",title=_("folderroadtypes_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        newFolder.invokeFactory("UrbanVocabularyTerm",id="com",title=u"Communale")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="priv",title=u"Privée")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="prov",title=u"Provinciale")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="reg",title=u"Régionale")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="vic",title=u"Vicinale")

    if not hasattr(tool, 'folderroadequipments'):
        #add RoadEquipments folder
        newFolderid = tool.invokeFactory("Folder",id="folderroadequipments",title=_("folderroadequipments_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
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

    if not hasattr(tool, "folderroadcoatings"):
        #add RoadCoatings folder
        newFolderid = tool.invokeFactory("Folder",id="folderroadcoatings",title=_("folderroadcoatings_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        newFolder.invokeFactory("UrbanVocabularyTerm",id="filetseau",title=u"Filets d'eau")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="bordures",title=u"Bordures")

    #add Zones folder
    if not hasattr(tool, "folderzones"):
        newFolderid = tool.invokeFactory("Folder",id="folderzones",title=_("folderzones_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
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
        newFolder.invokeFactory("UrbanVocabularyTerm",id="znatura2000",title=u"zone Natura 2000")

    #add the RCU folder
    if not hasattr(tool, "rcu"):
        newFolderid = tool.invokeFactory("Folder",id="rcu",title=_("rcu_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        #add some examples
        newFolder.invokeFactory("UrbanVocabularyTerm",id="rcu-aire-a",title=u"Aire A habitat centre des villages")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="rcu-aire-b",title=u"Aire B habitat hors centre des villages")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="rcu-aire-c",title=u"Aire C rives des habitats")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="rcu-aire-d",title=u"Aire D activités économiques")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="rcu-aire-e",title=u"Aire E dominante rurale")

    #add the SSC folder
    if not hasattr(tool, "ssc"):
        newFolderid = tool.invokeFactory("Folder",id="ssc",title=_("ssc_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        #add some examples
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-centre-ville",title=u"Zone d'habitat urbain de centre-ville")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-suburbain",title=u"Zone d'habitat suburbain")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-services-publics",title=u"Zone de services publics et d'équipements communautaires")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-industrielle",title=u"Zone industrielle")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-industrielle-verte",title=u"Zone industrielle verte")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-militaire",title=u"Zone militaire")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-habitat-urban-differe",title=u"Zone d'habitat urbain à aménagement différé")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-extraction",title=u"Zone d'extraction")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-loisirs",title=u"Zone de loisirs et de séjours")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-agricole",title=u"Zone agricole")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-vert-social",title=u"Zone d'espace vert social")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-vert-eco",title=u"Zone d'espace vert ecologique")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-vert-mixte",title=u"Zone d'espace vert mixte")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-naturelle",title=u"Zone naturelle")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-forestiere",title=u"Zone forestière")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-forestiere-mixte",title=u"Zone forestière mixte")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-activites-economiques-mixtes",title=u"Zone d'activités économiques mixtes")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="ssc-activites-economiques-tertiaires",title=u"Zone d'activités économiques tertiaires")

    #add the additional_layers folder
    if not hasattr(tool, "additional_layers"):
        newFolderid = tool.invokeFactory("Folder",id="additional_layers",title=_("additonal_layers_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['Layer'])
        newFolder.setImmediatelyAddableTypes(['Layer'])
        #additional layers are added in the extra step "setupExtra"

    #add the persons_titles folder
    if not hasattr(tool, "persons_titles"):
        newFolderid = tool.invokeFactory("Folder",id="persons_titles",title=_("persons_titles_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['PersonTitleTerm'])
        newFolder.setImmediatelyAddableTypes(['PersonTitleTerm'])
        newFolder.invokeFactory("PersonTitleTerm",id="notitle",title=u"", abbreviation="", gender="male", multiplicity="single")
        newFolder.invokeFactory("PersonTitleTerm",id="madam",title=u"Madame", abbreviation="Mme", gender="female", multiplicity="single")
        newFolder.invokeFactory("PersonTitleTerm",id="miss",title=u"Mademoiselle", abbreviation="Mlle", gender="female", multiplicity="single")
        newFolder.invokeFactory("PersonTitleTerm",id="mister",title=u"Monsieur", abbreviation="M", gender="male", multiplicity="single")
        newFolder.invokeFactory("PersonTitleTerm",id="madam_and_mister",title=u"Monsieur et Madame", abbreviation="M et Mme", gender="male", multiplicity="plural")
        newFolder.invokeFactory("PersonTitleTerm",id="master",title=u"Maître", abbreviation="Me", gender="male", multiplicity="single")
        newFolder.invokeFactory("PersonTitleTerm",id="masters",title=u"Maîtres", abbreviation="Mes", gender="male", multiplicity="plural")
        newFolder.invokeFactory("PersonTitleTerm",id="misters",title=u"Messieurs", abbreviation="MM", gender="male", multiplicity="plural")
        newFolder.invokeFactory("PersonTitleTerm",id="ladies",title=u"Mesdames", abbreviation="Mmes", gender="female", multiplicity="plural")
        newFolder.invokeFactory("PersonTitleTerm",id="consorts",title=u"Consorts", abbreviation="Crts", gender="male", multiplicity="plural")

    #add the persons_grades folder
    if not hasattr(tool, "persons_grades"):
        newFolderid = tool.invokeFactory("Folder",id="persons_grades",title=_("persons_grades_folder_title", 'urban', context=site.REQUEST))
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

    #add the country folder
    if not hasattr(tool, "country"):
        newFolderid = tool.invokeFactory("Folder",id="country",title=_("country_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        newFolder.invokeFactory("UrbanVocabularyTerm",id='germany', title="Allemagne")
        newFolder.invokeFactory("UrbanVocabularyTerm",id='belgium', title="Belgique")
        newFolder.invokeFactory("UrbanVocabularyTerm",id='france', title="France")
        newFolder.invokeFactory("UrbanVocabularyTerm",id='luxembourg', title="Luxembourg")
        newFolder.invokeFactory("UrbanVocabularyTerm",id='netherlands', title="Pays Bas")


    #add the decisions folder
    if not hasattr(tool, "decisions"):
        newFolderid = tool.invokeFactory("Folder",id="decisions",title=_("decisions_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        newFolder.invokeFactory("UrbanVocabularyTerm",id="favorable",title=u"Favorable")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="defavorable",title=u"Défavorable")

    #add the external opinions decisions folder
    if not hasattr(tool, "externaldecisions"):
        newFolderid = tool.invokeFactory("Folder",id="externaldecisions",title=_("external_decisions_folder_title", 'urban', context=site.REQUEST))
        newFolder = getattr(tool, newFolderid)
        newFolder.setConstrainTypesMode(1)
        newFolder.setLocallyAllowedTypes(['UrbanVocabularyTerm'])
        newFolder.setImmediatelyAddableTypes(['UrbanVocabularyTerm'])
        newFolder.invokeFactory("UrbanVocabularyTerm",id="favorable",title=u"Favorable")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="favorable-conditionnel",title=u"Favorable conditionnel")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="defavorable",title=u"Défavorable")
        newFolder.invokeFactory("UrbanVocabularyTerm",id="favorable-defaut",title=u"Réputé favorable par défaut")

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
            topicsFolderId = urbanConfig.invokeFactory("Folder",id="topics",title=_("topics", 'urban', context=site.REQUEST))
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
                topic.setTitle(_("%s_%s"% (urban_type.lower(), topicId), 'urban', context=site.REQUEST))
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
        frontpage.setTitle(_("front_page_title", 'urban', context=site.REQUEST))
        frontpage.setDescription(_("front_page_descr", 'urban', context=site.REQUEST))
        frontpage.setText(_("front_page_text", 'urban', context=site.REQUEST), mimetype='text/html')
        #remove the presentation mode
        frontpage.setPresentation(False)
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

    if not hasattr(aq_base(site), "urban"):
        newFolderid = site.invokeFactory("Folder",id="urban",title=_("urban", 'urban', context=site.REQUEST))
        newFolder = getattr(site, newFolderid)
        newFolder.setLayout('urban_view')
    else:
        newFolder = getattr(site, 'urban')

    for urban_type in URBAN_TYPES:
        if not hasattr(newFolder, urban_type.lower() + 's'):
            newFolderid = newFolder.invokeFactory("Folder",id=urban_type.lower() + 's',title=_(urban_type.lower() + 's', 'urban', context=site.REQUEST))
            newSubFolder = getattr(newFolder, newFolderid)
            alsoProvides(newSubFolder, ILicenceContainer)
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
        newFolderid = newFolder.invokeFactory("Folder",id="architects",title=_("architects_folder_title", 'urban', context=site.REQUEST))
        newSubFolder = getattr(newFolder, newFolderid)
        newSubFolder.setConstrainTypesMode(1)
        newSubFolder.setLocallyAllowedTypes(['Architect'])
        newSubFolder.setImmediatelyAddableTypes(['Architect'])
        newSubFolder.setLayout('architects_folder_view')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Contact', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains geometricians
    if not hasattr(newFolder, "geometricians"):
        newFolderid = newFolder.invokeFactory("Folder",id="geometricians",title=_("geometricians_folder_title", 'urban', context=site.REQUEST))
        newSubFolder = getattr(newFolder, newFolderid)
        newSubFolder.setConstrainTypesMode(1)
        newSubFolder.setLocallyAllowedTypes(['Geometrician'])
        newSubFolder.setImmediatelyAddableTypes(['Geometrician'])
        newSubFolder.setLayout('geometricians_folder_view')
        #manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Geometrician', ['Manager', 'Editor', ], acquire=0)

    #add a folder that will contains notaries
    if not hasattr(newFolder, "notaries"):
        newFolderid = newFolder.invokeFactory("Folder",id="notaries",title=_("notaries_folder_title", 'urban', context=site.REQUEST))
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
            newFolder.invokeFactory("Link",id=search_link[0],title=_('urban_%s_descr' % search_link[0], 'urban', context=site.REQUEST), remoteUrl=search_link[1])

def addTestObjects(context):
    """
       Add some users and objects for test purpose...
    """
    if context.readDataFile('urban_tests_marker.txt') is None:
        return

    #add some users, some architects and some foldermanagers...
    #add 3 users, one as manager, one as reader and one as editor...
    site = context.getSite()
    is_mountpoint = len(site.absolute_url_path().split('/')) > 2
    try:
        password = 'urbanmanager'
        if is_mountpoint:
            password = generatePassword(8)
        member = site.portal_registration.addMember(id="urbanmanager", password=password)
        member.setMemberProperties({'ext_editor':True})
        password = 'urbanreader'
        if is_mountpoint:
            password = generatePassword(8)
        site.portal_registration.addMember(id="urbanreader", password=password)
        password = 'urbaneditor'
        if is_mountpoint:
            password = generatePassword(8)
        member = site.portal_registration.addMember(id="urbaneditor", password=password)
        member.setMemberProperties({'ext_editor':True})
        #put users in the correct group
        site.acl_users.source_groups.addPrincipalToGroup("urbanmanager", "urban_managers")
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
    tool = site.portal_urban
    fmFolder = getattr(tool, "foldermanagers")
    if not fmFolder.objectIds():
        fmFolder.invokeFactory("FolderManager",id="foldermanager1",name1="Dumont", name2="Jean",
                                grade='agent-technique', manageableLicences=['BuildLicence'])
        fmFolder.invokeFactory("FolderManager",id="foldermanager2",name1="Schmidt", name2="Alain",
                                grade='directeur-general', manageableLicences=['NotaryLetter'])
        fmFolder.invokeFactory("FolderManager",id="foldermanager3",name1="Robert", name2="Patrick",
                                grade='responsable-administratif', manageableLicences=['BuildLicence'])

    tool = site.portal_urban

    #create some streets using the Extensions.imports script
    if not tool.streets.objectIds('City'):
        from Products.urban.Extensions.imports import import_streets_fromfile, import_localities_fromfile
        import_streets_fromfile(tool)
        import_localities_fromfile(tool)

    #add default UrbanEventTypes for documents generation
    addUrbanEventTypes(context)
    #add OpinionRequest UrbanEventTypes by notifying the creation of their corresponding OrganisationTerm
    for organisation_term in tool.buildlicence.foldermakers.objectValues():
        event.notify(ObjectInitializedEvent(organisation_term))

    #add some generic templates in configuration
    addGlobalTemplates(context)

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


def addTestBuildlicense(context):
    """
    Add a Buildlicence for tests purpose ...
    """
    if context.readDataFile('urban_tests_marker.txt') is None:
        return

    site = context.getSite()
    urban_folder = site.urban
    portal_urban = site.portal_urban
    buildlicences_folder = urban_folder.buildlicences
    foldermanager = portal_urban.foldermanagers.foldermanager1
    architects_folder = buildlicences_folder.architects

    architect = getattr(architects_folder, portal_urban.plone_utils.normalizeString('Archi1Name-Archi1FirstName'))

    licence_id = site.generateUniqueId('homewrecker')
    buildlicences_folder.invokeFactory('BuildLicence', id=licence_id, licenceSubject='starfish chocolates', usage='for_habitation',architects=[architect], foldermanagers=[foldermanager])
    licence = getattr(buildlicences_folder, licence_id)
    licence.invokeFactory("Applicant", id=site.generateUniqueId('smithandwesson'), personTitle='masters', name1='Smith &', name2='Wesson', street='Rue du porc dans le yaourt', number='42', zipcode='5032', city='Couillet' )
    licence.processForm()

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
        logger.warning("No 'additonal_layers' folder found in portal_urban, we create it.")
        additional_layers_id = portal_urban.invokeFactory("Folder",id="additional_layers",title=_("additonal_layers_folder_title", 'urban', context=portal.REQUEST, default="Additional layers"))
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
                        additional_layers.invokeFactory("Layer", id="ppnc", title=u"PPNC", WMSUrl="http://cartopro1.wallonie.be/WMS/com.esri.wms.Esrimap/PPNC?", layers=layer, SRS="ESPG:31370", baseLayer=True, layerFormat="image/png")
                        already_ppnc = True
                        logger.info("Additional layer '%s' added with layer '%s'"%('ppnc', layer))
                    else:
                        logger.info("ALREADY found layer !")
                        additional_layers.invokeFactory("Layer", id=layer, title=layer.upper(), WMSUrl="http://cartopro1.wallonie.be/WMS/com.esri.wms.Esrimap/PPNC?", layers=layer, SRS="ESPG:31370", baseLayer=True, layerFormat="image/png")
                        additional_layers.ppnc.setTitle(additional_layers.ppnc.getLayers().upper())
                        additional_layers.ppnc.reindexObject()
                        logger.info("Additional layer '%s' added with layer '%s'"%(layer, layer))

            if not hasattr(aq_base(additional_layers), 'ppnc'):
                logger.error("Additional layer '%s' added WITHOUT specific layer because no ppnc intersection found"%'ppnc')
                additional_layers.invokeFactory("Layer", id="ppnc", title=u"PPNC", WMSUrl="http://cartopro1.wallonie.be/WMS/com.esri.wms.Esrimap/PPNC?", layers='ppnc', SRS="ESPG:31370", baseLayer=True, layerFormat="image/png")
        else:
            logger.error("Additional layer '%s' not added because the mapExtent is not defined in portal_urban"%'ppnc')
#Layers order
#PPNC
#Parcelles
#Rues
#Batiments
#N° parcelle
#N° maison
    if not hasattr(aq_base(additional_layers), 'parcelles'):
        additional_layers.invokeFactory("Layer",id="parcelles",title=u"Parcelles",layers="urban%s:capa" % nis,SRS="ESPG:31370",transparent=False,visibility=True, layerFormat="image/png")
        logger.info("Additional layer '%s' added"%'parcelles')
    if not hasattr(aq_base(additional_layers), 'rues'):
        additional_layers.invokeFactory("Layer",id="rues",title=u"Nom des rues",layers="urban%s:toli" % nis,SRS="ESPG:31370",transparent=True,visibility=True, layerFormat="image/png")
        logger.info("Additional layer '%s' added"%'rues')
    if not hasattr(aq_base(additional_layers), 'batiments'):
        additional_layers.invokeFactory("Layer",id="batiments",title=u"Bâtiments",layers="urban%s:cabu" % nis,SRS="ESPG:31370",transparent=True,visibility=True, layerFormat="image/png")
        logger.info("Additional layer '%s' added"%'batiments')
    if not hasattr(aq_base(additional_layers), 'num_parcelle'):
        additional_layers.invokeFactory("Layer",id="num_parcelle",title=u"N° de parcelle",layers="urban%s:canu" % nis,styles="ParcelsNum", SRS="ESPG:31370",transparent=True,visibility=False, layerFormat="image/png")
        logger.info("Additional layer '%s' added"%'num_parcelle')
    if not hasattr(aq_base(additional_layers), 'num_maisons'):
        additional_layers.invokeFactory("Layer",id="num_maisons",title=u"N° de maison",layers="urban%s:canu" % nis,styles="HousesNum",SRS="ESPG:31370",transparent=True,visibility=False, layerFormat="image/png")
        logger.info("Additional layer '%s' added"%'num_maisons')

def setHTMLContentType(folder, fieldName):
    """
      Set the correct text/html content type for text/html TextFields
    """
    objs = folder.objectValues()
    for obj in objs:
        if hasattr(aq_base(obj), fieldName):
            obj.setContentType('text/html', fieldName)

##/code-section FOOT
