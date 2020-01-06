1. Présentation fonctionnelles
=============================

En quoi consiste l’outil ?

| 

L’application **Urban** permet d’assurer la gestion administrative des
types de dossiers suivants :

-  Permis d’urbanisme
-  Permis d’urbanisation
-  Déclarations
-  Divisions
-  Lettres de notaires
-  Certificats d’urbanisme 1 et 2
-  Déclarations environnementales.

| 

| En outre, il est possible de générer l’exportation de la liste 220
  ainsi que les statistiques INS.
| Intégrant une cartographie, l’outil permet de visualiser les parcelles
  sélectionnées dans le permis ainsi que les parcelles concernées lors
  d’une enquête dans un rayon de 50 mètres. Une cartographie
  indépendante est également accessible afin de permettre à d’autres
  services de la commune de l’’utiliser.

2. Prérequis utilisateur
========================

| 
| Afin de pouvoir utiliser correctement l’application, il est nécessaire
  d’installer et configurer différents outils sur le poste de
  l’utilisateur:

-  un navigateur efficace
-  un outil bureautique adapté avec des macros spécifiques
-  une extension d’édition externe pour Plone
-  les préférences de l’utilisateur à appliquer

| 
| Tout ceci est à configurer suivant les spécifications précisées pour
  l’\ `installation côté
  client <https://www.imio.be/support/documentation/manual/urban-installation/installation-cote-client>`__.
|  

3. Utilisation d’urban
======================

Manuel pour l’agent traitant (urban editor)

3.1. Créer un permis
====================

3.1.1. Exemple: créer un nouveau permis d’urbanisme
===================================================

Voici les différents écrans, par onglet, qui apparaissent lors de
l’ajout ou l’édition d’un permis :
1. Onglet Récapitulatif
Permis d&rsquo;urbanisme - ajout.png
Les champs obligatoires sont marqués par un carré rouge. La plupart des
listes étant configurable, n’hésitez pas à lire
la\ `documentation <https://www.imio.be/support/documentation/manual/urban-utilisateur/utilisation-durban/les-permis-declarations-divisions-et-autres/resolveuid/d7369a8fab063734a017bd2276b5023b>`__\ concernant
la configuration des éléments liés au permis d’urbanisme.
Le bouton “Ajouter” affiche un popup permettant de choisir dans une
liste le ou les éléments souhaités, par exemple pour choisir un agent
technique ou un architecte:
Ajout agent.png
2. Onglet Voirie
Permis d&rsquo;urbanisme - ajout (voirie).png
3. Onglet Urbanisme
Permis d&rsquo;urbanisme - ajout (urbanisme).png
4. Onglet Enquête et avis
Permis d&rsquo;urbanisme - ajout (enquete et avis).png
5. Onglet PEB
\ Permis d&rsquo;urbanisme - ajout (peb).png
 

3.1.2. Compléter certaines informations du permis
=================================================

Une fois le permis créé, l’écran suivant apparaît.
On peut noter que des messages d’avertissement apparaissent au-dessus de
l’intitulé du permis. Ceux-ci stipulent, dans ce cas, qu’il est
nécessaire de renseigner les parcelles du permis et les demandeurs.
Un nouvel onglet est également affiché sur le permis (le plus à droite):
celui-ci permet de gérer toutes les étapes et documents du dossier
(\ `voir la section sur les
événements <https://www.imio.be/support/documentation/manual/urban-utilisateur/utilisation-durban/les-permis-declarations-divisions-et-autres/gerer-les-etapes-du-permis-via-longlet-evenements-du-dossier>`__\ ).
Permis d&rsquo;urbanisme - ajout (partie 2).png
L’ajout d’un demandeur se fait en cliquant sur le bouton de même nom.
La page suivante se charge, dans laquelle vous pouvez entrer les
coordonnées d’un demandeur.
La même opération peut être effectuée plusieurs fois afin de renseigner
plusieurs demandeurs pour le permis.
Permis d&rsquo;urbanisme - ajout demandeur.png
L’ajout d’une parcelle se fait en cliquant sur le bouton de même nom.
La page suivante se charge, dans laquelle vous pouvez rechercher une
parcelle suivant ses coordonnées cadastrales ou son propriétaire.
Une fois la recherche effectuée, il est nécessaire de cliquer sur le
bouton “Ajouter cette parcelle”.
La même opération peut être effectuée plusieurs fois afin de renseigner
plusieurs parcelles pour le permis.
Permis d&rsquo;urbanisme - Ajout parcelle.png
 

3.1.3. Gérer les étapes du permis, via l’onglet “Evénements du dossier”
=======================================================================

| 
| Lorsque cet onglet est sélectionné, l’écran suivant apparaît:
| |PErmis d&rsquo;urbanisme - Ajout événement.png|
| L’événement représente une étape à enregistrer dans la gestion du
  dossier.
| Lors de l’ajout ou la modification d’un événement, il est possible
  d’enregistrer différentes informations concernant l’événement: sa date
  représentative, la date de transmis, etc.
| Une fois l’événement créé, l’agent pourra associer à l’événement un ou
  plusieurs documents bureautiques.
| Afin de rajouter un événement, il faut le sélectionner dans la liste
  déroulante et cliquer sur le bouton “Ajouter un événement”.
| La liste des événements principaux est la suivante:

-  Procédure erronée (article 127)
-  Dépôt de la demande (récépissé - article 115)
-  Avis sur l’étude d’incidence
-  Récépissé d’un complément à une demande de permis (article 115)
-  Récépissé d’un modificatif à une demande de permis (article 116 - 6)
-  Dossier incomplet (avec listing des pièces manquantes - article 116 §
   1)
-  Accusé de réception (dossier complet - article 116 § 1)
-  Demande d’avis (…)
-  Transmis 1er dossier RW
-  Enquête publique
-  Rapport du Collège
-  Transmis 2eme dossier RW
-  Passage au Conseil Communal
-  Délivrance du permis (octroi ou refus)
-  Demande de raccordement à l’égout
-  Avis technique PEB
-  Début des travaux
-  Fin des travaux
-  Prorogation du permis
-  Suspension du permis
-  Enveloppes
-  Rappel implantation
-  Rappel déclaration initiale PEB
-  Rappel implantation et PEB
-  Demande irrecevable (article 159 bis)
-  Fiche récapitulative
-  Recours du demandeur contre la décision au conseil d’état
-  Recours du demandeur contre la décision au gouvernement

| 
| Une fois cliqué le bouton “Ajouter un événement”, l’écran d’édition
  apparaît:
| |Permis d&rsquo;urbanisme - Ajout dépôt de la demande|
| Suivant l’événement sélectionné, le formulaire contiendra plus ou
  moins de champs à compléter.
| Le plus courant sera la date correspondant à l’événement, dans ce cas
  la date de dépôt par exemple. 
| Dès que le formulaire est enregistré, l’écran suivant apparaît:
| |Permis d&rsquo;urbanisme - Dépôt de la demande créé|
| Les informations encodées sont affichées dans la colonne de gauche,
  partie supérieure.
| Ensuite, on trouve une liste des documents bureautiques qui peuvent
  être générés.
| En cliquant sur l’intitulé d’un document, l’application crée le
  document bureautique et ouvre l’éditeur permettant de modifier le
  contenu du document.
| Pour rappel, afin de gérer correctement les documents bureautiques, il
  est nécessaire d’avoir installé `les outils
  client <https://www.imio.be/support/documentation/manual/urban-installation/installation-cote-client>`__.
| Lors de la toute première création d’un document, Firefox demande
  comment ouvrir le document.
| |Firefox ouverture external editor|

| Il est nécessaire de choisir d’ouvrir le fichier avec “ZopeEdit” et de
  cocher “Toujours effectuer cette action pour ce type de fichier” afin
  d’enregistrer ce choix pour la suite. 
| Après avoir cliqué sur “OK”, l’éditeur bureautique (LibreOffice,
  OpenOffice ou Word) s’ouvre.

|Panneau attention 600x500| Si le document ne s’ouvre pas correctement
dans LibreOffice, vous pouvez effectuer les `réglages proposés dans
ZopeEdit <https://www.imio.be/support/documentation/manual/urban-installation/reglages-de-zopeedit-en-cas-de-probleme>`__.

| Après modification du document dans l’éditeur bureautique, il est
  nécessaire d’enregistrer le document et de fermer la fenêtre.
| Après quelques secondes apparaît alors un petit popup signifiant que
  le document a bien été enregistré dans Urban.
| |Popup external editor|
| Il suffit dès lors de cliquer sur le bouton “OK”.
| |Permis d&rsquo;urbanisme - Document récépissé créé|
| Le document modifié est bien enregistré dans l’événement et il est
  possible à tout moment de cliquer à nouveau sur l’intitulé dans le
  tableau pour le modifier.
| Si l’on revient sur le permis, dans la liste des événements, un
  tableau récapitulatif des différents événements est affiché :
| |Permis d&rsquo;urbanisme - Evénements|
| On constate qu’une liste des événements est affichée comprenant,
  en-dessous de l’intitulé de l’événement, le nom du document.
| On peut dès lors à partir de l’onglet général:

-  afficher un événement en cliquant sur son intitulé
-  modifier un document en cliquant sur son intitulé
-  clôturer un événement une fois celui-ci passé
-  modifier un événement en cliquant sur l’icône |Icône édition|
-  supprimer un événement en cliquant sur l’icône |image9|

| 
| L’intitulé de l’événement peut également être de différentes couleurs:

-  en gris, pour les événements cloturés
-  en orange, pour les événements en cours

 

3.1.4. Visualisation cartographique
===================================

| 
| La visualisation cartographique est accessible sur un permis via
  l’onglet **Carte**.
| |Onglet carte.png|
| Dans la partie supérieure sont affichées les parcelles concernées.
| Dans la partie inférieure est affichée une cartographie dynamique
  présentant la parcelle concernée.
| |Cartographie|
| La colonne de gauche présente les différentes couches qu’il est
  possible d’activer ou désactiver en les cochant ou décochant.
| La zone principale présente les couches et contient dans sa partie
  supérieure une barre d’icône (dans tous les cas, il faut cliquer sur
  l’icône pour activer la fonctionnalité avant de procéder à la suite de
  la manipulation):

-  |Icône carto - déplacer.png| : permet de déplacer la carte en “drag
   and drop”, c’est-à-dire en cliquant avec la souris, en maintenant et
   en déplaçant le curseur
-  |Icône carto - étendue départ| : zoom vers l’étendue de départ
-  |Icône carto - zoom| : option de zoom. Il faut cliquer sur la carte
   en drag and drop afin de fixer le niveau de zoom. Plus on fait une
   petite sélection, plus le niveau de zoom sera important.
-  |Icône carto - dézoom| : option de dézoom. Il faut cliquer sur la
   carte en drag and drop afin de fixer le niveau de dézoom. Plus on
   fait une petite sélection, plus le niveau de dézoom sera important.
-  |Icône carto - précédent| : revenir à la visualisation précédente. 
-  |Icône carto - suivant| : revenir à la visualisation suivante.
-  |Icône carto - mesure distance| : mesure d’une distance. Il faut
   sélectionner en cliquant sur la carte le point de départ et les
   points intermédiaires, et enfin le point final en double cliquant. La
   distance totale est alors affichée.
-  |Icône carto - mesure superficie| : mesure d’une superficie. Il faut
   sélectionner en cliquant sur la carte les sommets de la forme
   désirée, et enfin le sommet final en double cliquant. La superficie
   est alors affichée.
-  |Icône carto - information| : information sur une parcelle. Après
   avoir sélectionné une parcelle, l’information sur celle-ci est
   affichée tout en bas de la carte. Il faut cliquer sur la barre grise
   du bas afin de montrer le panneau caché.
-  |Icône carto - enquête publique| : enquête publique de 50m. Après
   avoir sélectionné une parcelle, le rayon de 50 mètres est affiché
   ainsi que les parcelles concernées. La liste des parcelles est
   affichée en bas de la carte. Il faut cliquer sur la barre grise du
   bas afin de montrer le panneau caché.
-  |Icône carto - couches| : ajout d’une couche wms. Après avoir choisi
   un serveur, il est possible de sélectionner une des couches proposées
   et de l’ajouter. Cette dernière est alors listée dans la colonne de
   gauche.
-  |Icône carto - échelle| : choix direct d’une échelle de zoom.

| 
|  

3.2. Les différentes recherches disponibles
===========================================

Par parcelle, demandeur ou rue

3.2.1. Recherche de dossiers par parcelle
=========================================

| Sur la page d’accueil, il est possible de sélectionner différentes
  recherches prédéfinies:
| |Les recherches.png|
| Dont la recherche de dossiers par parcelle:
| |Recherche par parcelle.png|
| Il est possible de sélectionner le type de permis recherché et la
  parcelle concernée.
| Le résultat est affiché en bas de page :
| |Recherche_parParcelleReulstat.png|

3.2.2. Recherche de dossiers par demandeur
==========================================

| Sur la page d’accueil, il est possible de sélectionner différentes
  recherches prédéfinies:
| |Les recherches.png|
| Dont la recherche de dossiers par demandeur:
| |Recherche par demandeur.png|
| Il est possible de sélectionner le type de permis recherché et une des
  informations indiquées concernant le demandeur.
| Le résultat est affiché en bas de page :
| |Recherche_parDemandeurResultat.png|

3.2.3. Recherche de dossiers par rue
====================================

| Sur la page d’accueil, il est possible de sélectionner différentes
  recherches prédéfinies:
| |Les recherches.png|
| Dont la recherche de dossiers par rue:
| |Recherche par rue.png|
| Il est possible de sélectionner le type de permis recherché et la rue
  concernée.
| Le résultat est affiché en bas de page :
| |Résultat recherche par rue.png|

3.3. Les fonctionnalités additionnelles
=======================================

Export 220, statistiques INS

3.3.1. Exportation liste 220
============================

Générer la liste 220 pour Urbain
--------------------------------

Cette procédure permet de générer un fichier **.xml** qui doit ensuite
être importé dans l’application **Urbain** du SPF Finances. Voici la
marche à suivre pour récupérer ce fichier :

1. Sélectionner une procédure (par exemple: Permis d’urbanisme CODT) :

|image31|

2. Afficher les filtres avancés :

|image32|

3. Choisir un intervalle de dates de décision :

|image33|

Note: cette date de décision correspond à la date encodée sur
l’événement “Délivrance du permis (octroi ou refus)” (nom par défaut).

4. Cliquer sur Liste 220 en bas à droite des filtres afin de la générer
:

|image34|

Une fois cliqué, un fichier .xml se télécharge. Il suffit ensuite
d’importer le fichier dans Urbain (SPF Finances).

Descriptif des erreurs
----------------------

Si une page d’erreur apparait comme suit au lieu de télécharger un
fichier :

|image35|

Ca signifie que certains dossiers listés manquent d’informations
essentielles à la liste 220, et le fichier ne peut donc pas être généré
tant que ces informations ne sont pas encodées.

Voici un descriptif des erreurs possibles et leur résolution :

-  **no applicant found** : Il n’y a pas de demandeur renseigné sur le
   dossier.
-  **no parcel found** : Il n’y a pas de parcelle(s) renseignée(s) sur
   le dossier.
-  **unknown worktype** : Le champ “Nature des travaux” n’a pas été
   renseigné. Ce champ se trouve dans Récapitulatif (à modifier par un
   agent technique) :

|image36|

-  **no street (with code) found** : La rue sélectionnée comme adresse
   des travaux ne possède pas de code INS associé. C’est à modifier dans
   la liste des rues dans “configuration urban” -> “Rues” (à modifier
   par une personne ayant accès à la configuration, rôle
   **urban_manager**) :

|image37|

 

Si une autre page d’erreur apparait, veuillez nous contacter.

3.3.2. Echéancier
=================

| 
| L’échéancier est accessible via la page d’accueil d’Urban, dans la
  colonne du milieu.
| |image38|
| Dans l’échéancier sont affichés des permis pour lesquels une étape de
  traitement comporte une échéance.
| A ce niveau l’échéancier prend en compte tous les permis créés.
| Une fois le lien “Echéancier” cliqué, l’écran suivant apparaît:
| |image39|
| A gauche sont listées les vérifications effectuées. Une vérification
  est donc une étape de traitement comportant unee échéance.
| Il est possible de filtrer le résultat en cochant ou décochant
  certaines vérifications.
| A droite est affiché le résultat des différentes vérifications.
| La colonne statut indique un décompte de jours par rapport à
  l’échéance.

-  En noir, le statut indique que l’étape du permis suit son cours
   normal.
-  En orange, il indique que l’étape du permis arrive bientôt à
   échéance.
-  En rouge, il indique que l’étape du permis est à échéance ou en
   retard.

| 
| Par défaut, une étape passe en mode “avertissement” lorsqu’il reste
  moins de 10 jours pour la finir.
| Ce paramètre peut être adapté dans la configuration.
|  

3.4. Gérer les architectes, notaires et géomètres
=================================================

3.4.1. Gérer les architectes
============================

Gestion des architectes

| 
| La page d’accueil contient dans sa partie droite les liens suivants:
| |Gérer.png|
| En cliquant par exemple sur le lien “Gérer les architectes”, le
  tableau suivant reprenant la liste des différents architectes déjà
  encodés apparaît.
| |Architectes.png|
| Plusieurs actions sont possibles:

-  Ajouter un architecte via le bouton de même nom
-  Activer ou désactiver un architecte: un architecte activé peut être
   lié à un permis
-  Visualiser les détails d’un architecte, en cliquant sur son intitulé
-  Modifier un architecte, en cliquant sur le petit crayon à droite
-  Effacer un architecte, en cliquant que la  croix à droite (une
   confirmation est toujours demandée lorsqu’on efface quelque chose)

| 
| Lorsqu’un architecte ne doit plus être utilisé pour les nouveaux
  permis (retraite, décès ou autre), il faut le désactiver (et non le
  supprimer) afin que les permis existants soient toujours cohérents.
| Lorsqu’on clique sur l’intitulé d’un architecte, toutes les
  informations le concernant sont affichées, tel que montré ci-dessous:
| |Architecte_view.png|
| Si l’on veut modifier ces informations, soit en cliquant sur le crayon
  du premier écran, soit en cliquant sur l’onglet “Modifier” de la vue
  de l’architecte, l’écran suivant apparaît:
| |Architecte_edit.png|
| A noter qu’il est possible d’importer une liste d’architectes et
  autres à partir d’un fichier csv. Pour se faire, veuillez-vous
  adresser à votre administrateur du logiciel (le tutoriel à ce sujet se
  trouve à cet
  `endroit <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configuration/importation-liste>`__).
| Concernant les architectes, il est prévu par la suite de synchroniser
  la liste avec l’Ordre des Architectes…
|  

4. Configuration d’urban
========================

4.1. Configurer Urban
=====================

Comment configurer l’application: champs utilisés dans les permis,
modèles de documents, vocabulaire, options diverses, …

4.1.1. Comment accéder à la configuration d’urban?
==================================================

| Depuis la page d’accueil de l’application cliquer sur le lien
  Configuration de ‘urban’.
| Attention que ce lien n’apparait que pour les personnes ayant le rôle
  “urban manager”.

| 
| |lien-urban_cfg|

4.1.2. Activer/désactiver les champs de données des permis
==========================================================

Introduction
------------

Un permis se présente sous la forme de données réparties dans 3 ou 4
onglets (récapitulatif, voirie, urbanisme, enquête). Certaines de ces
données sont indispensables comme l’objet du permis ou l’adresse du bien
concerné, d’autres n’ont peut-être aucune utilité pour vous et devraient
disparaitre.

Il est possible de configurer quels champs de données doivent apparaitre
pour chaque type de permis.

Exemple:
--------

| En exemple, voyons comment désactiver les champ ‘Zonage au plan de
  secteur’ et ‘Détails concernant le zonage’ de l’onglet ‘urbanisme’ des
  permis de batir. Puis comment retirer l’onglet ‘urbanisme’ au complet.

#. Sur un permis d’urbanisme quelconque on peut voir que les champs
   ‘Zonage au plan de secteur’ et ‘Détails concernant le zonage’ sont
   présents dans l’onglet urbanisme.
#. Pour les désactiver il faut aller dans la configuration des permis
   d’urbanisme: cliquer sur ‘Paramètres des permis d’urbanisme’ depuis
   la configuration d’urban (le lien se trouve plutot dans le bas de la
   page de la configuration d’urban).
#. Ensuite cliquer sur l’onglet ‘Modifier’.

   | 
   | |image45|

#. Si on revient sur un permis d’urbanisme, on voit que les deux valeurs
   ont disparu de l’onglet ‘urbanisme’.

 

 Pour masquer l’onglet urbanisme ou voirie en entier, l’opération est la
même mais il faut déselectionner toutes les valeurs concernant l’onglet.
C’est à dire toutes les valeurs commençant par ‘(urb)’ ou ‘(voir)’

4.1.3. Configurer les listes de vocabulaires urban
==================================================

.. _introduction-1:

4.1.3.1. Introduction
=====================

Principe général
----------------

À différents endroits dans urban, il existe des listes de valeurs à
sélectionner. Pour certaines de ces listes les valeurs sont
configurables dans urban c’est à dire qu’il est possible d’ajouter de
nouvelles valeurs, d’en supprimer ou de modifier les existantes.

Voici quelques exemples de listes configurables:

-  Les titres des personnes: monsieur, madame, maitres, …(par ex: quand
   on ajoute un demandeur)
-  Pour les cu1, la liste des particularités communales du bien.
-  Pour les permis d’urbanisme, les différents types de ‘pièces
   manquantes’.
-  La liste des organismes à qui faire des demandes d’avis.
-  Les rues.
-  …

| 

Où les trouver
--------------

On remarque que certaines de ces listes sont spécifiques à des types de
permis, d’autres sont communes à tous. C’est ce critère qui détermine
l’endroit de la configuration d’urban ou l’on pourra trouver la liste de
vocabulaire à modifier. Les listes ‘communes’ se trouvent dans le bas la
page principale de la configuration d’urban tandis que les listes
propres à certains type de permis se trouvent dans les sous-dossiers
correspondants. (ex: pour configurer la liste ‘particularités communales
du bien’ des cu1, il faudra aller dans le dossier ‘Paramètres des
Certificats d’urbanisme n°1’ puis dans ‘Particularité(s) communale(s) du
bien’)

4.1.3.2. Exemple de configuration de liste de vocabulaire urban
===============================================================

L’exemple: le listing des pièces manquantes des permis d’urbanisme
------------------------------------------------------------------

Si on prend un permis d’urbanisme quelconque et qu’on édite le
récapitulatif (cliquer sur le crayon de l’onglet ‘récapitulatif’).

|image46|

| 
| On voit le listing des pièces manquantes.
| |image47|

Où configurer les valeurs.
--------------------------

Les pièces manquantes diffèrent pour chaque type de permis, il faut donc
aller dans la configuration des permis d’urbanisme (le lien se trouve
dans le bas de la page de la configuration d’urban).

| |goto-pu-cfg|
| Ensuite aller dans le dossier ‘Liste des pièces nécessaires pour gérer
  les pièces manquantes’.

| |image49|
|  

Comment modifier les valeurs ?
------------------------------

-  .. rubric:: Retirer une valeur
      :name: retirer-une-valeur

#. Pour retirer une ou plusieurs valeurs. Cliquer sur l’onglet
   ‘Contenus’ et sélectionner toutes les valeurs qui devront être
   retirées.
#. Ensuite cliquer sur ‘changer l’état’.
#. Et pour finir, aller dans le bas du formulaire et sélectionner
   ‘Désactiver’ puis cliquer sur enregistrer.

-  .. rubric:: Ajouter une valeur
      :name: ajouter-une-valeur

#. Pour ajouter une nouvelle valeur. Cliquer sur l’onglet ‘Ajout d’un
   élément’ (en haut à droite) et sélectionner ‘Terme de vocabulaire
   urban’.
#. Écrire la nouvelle valeur dans le champ ‘Titre’ (par exemple ‘Ma
   nouvelle pièce manquante’) puis enregistrer. Si vous avez un doute
   sur les champs à remplir, regardez une autre valeur et éditez la sans
   la modifier pour voir quelles sont les différentes valeurs et
   l’endroit où elles sont encodées (Titre, Observations, Valeur
   supplémentaire, …).

-  .. rubric:: Modifier une valeur
      :name: modifier-une-valeur

#. Pour modifier une valeur existante. Cliquer sur la valeur à modifier
   puis sur l’onglet ‘Modifier’.
#. Changer le contenu des différents champ à sa convenance puis cliquer
   sur ‘Enregistrer’.

4.1.3.3. Les listes ‘spéciales’ d’urban.
========================================

| La plupart des listes configurables d’urban sont des dossiers
  contenants des objets ‘termes de vocabulaire urban’ comme dans
  l’exemple précédent.
| Cependant il existe des listes qui contiennent d’autres types d’objet
  et/ou dont il est préférable de connaitre les spécificités avant de
  les modifier.
| Ces listes sont:

-  Les rues (config générale d’urban)
-  Les demandes d’avis (config spécifique aux permis)
-  Les agents traitants (config générale d’urban)
-  Les types d’événements (config spécifique aux permis)

 

#. Les rues.

#. Les demandes d’avis.

   Voir également `configurer les événements de demandes
   d’avis <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/configurer-les-evenements-durban/les-evenements-de-demandes-davis>`__.

#. Les agents traitants font l’objet d’une documentation spécifique
   lisible
   `ici <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/ajouter-un-agent-traitant>`__.

#. Idem pour les type d’événements, ils font l’objet d’une documentation
   lisible
   `ici <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/configurer-les-evenements-durban>`__.

4.1.4. Configurer les événements d’urban.
=========================================

Comment modifier les événements, en supprimer ou en ajouter.

.. _introduction-2:

4.1.4.1. Introduction
=====================

Rappel
------

Un bref rappel sur les événements: ce sont les objets qui représentent
les différentes étapes par lesquelles passe un permis. Ils sont
ajoutables via l’onglet ‘Événements du dossier’ du permis depuis une
liste déroulante.  Chaque événement contient au minimum une date
indiquant quand il s’est produit et possède un nombre variable de
documents à générer qui lui sont liés.

Que peut on configurer sur les évémenents:
------------------------------------------

-  Ajouter de nouveaux événements dans la liste, avec leur propres
   modèles de documents à générer.
-  Retirer des événements inutiles de la liste.
-  Changer l’ordre dans lequel ils apparaissent.
-  Mettre des conditions sur l’apparition des événements dans la liste.
   Par exemple: l’événement ‘Dossier complet’ ne peut pas apparaitre
   dans la liste avant que l’événement ‘Dépôt de la demande’ ait été
   créé.
-  Ajouter/supprimer les champs d’un événement (une date supplémentaire,
   un champ contenant la décision,…).
-  Changer les délais et délais d’alerte de l’événement.
-  Activer la notion d’événement clé dans l’affichage des permis.
-  Ajouter/supprimer des modèles de documents à générer pour un
   événement donné.

| 

Où les configurer
-----------------

| Les événements sont configurables à travers les objets ‘types
  d’événements’. Ceux-ci se trouvent dans les dossiers nommés ‘Types
  d’événements’ qui sont présents dans chaque dossier de configuration
  de chaque type de permis.

Par exemple pour configurer l’événement ‘Récépissé de la demande’ des
permis d’urbanisme il faut `aller dans la configuration
d’urban <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/comment-y-acceder>`__,
puis dans ‘Paramètres des permis d’urbanisme’.

|goto-pu-cfg|

Puis dans ‘Types d’événements’.

| |image50|
| Et finalement dans ‘Dépôt de la demande (récépissé - article 115)’ .

|image51|

 

4.1.4.2. Ajouter/supprimer des événements
=========================================

Avant d’aller plus loin, il faut distinguer deux cas: celui des
événements de type ‘demande d’avis à  XXX’ et celui des autres
événements. Pour les demandes d’avis, c’est par ici que ça se passe.

L’exemple: un nouveau type d’événement pour les déclarations
------------------------------------------------------------

Nous allons créer un nouvel événement ‘suicide de mon 14ème
psychanaliste’ ajoutable pour les déclarations urbanistiques et ensuite
voir comment le supprimer.  Une fois créé, il devra apparaitre dans la
liste des événements ajoutables pour n’importe quelle déclaration.

| |image52|
|  

Où gérer les configurations d’événements
----------------------------------------

Pour notre exemple, comme nous travaillons sur les déclarations,  il
faut se rendre dans la configuration des déclarations urbanistiques (le
lien se trouve dans le bas de la page de `la configuration
d’urban <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/comment-y-acceder>`__).

|image53|

Ensuite aller dans le dossier ‘Types d’événements’.

| |urbaneventtypes-cfg|
|  

Ajouter un nouveau type d’événement
-----------------------------------

#. Cliquer sur l’onglet ‘Ajout d’un élément’ (en haut à droite) et
   sélectionner ‘Type d’événement du dossier’.
#. Un formulaire apparait avec différents champs:
#. Cliquer sur enregistrer en bas de la page pour ajouter ce nouveau
   type d’événement.

Si l’on se rend dans l’onglet ‘Événéments du dossier’ d’une déclaration
quelconque, on peut voir que ce nouvel événement apparait dans la liste
de ceux qui peuvent être ajoutés.

| |image55|
|  

 Retirer un événement
---------------------

| Comment désactiver le type d’événement ‘suicide de mon 14ème
  psychanaliste’ que nous venons de créer.

#. Cliquer sur l’onglet ‘Contenus’
#. Sélectionner tous les événements à désactiver. Dans notre cas, il n’y
   en a qu’un. Puis cliquer sur ‘Changer l’état’.
#. Et pour finir, aller dans le bas du formulaire et sélectionner
   ‘Désactiver’ puis cliquer sur enregistrer.

| La configuration de l’événement apparait désormais en rouge: il a été
  désactivé d’urban et n’apparaitra plus dans les événements disponibles
  des déclarations. L’avantage de la désactivation comparé à la
  suppression est que l’on peut réactiver l’événement si besoin en est.

4.1.4.3. Configurer les champs apparaissant dans un événement
=============================================================

| Par défaut, un événement contient au minimum un champ de date qui ne
  peut pas être enlevé. Mais il se peut que certains événements aient
  besoin de champs supplémentaire ou qu’un de ces champs ne soit pas
  utilisé et doive être retiré. Ces champs sont utiles car c’est aussi à
  partir des valeurs qu’ils contiennent que l’on génére les documents
  administratifs automatiquement.

Exemple: Changer les champs de l’événement ‘Avis technique’ des déclarations
----------------------------------------------------------------------------

| 

L’événement ‘avis technique’ contient deux champs de dates: la date de
retour souhaitée et la date de transmis. Nous allons retirer le champ
‘date de transmis’ et ajouter deux nouveaux champs ‘avis’ et ‘texte de
l’avis’.

|image56|

| 

#. `Se rendre dans la configuration
   d’urban <http://imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/comment-y-acceder>`__
   puis aller dans ‘Paramètres des déclarations’, ensuite dans ‘Type
   d’événements’ et finalement dans ‘Avis technique’.
#. Cliquer sur l’onglet ‘Modifier’
#. Ensuite, dans le formulaire, chercher la zone ‘Champ(s) activé(s)’.
   Mettre à droite la valeur ‘date de transmis’ et mettre à gauche les
   valeurs ‘avis’ et ‘texte de l’avis’.
#. Pour finir, cliquer sur enregistrer (bas de la page). Tous les
   événement ‘Avis technique’ des déclarations contiennent à présent les
   champs ‘avis’ ainsi que ‘texte de l’avis’ et n’ont plus le champ
   ‘date de transmis’.

| 

4.1.4.4. Ajouter, retirer ou modifier les modèles de documents à générer sur un événement
=========================================================================================

L’exemple
---------

La plupart des événements contiennent un ou plusieurs documents à
générer.  L’image ci dessous montre les deux documents liés à
l’événement ‘Transmis décision au FD et demandeur’ d’une déclaration
urbanistique.

|image57|

| Comment compléter cette liste avec de nouveaux documents à générer,
  retirer des documents inutiles ou les modifier?
|  

Où gérer les modèles de documents d’un événement
------------------------------------------------

Comme l’exemple choisi porte sur un événement des déclarations il faut
se rendre dans la configuration des déclarations urbanistiques (le lien
se trouve dans le bas de la page de `la configuration
d’urban <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/comment-y-acceder>`__).

|image58|

Ensuite aller dans le dossier ‘Types d’événements’.

|urbaneventtypes-cfg|

Et finalement dans ‘Transmis décision au FD et demandeur’.

|image59|

Ajouter un modèle de document à générer
---------------------------------------

En exemple, j’ai créé un modèle de document appelé ‘yaourt.odt’ et je
l’ai enregistré sur le bureau de mon ordinateur. Pour l’ajouter aux
modèles de l’événement il faut:

#. Cliquer sur l’onglet ‘Ajout d’un élément’ (à droite) et sélectionner
   ‘Fichier’.
#. Remplir le titre avec le nom du document tel que vous voudriez qu’il
   apparaisse dans la liste et cliquer sur ‘Browse…’.
#. Aller chercher le modèle de document là où il est enregistré sur
   votre ordinateur puis cliquer sur ‘Enregistrer’.
#. On constate que le modèle est ajouté avec les autres et si on va sur
   l’événement ‘Transmis décision au FD et demandeur’ d’une déclaration
   urbanistique, on constate qu’il apparait bien dans le liste des
   documents à générer pour cet événement.

Retirer un modèle de document
-----------------------------

Il existe deux manières de retirer un modèle: la désactivation et la
supression. La désactivation permet de garder le modèle dans la
configuration d’urban mais ne le propose plus dans la liste des
documents à générer tandis que la supression est l’option plus radicale
puisqu’elle efface définitivement le modèle d’urban.

Dans les deux cas il faut:

#. Cliquer sur le modèle que l’on veut retirer (ils se trouvent en bas
   de la page de la configuration de l’événement).
#. Cliquer sur l’onglet ‘Activé’ et sélectionner l’option ‘Désactiver’
   si on veut juste le désactiver.
#. S’il a été désactivé, le nom du modèle est à présent affiché en
   rouge. S’il a été supprimé, le nom a disparu de la liste. Mais dans
   les deux cas on peut vérifier sur une déclaration urbanistique que ce
   modèle n’apparait plus dans la liste des documents à générer pour
   l’événement ‘Transmis décision au FD et demandeur’.

Modifier un modèle de document
------------------------------

Le manuel ci-dessous n’explique que comment accéder à un document pour
le modifier et à enregistrer ces changements. Pour de plus amples
informations sur tous les changements possibles et apprendre à faire ses
propres modèles, se référer à comment `adaper les modèles
d’urban <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/adapter-les-modeles-de-documents-urban>`__.

Pour modifier un modèle il faut:

#. Se rendre sur le type d’événement où le modèle est contenu. Les noms
   des modèles d’un type d’événement apparaissent dans le bas de la page
   (s’il en contient). Cliquer sur le nom du modèle que l’on veut
   éditer.
#. Ensuite cliquer sur ‘Modifier avec une application externe’.
#. Normalement libreoffice ou openoffice doit se lancer, le document s’y
   ouvre et est éditable. Si ça ne se passe pas aussi bien, se référer à
   l’\ `installation coté
   client <https://www.imio.be/support/documentation/manual/urban-installation/installation-cote-client>`__
   d’urban
#. Faire les modifications voulues puis enregistrer les changements dans
   libre office avant de quitter. Si tout se passe bien, un popup
   signalant la fin de l’édition externe apparait. Les changements sur
   le document ont bien été enregistrés dans urban.

| 

4.1.4.5. Changer l’ordre des événements
=======================================

L’ordre dans lesquel les événements apparaissent dans la liste des
événements ajoutables d’un permis est déterminé par l’ordre des objets
‘type d’événement’ dans la configuration.

+-----------------------------------+-----------------------------------+
| Liste des événements dans un      | Liste des types d’événements dans |
| permis                            | la configuration d’urban          |
+-----------------------------------+-----------------------------------+
| |image62|                         | |image63|                         |
+-----------------------------------+-----------------------------------+

 

En exemple nous allons changer l’ordre des évéments des déclarations.

#. `Se rendre dans la configuration
   d’urban <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/comment-y-acceder>`__
   puis aller dans ‘Paramètres des déclarations’  et finalement dans
   ‘Type d’événements’.
#. Cliquer sur l’onglet contenu.
#. Changer l’ordre des types d’événements en cliquant sur l’image
   |image64| de la 1ère colonne. Maintenir le clique enfoncé et bouger
   l’élément à la place voulue.
#. Si on revient sur l’onglet ‘Voir’ on constate que le nouvel ordre est
   conservé. Et si on rafraichit la page de déclaration d’exemple dans
   le navigateur, on voit que la liste des événements ajoutables est
   dans ce nouvel ordre.

| 

4.1.4.6. Condition d’apparition des événements
==============================================

.. _introduction-3:

Introduction
------------

Il est possible de configurer les événements de telle sorte qu’ils
n’apparaissent dans la liste des événements ajoutables d’un permis que
sous certaines conditions. Par défaut, tous les événements (à
l’exception des événements de demande d’avis) y sont présents.

Dans la configuration d’un événement il y a un champ ’Condition TAL’
(vide par défaut) dans lequel on peut écrire une expression en langage
Python. Cette expression est évaluée au moment de générer la liste des
événements disponibles à l’ajout. Si elle est vraie alors l’événement
est ajouté à la liste, sinon il n’y apparait pas.

L’avantage de ce système est qu’il offre une grande liberté au niveau
des conditions qui peuvent être mises sur chaque événement. Le
désavantage est qu’il faut bien connaitre l’application ainsi que le
langage python pour être capable de traduire la condition depuis le
francais en une expression python. Donc à priori, il faut s’adresser au
support de communesplone (via un ticket du trac, en atelier ou sur le
forum) pour configurer ce paramètre.

| Cependant, voici quelques exemples de conditions simples à
  copier/coller qui permettront aux plus débrouillards de s’en tirer
  tout seul.
| Ces exemples sont:

-  L’événement B apparait dans la liste si et seulement si l’événement A
   a été créé.
-  L’événement B doit disparaitre de la liste une fois créé.
-  L’événement B doit disparaitre de la liste une fois que l’événement C
   a été créé.
-  Comment combiner ces conditions ensembles.

Exemple 1: l’événement A apparait dans la liste si l’événement B a été créé.
----------------------------------------------------------------------------

De manière concrète, cet exemple sera illustré avec : l’événement ‘avis
technique’ d’une déclaration ne peut apparaitre que si le dépot de la
demande a été fait.

#. `Se rendre dans la configuration
   d’urban <http://imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/comment-y-acceder>`__
   puis aller dans ‘Paramètres des déclarations’, ensuite dans ‘Type
   d’événements’ et finalement dans ‘Avis technique’.
#. Cliquer sur l’onglet ‘Modifier’.
#. Dans le champ ‘Condition TAL’, mettre le texte suivant:
#. Cliquez sur enregistrer (en bas de la page) pour finir. Vous pouvez à
   présent vérifier sur n’importe quelle déclaration, via l’onglet
   ‘Evénements du dossier’, que l’événement ‘Avis technique’ apparait ou
   n’apparait pas selon qu’il y ait un événement ‘dépot de la demande’
   déjà créé.

| 

Exemple 2: l’événement A disparait de la liste une fois créé.
-------------------------------------------------------------

| De manière concrète, cet exemple sera illustré avec : l’événement
  ‘Avis technique’ disparait une fois créé.
| Il suffit de reprendre toutes les étapes de l’exemple précédent mais
  cette fois, dans la ‘Condition TAL’ il faudra mettre:

python: licence.hasNoEventNamed(event.Title())

| Cette expression est valide telle quelle etfonctionne pour n’importe
  quel événement.
|  

Exemple 3: l’événement A disparait de la liste une fois que l’événement B est créé.
-----------------------------------------------------------------------------------

| De manière concrète, cet exemple sera illustré avec : l’événement
  ‘Avis technique’ disparait de la liste dès que la délibération du
  collège est créée.
| Il suffit de reprendre toutes les étapes de l’exemple 1 mais cette
  fois, dans la ‘Condition TAL’ il faudra mettre:

python: licence.hasNoEventNamed([’Délibération collège’])

| De la même manière, si on remplace le titre ‘Délibération collège’ par
  celui d’un autre événement, la condition se fera selon cet autre
  événement.

Exemple 4: combiner les conditions.
-----------------------------------

| Pour créer une combinaison des conditions précédentes il suffit de
  reprendre tout le texte XXX qui vient avant le mot ‘python:’ et de les
  combiner avec les mots clés ‘and’ ou ‘or’.
| Exemple si je reprends les condition de l’exemple 1 et 2 et que je
  veux les combiner, càd que je veux que l’avis technique n’apparaisse
  dans la liste que si le dépot de la demande est fait et qu’il
  disparaisse une fois créé alors j’ai les deux conditions suivantes:

“python: licence.hasEventNamed([’Dépôt de la demande’])” et "python:
licence.hasNoEventNamed(event.Title())"

+-----------------------------------+-----------------------------------+
| Pour les combiner il suffit de    | python:                           |
| commencer                         |                                   |
| ma nouvelle condition par         |                                   |
| ‘python:’.                        |                                   |
+-----------------------------------+-----------------------------------+
| Puis d’y ajouter tout le contenu  | python:                           |
| qui suit le                       | licence.hasEventNamed([’Dépôt de  |
| mot ‘python:’ de la première      | la demande’])                     |
| expression.                       |                                   |
+-----------------------------------+-----------------------------------+
| D’y ajouter le mot clé ‘and’ qui  | python:                           |
| signifie ‘et’ .                   | licence.hasEventNamed([’Dépôt de  |
|                                   | la demande’]) and                 |
+-----------------------------------+-----------------------------------+
| Et de finir en ajoutant tout ce   | python:                           |
| qui suit le                       | licence.hasEventNamed([’Dépôt de  |
| mot ‘python:’ de la deuxième      | la demande’]) and                 |
| expression.                       | licence.hasNoEventNamed(event.Tit |
|                                   | le())                             |
+-----------------------------------+-----------------------------------+

|  
| En résumé:
| ‘python: XXX’ et ‘python: YYY’ devient ‘python: XXX and YYY’
| De même s’il faut mixer plus de deux conditions :
| ‘python: XXX’ ou ‘python: YYYY’ ou ‘python: ZZZ’  devient ‘python: XXX
  or YYY or ZZZ’ .

 

4.1.4.7. Les événements de demandes d’avis
==========================================

.. _introduction-4:

Introduction
------------

Les événements représentants les demandes d’avis en cas d’enquête
publique se gèrent de manière un peu différente que les autres
événements. Cela vient du fait que la notion de demande d’avis apparait
dans urban de deux manières. D’une part dans l’onglet “enquête publique”
de certains types de permis, où l’on peut cocher les organismes devant
renvoyer un avis. D’autre part dans l’onglet “Événements du dossier” ou
les demande d’avis selectionnées dans l’enquête publique doivent
apparaitre dans la liste des événements ajoutables. Il faut que
l’information entre les deux soit cohérente. En effet les valeurs de la
liste dans l’onglet ‘enquête publique’ sont gérées via les termes de
vocabulaire urban, tandis que les événements sont gérés via les “types
d’événements” de la configuration d’urban.  Pour pouvoir faire un lien
entre les deux, les termes de vocabulaire des demandes d’avis
contiennent une référence vers le type d’événement qui lui correspond.
Par exemple: le terme de vocabulaire “Belgacom” qui est dans le dossier
“Demandes d’avis” de la config des permis d’urbanisme contient une
référence vers le type d’événement “Demande d’avis (Belgacom)” qui lui
est dans le dossier “Types d’événements”.

Conclusion: si on ajoute, supprime ou modifie un élément d’un coté, il
faut s’assurer que l’autre coté soit bien mis à jour de manière
cohérente.

Les demandes d’avis se distinguent aussi par leur gestion des modèles de
document. Par défaut un type d’événement de demande d’avis ne contient
aucun modèle et tant que c’est le cas c’est le modèle du type
d’événement “\***Demande d’avis CONFIG**\*” qui est utilisé à la place.
Ce qui signifie que par défaut, il y a un modèle unique de document pour
toutes les demandes d’avis. Ce manuel explique également comment
modifier le modèle d’une demande d’avis.

Ajouter une demande d’avis
--------------------------

C’est toujours par le dossier “Demande d’avis” qu’il faudra passer et
jamais via le dossier “Type d’événements”. En effet, une mécanique est
prévue pour automatiquement créer un “type d’événement” de demande
d’avis dès que l’on crée un nouveau terme de vocabulaire “demande
d’avis”.

En exemple nous allons ajouter une valeur “demande d’avis à mon voisin
de gauche” dans le dossier “demandes d’avis” des permis d’urbanisme et
voir qu’un événement “Demande d’avis (voisin de gauche)” a bien été créé
et lié au terme de vocabulaire.

|goto-pu-cfg|

|image66|

|image67|

#. Se rendre dans `la configuration
   d’urban <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/comment-y-acceder>`__,
   puis aller dans “Paramètres des permis d’urbanisme”.
#. Aller dans le dossier “Demandes d’avis”.
#. Cliquer sur l’onglet “Ajout d’un élément” et sélectionner
   “OrganisationTerm”.
#. Remplir le titre avec le nom de l’organisme et mettre son adresse
   dans le champ “Observations”. Puis finir en cliquant sur enregistrer
   dans le bas du formulaire.

| 
| Sur le terme de vocabulaire fraichement créé on peut voir qu’il y a un
  lien “Événement de demande d’avis lié”.

| |image68|         |image69|
| Si on clique dessus on arrive dans le type d’événement “Demande d’avis
  (Voisin de gauche)” qui vient d’être créé dans le dossier “Type
  d’événements”.

| |image70|
|  

Retirer une demande d’avis
--------------------------

C’est exactement pareil que pour un terme de vocabulaire ou que pour un
événement classique. On peut soit désactiver ou soit supprimer la
demande d’avis mais il faut faire de même avec l’événement
correspondant. Pour l’instant, il n’y a pas de mécanisme qui gère
automatiquement la supression ou la désactivation de l’un en fonction de
l’autre.

|opinion-request|

|disable|

Cliquer sur l’onglet “Actions” et sélectionner “Supprimer” si on veut
l’effacer complètement.

|delete|

#. Se rendre dans le dossier “Types d’événements”. Cliquer sur la
   demande d’avis que l’on veut retirer.
#. Cliquer sur l’onglet “Activé” et sélectionner l’option “Désactiver”
   si on veut juste la désactiver.
#. Faire de même avec le terme de vocabulaire correspondant du dossier
   “Demandes d’avis”.

Modifier une demande d’avis
---------------------------

Cela se fait de la même manière que pour un événement ou un terme de
vocabulaire normal: en cliquant sur l’onglet “Modifier” de l’élément que
l’on veut changer.

|modify-pu-cfg|

| Le seul élément auquel il fait faire attention est le titre. Si on
  modifie le titre de l’un, il faut s’assurer que le titre de l’autre
  change de la même manière.
|  

Modifier les modèles de documents des demandes d’avis
-----------------------------------------------------

Comme précisé dans l’introduction, les type d’événements de demandes
d’avis ne contiennent aucun modèle de document et que c’est dans le type
d’événement “\***Demande d’avis CONFIG**\*” que se trouve le modèle par
défaut pour TOUTES les demandes d’avis.

Donc si l’on veut modifier le modèle par défaut pour toutes les demandes
d’avis, il faut se rendre dans le dossier “Types d’événements” puis dans
“\***Demande d’avis CONFIG**\*” et y `modifier le
modèle <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/configurer-les-evenements-durban/ajouter-supprimer-des-documents-a-generer-sur-un-evenement>`__
“Courrier de demande d’avis”.

Si l’on veut personnaliser le modèle d’une seule demande d’avis pour le
rendre différent des autres, il suffit de lui `créer un
modèle <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/adapter-les-modeles-de-documents-urban>`__
“Courrier de demande d’avis” puis de
`l’ajouter <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/configurer-les-evenements-durban/ajouter-supprimer-des-documents-a-generer-sur-un-evenement>`__
dans le type d’événement de la demande d’avis.

| 

4.1.5. Ajouter un agent traitant
================================

Pré-requis:
-----------

| Pour qu’un agent de l’urbanisme (en chair et en os)  puisse travailler
  sur l’application urban, il faut :
| -D’une part qu’il ait un login et un mot de passe d’utilisateur plone.

-D’autre part que cet utilisateur plone (virtuel) ait été lié à un
profil d’agent traitant urban (virtuel lui aussi).

Ce document explique comment un utilisateur étant au minimum ‘urban
manager’ peut créer un le profil d’agent traitant urban et le lier à un
utilisateur plone existant. Mais il faut savoir que créer un utilisateur
plone n’est faisable que par un administrateur du site. Si c’est le cas,
se référer à `ce
manuel <https://www.imio.be/support/documentation/tutoriels/gerer-les-utilisateurs-les-roles-les-permissions-et-le-workflow-2.5/gestion-des-utilisateurs-et-groupes>`__
pour en savoir plus. (C’est aussi lors de cette étape préliminaire que
l’utilisateur plone sera mis dans le(s) groupe(s) ‘urban manager’,
‘urban editor’ ou ‘urban reader’)

Comment créer un agent traitant urban?
--------------------------------------

#. Il faut se `rendre dans la configuration
   d’urban <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/comment-y-acceder>`__.
   Puis aller dans le dossier ‘agents traitants’
#. Ensuite cliquer sur ‘Ajout d’un élément’ (en haut à droite) et
   sélectionner ‘Gestionnaire de dossier’.
#. Remplir le formulaire avec les données correspondantes à l’agent.
   Dans le champ ‘Identifiant de l’utilisateur Plone lié’ , il faut
   mettre (oh surprise..) l’identifiant de l’utilisateur plone auquel on
   veut lier le profil d’agent traitant. Et ensuite cocher les types de
   permis gérables par ce dernier.

4.1.6. Adapter les modèles de documents urban
=============================================

.. _principe-général-1:

4.1.6.1. Principe général
=========================

.. _introduction-5:

Introduction
------------

Le principe des documents d’urban est le suivant: chaque document est
créé à partir d’un modèle (template). Un modèle est un fichier .odt
(l’équivalent libre du format .doc) qui contient un mélange de texte
normal et d’instructions du langage de programmation python. Au moment
de la génération, le code python est exécuté et remplacé par la valeur
qu’il représente de sorte que le document créé ne contienne finalement
que du texte personnalisé en fonction du contexte où il a été généré. 
Le modèle est donc comme la plaque d’une presse d’imprimerie de laquelle
sortent les documents générés. Pour un seul modèle, on génére autant de
documents que l’on veut.

Les modèles se situent au niveau de la configuration d’urban et plus
précisément dans chaque configuration d’événement. Les modèles sont
uniques par type de permis. Les documents générés, eux, se trouvent dans
les événements créés dans tous les différents permis.

La mise à jour automatique
--------------------------

Les modèles de base d’urban sont en théorie suffisamment ‘corrects’ pour
être utilisés tels quels. L’avantage est que ces modèles par défaut sont
réécrits par les développeurs d’imio en fonction de l’évolution de la
législation urbanistique et de la correction de bugs puis
automatiquement mis à jour sur l’application urban. Dès qu’un modèle est
modifié à la main, les mises à jours ne sont plus appliquées sur
celui-ci mais simplement signalées et c’est au responsable d’urban de la
commune d’adapter le modèle manuellement.

Cette explication n’est pas là pour décourager la modification des
modèles (et d’ailleurs certains modèles doivent être personnalisés pour
chaque commune) mais bien d’informer des implications de ce choix.

D’autre part, il est prévu de pouvoir personnaliser certaines zones d’un
modèle sans modifier le modèle lui-même. Ces zones, comme le header et
le footer, sont elles-mêmes gérées dans des modèles à part: les `modèles
généraux <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/les-modeles-generaux>`__.

À quoi ça ressemble dans un modèle
----------------------------------

Comme expliqué précédemment, c’est un mélange de texte et de code
python.

Le code python des modèles se présente sous deux formes: les champs de
saisies (les zones grisées)

| |image75|
| et les commentaires (ici bleus mais la couleur peut varier).

|image76|

Il n’est pas important de comprendre pourquoi (c’est comme ça..) mais le
savoir est quand même utile pour la raison qui va suivre.  Il est
important de bien distinguer les commentaires d’un modèle, qui
contiennent une expression python à exécuter, des commentaires d’un
document généré, qui contiennent les messages d’erreurs en cas mauvaise
exécution de cette expression. Ces deux types de commentaires ne
signifient pas du tout la même chose. Un document généré ne doit jamais
contenir de commentaires d’erreurs, si c’est le cas, il faut le signaler
au support d’imio (via un ticket du trac ou en atelier) pour corriger
son modèle correspondant.

Un exemple de commentaire d’erreur:

| |image77|
|  

4.1.6.2. Prérequis
==================

L’édition des modèles urban requiert:

|image78|

| Sinon la dernière version du plugin est disponible
  `ici <http://svn.communesplone.org/svn/communesplone/Products.urban/trunk/src/Products/urban/OOmacros/UrbanTemplateOO/UrbanTemplateOO-0.1.oxt>`__.
  Une fois téléchargé, il suffit de double cliquer dessus pour
  l’installer.
|  

-  D’avoir `installé libreoffice,
   zopeedit <https://www.imio.be/support/documentation/manual/urban-installation/installation-cote-client>`__
   sur son ordinateur et d’avoir `autorisé l’édition
   externe <https://www.imio.be/support/documentation/manual/urban-installation/installation-cote-client>`__
   dans ses préférences personnelles.
-  D’avoir téléchargé et installé le plugin open office ‘Urban templates
   editor’ dans libreoffice/openoffice. Si c’est le cas, un bouton
   ‘appyTE’ doit être présent dans le barre de menu d’openoffice.

4.1.6.3. Accéder aux modèles et les manipuler (ajout, retrait, changement)
==========================================================================

| Voir la `gestion des modèles d’un
  événement <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/configurer-les-evenements-durban/ajouter-supprimer-des-documents-a-generer-sur-un-evenement>`__
  urban.

4.1.6.4. Changer le texte ‘normal’ d’un modèle
==============================================

Ajouter, supprimer ou modifier le texte d’un modèle est à priori une
opération sans difficulté particulière et s’il y  en a une, c’est plutôt
vers la documentation de votre logiciel de traitement de texte qu’il
faudra vous tourner. Cependant il a y un point auquel il faut être
attentif lorsqu’on ajoute du texte ou que l’on crée un modèle depuis un
document vierge: les styles.

En effet il existe un mécanisme de gestion globale des styles des
modèles d’urban (voir le fichier style des `modèles
généraux <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/les-modeles-generaux>`__)
mais pour qu’il fonctionne, il faut que les styles propres à urban
soient utilisés dans les modèles de documents. Veillez bien, par
exemple,  à ce que votre corps de texte soit toujours dans le style
‘urban body’. Idem pour les titres avec le style ‘urban title’, etc,
etc,..

Attention que comme expliqué dans l’introduction, un modèle modifié ne
sera plus jamais mis à jour automatiquement. En cas de mise à jour d’un
modèle, vous serez mis au courant des changements du nouveau modèle mais
ceux-ci ne seront pas appliqués, ce sera à vous de modifier manuellement
le modèle si besoin en est.

4.1.6.5. Changer les champ de saisie et commentaires d’un modèle
================================================================

Comme expliqué dans l’introduction, les champs de saisies et les
commentaires avec du code python sont les éléments qui récupèrent
différentes données de l’application urban pour les insérer dans le
document généré. Une extension openoffice a été développée pour en
ajouter facilement. Cette extension permet de lancer un petit menu dans
lequel on peut choisir une valeur à récupérer sur urban en fonction de
son nom en français (exemple: je veux le nom de famille du demandeur du
permis) puis de générer à un endroit du modèle le champ de saisie ou le
commentaire avec le code python correct correspondant.

Utilisation de l’extension openoffice ‘Urban templates editor’
--------------------------------------------------------------

| En exemple nous allons modifier le modèle ‘Transmis de la décision au
  demandeur’. Celui-ci fait référence à un article du cwatupe, nous
  allons compléter cette référence avec le texte de l’article lui-même.

#. Assurez vous d’avoir bien `installé ‘Urban templates
   editor’ <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/adapter-les-modeles-de-documents-urban/prerequis>`__
   sur votre logiciel de traitement de texte.
#. Le modèle ‘Transmis de la décision au demandeur’ se trouve dans `la
   configuration
   d’urban <https://www.imio.be/support/documentation/manual/urban-utilisateur/configuration-durban/configurer-urban/comment-y-acceder>`__
   -> Paramètres des déclarations -> Types d’événements -> Transmis
   décision au FD et demandeur -> Transmis décision demandeur. Cliquer
   sur ‘modifier avec une application externe’ pour ouvrir le modèle.
#. Openoffice se lance et ouvre le modèle. Cliquer alors sur le boutton
   ‘appyTE’.
#. Une boite de menu verte apparait alors, elle contient deux menus
   déroulants: le premier permet de préciser l’objet sur lequel on veut
   récupérer une donnée et le deuxième permet de spécifier la valeur
   exacte que l’on veut sur cet objet. Donc pour notre exemple il faut
   parcourir la  première liste et sélectionner ‘déclaration’ car
   l’article du cwatupe est une valeur présente sur la déclaration
   elle-même. Dans la deuxième liste, on précise que l’on veut le texte
   de l’article..
#. Ensuite cliquer à l’endroit du modèle ou veut insérer la valeur et
   cliquer sur le boutton ‘Insérer’ du menu vert. Ici nous allons mettre
   le texte de l’article juste après sa référence. Dès que l’on clique
   sur insérer, un commentaire apparait à l’endroit du curseur.
#. Ensuite sauvegarder le modèle et fermer openoffice. Si tout se passe
   bien, un popup signalant la fin de l’édition externe doit apparaitre.
#. Pour finir, vérifions que le changement effectué est bien correct en
   générant un document de ‘Transmis de la décision au demandeur’ d’une
   déclaration quelconque. Aller dans une déclaration et s’assurer que
   cette déclaration a bien une valeur sélectionnée pour le champ
   ‘Article’ . Se rendre dans l’onglet ‘Événements’ et créer un nouvel
   événement ‘Transmis décision au FD et demandeur’ puis générer le
   document ‘Transmis décision demandeur’. On peut voir que le document
   généré contient à présent le texte de l’article du cwatupe
   sélectionné.

Aller plus loin
---------------

| Évidemment, la personnalisation des modèles ne se limite pas à
  uniquement récupérer les valeurs du permis. Il y a aussi moyen de
  générer des tableaux et des listes automatiquement, de mettre en place
  des conditions qui en fonctions de certaines valeurs vont générer (ou
  ne pas générer) un texte spécifique. L’extension open office ne permet
  pas de réaliser ce genre de choses. Si vous avez besoin d’une
  adaptation de plus complexe, il faudra la faire avec le support d’imio
  lors d’un atelier. Si vous êtes à l’aise en programmation la
  documention sur appy POD, le module qui gére le code python dans les
  commenatires et champs de saisies, est disponible
  `ici <http://appyframework.org/pod.html>`__.
|  

4.1.7. Les modèles généraux
===========================

Dans la configuration d’urban se trouve un dossier ‘Modèles généraux’.

|image79|

Celui-ci contient six documents odt respectivement nommés:

-  Fichier d’en tête pour les modèles de documents.
-  Fichier de pied de page pour les modèles de documents.
-  Fichier gérant la zone ‘Référence’ pour les modèles de documents.
-  Fichier gérant les signatures pour les modèles de documents.
-  Fichier modèle pour les statistiques INS.
-  Fichier gérant les styles communs aux différents modèles de
   documents.

Les quatres premiers permettent de personnaliser des zones des documents
qui son communes à tous les modèles. Le modèle des stats INS eest le
document qui sert à générer le document ‘statistique des permis de batir
modèle III’

.. |PErmis d&rsquo;urbanisme - Ajout événement.png| image:: img/permis-durbanisme-ajout-evenement.png
   :class: portraitPhoto
   :width: 995px
   :height: 304px
.. |Permis d&rsquo;urbanisme - Ajout dépôt de la demande| image:: img/permis-durbanisme-ajout-depot-de-la-demande
   :class: portraitPhoto
   :width: 991px
   :height: 197px
.. |Permis d&rsquo;urbanisme - Dépôt de la demande créé| image:: img/permis-durbanisme-depot-de-la-demande-cree
   :class: portraitPhoto
   :width: 999px
   :height: 371px
.. |Firefox ouverture external editor| image:: img/firefox-ouverture-external-editor
   :class: portraitPhoto
   :width: 999px
   :height: 396px
.. |Panneau attention 600x500| image:: img/28c8a7aa53ace60a2696ef9469473706_icon
   :width: 32px
   :height: 26px
.. |Popup external editor| image:: img/popup-external-editor
   :class: portraitPhoto
   :width: 1000px
   :height: 377px
.. |Permis d&rsquo;urbanisme - Document récépissé créé| image:: img/permis-durbanisme-document-recepisse-cree
   :class: portraitPhoto
   :width: 1000px
   :height: 370px
.. |Permis d&rsquo;urbanisme - Evénements| image:: img/permis-durbanisme-evenements
   :class: portraitPhoto
   :width: 998px
   :height: 357px
.. |Icône édition| image:: img/icone-edition
   :width: 16px
   :height: 16px
.. |image9| image:: img/delete_icon.gif
.. |Onglet carte.png| image:: img/onglet-carte.png
   :class: portraitPhoto
.. |Cartographie| image:: img/cartographie
   :class: portraitPhoto
   :width: 966px
   :height: 794px
.. |Icône carto - déplacer.png| image:: img/carto_pan.png
.. |Icône carto - étendue départ| image:: img/carto_arrow_out.png
.. |Icône carto - zoom| image:: img/carto_magnifier_zoom_in.png
   :width: 16px
   :height: 16px
.. |Icône carto - dézoom| image:: img/carto_magnifier_zoom_out.png
   :width: 16px
   :height: 16px
.. |Icône carto - précédent| image:: img/carto_resultset_previous.png
   :width: 16px
   :height: 16px
.. |Icône carto - suivant| image:: img/carto_resultset_next.png
   :width: 16px
   :height: 16px
.. |Icône carto - mesure distance| image:: img/carto_ruler.png
   :width: 16px
   :height: 16px
.. |Icône carto - mesure superficie| image:: img/carto_ruler_square.png
   :width: 16px
   :height: 16px
.. |Icône carto - information| image:: img/carto_information.png
   :width: 16px
   :height: 16px
.. |Icône carto - enquête publique| image:: img/carto_server_gear.png
   :width: 16px
   :height: 16px
.. |Icône carto - couches| image:: img/carto_map_add.png
   :width: 16px
   :height: 16px
.. |Icône carto - échelle| image:: img/carto_echelle.png
   :width: 205px
   :height: 15px
.. |Les recherches.png| image:: img/les-recherches.png
   :class: portraitPhoto
   :width: 244px
   :height: 60px
.. |Recherche par parcelle.png| image:: img/recherche-par-parcelle.png
   :class: portraitPhoto
   :width: 703px
   :height: 366px
.. |Recherche_parParcelleReulstat.png| image:: img/recherche-parparcellereulstat.png
   :class: portraitPhoto
   :width: 987px
   :height: 517px
.. |Recherche par demandeur.png| image:: img/recherche-par-demandeur.png
   :class: portraitPhoto
.. |Recherche_parDemandeurResultat.png| image:: img/recherche-pardemandeurresultat.png
   :class: portraitPhoto
.. |Recherche par rue.png| image:: img/recherche-par-rue.png
   :class: portraitPhoto
   :width: 591px
   :height: 296px
.. |Résultat recherche par rue.png| image:: img/resultat-recherche-par-rue.png
   :class: portraitPhoto
   :width: 991px
   :height: 391px
.. |image31| image:: img/1.png
   :class: portraitPhoto
.. |image32| image:: img/2.png
   :class: portraitPhoto
.. |image33| image:: img/3.png
   :class: portraitPhoto
.. |image34| image:: img/4.png
   :class: portraitPhoto
.. |image35| image:: img/5.png
   :class: portraitPhoto
.. |image36| image:: img/6.png
   :class: portraitPhoto
.. |image37| image:: img/7.png
   :class: portraitPhoto
.. |image38| image:: img/echeancier.png
   :class: portraitPhoto
   :width: 293px
   :height: 135px
.. |image39| image:: img/echeancier-view.png
   :class: portraitPhoto
   :width: 991px
   :height: 412px
.. |Gérer.png| image:: img/gerer.png
   :class: portraitPhoto
.. |Architectes.png| image:: img/architectes.png
   :class: portraitPhoto
   :width: 989px
   :height: 456px
.. |Architecte_view.png| image:: img/architecte-view.png
   :class: portraitPhoto
   :width: 991px
   :height: 510px
.. |Architecte_edit.png| image:: img/architecte-edit.png
   :class: portraitPhoto
   :width: 800px
   :height: 900px
.. |lien-urban_cfg| image:: img/urban-cfg-link.png
.. |image45| image:: img/modify-pu-cfg.png
   :width: 489px
   :height: 131px
.. |image46| image:: img/edit-pu.png
.. |image47| image:: img/missing-parts.png
   :width: 666px
   :height: 236px
.. |goto-pu-cfg| image:: img/1goto-pu-cfg.png
   :width: 647px
   :height: 81px
.. |image49| image:: img/missing-parts-cfg.png
   :width: 820px
   :height: 146px
.. |image50| image:: img/urbaneventtypes-cfg.png
   :width: 633px
   :height: 74px
.. |image51| image:: img/uet-recepisse.png
   :width: 716px
   :height: 167px
.. |image52| image:: img/add-event.png
   :width: 525px
   :height: 188px
.. |image53| image:: img/decl-cfg.png
   :width: 647px
   :height: 81px
.. |urbaneventtypes-cfg| image:: img/urbaneventtypes-cfg.png
   :width: 633px
   :height: 74px
.. |image55| image:: img/new-uet-list.png
   :width: 526px
   :height: 209px
.. |image56| image:: img/avis-tech-old-fields.png
   :width: 307px
   :height: 207px
.. |image57| image:: img/generate-doc-list.png
   :width: 245px
   :height: 170px
.. |image58| image:: img/decl-cfg.png
   :width: 647px
   :height: 81px
.. |image59| image:: img/1uet-transmis-fd.png
   :width: 634px
   :height: 95px
.. |image60| image:: img/eventlist.png
   :width: 527px
   :height: 177px
.. |image61| image:: img/uet-decl.png
   :width: 406px
   :height: 135px
.. |image62| image:: img/eventlist.png
   :width: 527px
   :height: 177px
.. |image63| image:: img/uet-decl.png
   :width: 406px
   :height: 135px
.. |image64| image:: img/move-icon.png
   :width: 10px
   :height: 17px
.. |goto-pu-cfg| image:: img/1goto-pu-cfg.png
.. |image66| image:: img/foldermakers.png
   :width: 820px
   :height: 99px
.. |image67| image:: img/add-organisationterm.png
   :width: 391px
   :height: 86px
.. |image68| image:: img/new-organisationterm.png
   :width: 380px
   :height: 325px
.. |image69| image:: img/new-foldermaker-uet.png
   :width: 532px
   :height: 319px
.. |image70| image:: img/urbaneventtypes-adress.png
   :width: 844px
   :height: 48px
.. |opinion-request| image:: img/opinion-request.png
   :width: 637px
   :height: 76px
.. |disable| image:: img/disable.png
.. |delete| image:: img/delete.png
.. |modify-pu-cfg| image:: img/modify-pu-cfg.png
.. |image75| image:: img/champ-saisies.png
   :width: 332px
   :height: 111px
.. |image76| image:: img/commentaires.png
.. |image77| image:: img/appy-error.png
   :width: 295px
   :height: 122px
.. |image78| image:: img/appyte.png
   :width: 315px
   :height: 181px
.. |image79| image:: img/gobal-templates.png
   :width: 636px
   :height: 90px
