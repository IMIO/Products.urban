.. Urban documentation master file, created by
   sphinx-quickstart on Tue Mar  6 11:32:14 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*********
Tutoriels
*********

Contents:

.. toctree::
   :maxdepth: 2


Configuration
=============

Voici un chapitre traitant des fonctionalités accessibles dans le menu "Configuration urban" accessible en bas à gauche sur l'accueil. Un rôle "Urban Manager" est requis.

Configuration générale
----------------------

Configurer les champs optionnels de données
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Un permis se présente sous la forme de données réparties dans plusieurs onglets (récapitulatif, avis, enquête, voirie, etc...). Certaines données sont indispensables (objet du permis, adresse du bien concerné) quand d'autres sont optionnelles.

Il est donc possible de configurer quels champs de données vont apparaitre pour chaque type de permis.

#. Aller dans "Configuration d'urban", "Paramètres des procédures", choisir la procédure de permis concernée.
#. Cliquer sur "Modifier", une liste de champs optionnels apparait. La valeur entre parenthèses devant chaque champ correspond à l'onglet dans lequel ce champ se trouve.
#. Sélectionner ou désélectionner en cliquant avec la touche ``CTRL`` enfoncée.
#. Enregistrer les modifications.

Si l'on veut masquer un onglet entièrement, il suffit de le décocher dans la liste des onglets.

Configurer les listes de vocabulaire
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A différents endroits dans Urban, il existe des listes de valeurs à sélectionner. Pour certaines de ces listes, les valeurs sont configurables, c'est-à-dire qu'on peut en rajouter, supprimer ou les modifier. Par exemple:

   * Les titres des personnes: Monsieur, Madame, Maitre,...
   * Pour les CU1, la liste des particularités communales du bien.
   * Pour les permis d'urbanisme, les différents types de 'pièces manquantes'.
   
Certaines de ces listes sont spécifiques à des types de permis, quand d'autres sont communes à tous.

Les listes de vocabulaires communes vont donc se trouver dans la page de configuration d'urban, à l'onglet "Vocabulaire", tandis que les listes spécifiques vont se trouver dans la page de la procédure de permis concernée, toujours à l'onglet "Vocabulaire".

Pour commencer à modifier les valeurs d'une liste de vocabulaire, il faut cliquer dessus, puis aller dans la vue "Contenus", pour ensuite :

* Ajouter une valeur se fait avec le bouton "Ajout d'un élément" puis "Terme de vocabulaire urban". Il suffit alors de lui donner un titre, qui est la valeur du vocabulaire.

* Supprimer une valeur se fait en **changeant l'état** de la valeur concernée, pour le passer à "Désactivé". Supprimer réellement un élément risque d'entrainer des effets de bords si celui-ci est utilisé sur des permis.

* Modifier une valeur se fait avec le bouton "Renommer", puis modifier le titre. Attention à ne pas modifier l'identifiant sous peine d'effet de bord.

Configurer les événements
^^^^^^^^^^^^^^^^^^^^^^^^^

Un bref rappel: les événements représentent les différentes étapes par lesquelles passent un permis. L'ensemble de ces événements forment une procédure de permis. Ils sont ajoutables via l'onglet "Événement du dossier" dans un permis en cours. Chaque événement contient au minimum une date indiquant quand il s'est produit et possède un nombre variable de documents à générer qui lui sont liés.

Que peut on configurer sur les événements ?

* En ajouter, avec leur propres modèles de documents à générer.
* Retirer des événements inutiles.
* Changer l'ordre dans la liste.
* Instaurer des conditions d'apparition. Par exemple, l'événement "Dossier complet" ne peut pas apparaitre dans la liste avant que l'événement "Dépôt de demande" ait été créé.
* Modifier les délais et délais d'alerte de l'événement.
* Ajouter ou supprimer des modèles de documents à générer pour un événement donné.

   **Ajouter un événement**
	
	
	
   **Retirer un événement**
	
	
	
   **Ajouter ou supprimer des modèles de documents**



.. todo::

Mise en place des demandes d'avis
---------------------------------

Ce tutoriel permet de créer de nouvelles demandes d'avis à partir d'un canevas existant, situé dans l'événement \*\*\*Demande d'avis CONFIG\*\*\*.

#. Se positionner dans la liste des types d'événement d'une procédure.
#. Ajouter un élément et choisir "OpinionRequestEventType".
#. Remplir les champs suivants :

	* Titre.
	* Observation: les données de contact (nom de l'organisation, rue, ville,...).
	* Catégorie du type d'événement: sélectionner "Demande d'avis".
	* Eventportaltype: sélectionner "Evénement lié à une demande d'avis".
	* Valeur supplémentaire: label permettant de la retrouver facilement, exemple: fluxys pour une demande concernant cette organisation.
	
	* (optionnel) Champs activés: sélectionner les champs qui apparaitront à la création de l'événement dans une procédure. Un champ de date d'événement existe par défaut.

#. Enregistrer, et récupérer l'identifiant de l'événement situé à la fin de l'url, exemple : :samp:`macommune-urban.imio-app.be/portal_urban/codt_buildlicence/urbaneventtypes/{demande-davis-fluxys}`

#. Modifier à nouveau la demande, et placer dans le champ "Condition TAL": :samp:`python: here.mayAddOpinionRequestEvent('{demande-davis-fluxys}')` avec l'identifiant de l'événement entre les apostrophes.

#. Enregistrer, puis tester sur un dossier de test si besoin. C'est terminé !

Par défaut, les nouvelles demandes vont utiliser le modèle de base dans \*\*\*Demande d'avis CONFIG\*\*\*, avec les données de contact renseignées dans le champ "Organisation".

Pour utiliser un modèle spécifique à une demande, le rajouter dans la page de la demande (ajout d'un élément -> UrbanTemplate). Attention, le modèle de base ne sera **plus** utilisé.

Utiliser l'échéancier
=====================

L'échéancier est accessible via la page d'accueil d'Urban, dans la colonne de gauche à l'onglet "Outils". Il se présente sous la forme d'un tableau de suivi de permis, affichant les différents permis pour lesquels une tâche est en cours, classés par défaut par échéance, de la plus proche (ou en retard) à la plus éloignée.

Le tableau comprend au minimum les colonnes suivantes :

* Titre du permis: comprenant un lien permettant d'accéder à la page de la procédure du permis.
* Titre de la tâche en cours: cette tâche générale peut désigner un "état" dans lequel se trouve le permis (exemple: incomplet), et les sous-tâches vont alors désigner les actions à effectuer.
* Adresse et référence cadastrale du ou des biens concerné.
* Assigné à: désigne l'agent d'urbanisme à qui le suivi de ce permis et donc la tâche en cours est assignée.
* Status: affiche le status de la tâche en cours, avec un code couleur ainsi que la ou les sous-tâches si la tâche en cours en est composée. Le code couleur est le suivant:

	* Vert pour une tâche faite.
	* Jaune pour une tâche en cours.
	* Bleu pour une tâche qui va prochainement démarrer mais ne peut s'effectuer actuellement (exemple: une autre sous-tâche doit s'effectuer avant).
	
	Cliquer sur le code couleur d'un permis permet de consulter l'historique des tâches pour ce suivi de permis.
	
* Échéance: l'échéance de la tâche générale en cours. Si une ou plusieurs sous-tâches sont en cours, leurs échéances respectives s'affichent dans la colonne status.
* Actions: permet des actions sur le suivi de permis comme la possibilité de ré-assigner à un autre agent.

A gauche du tableau se trouve des liens permettant de filtrer les permis. Il est possible de les classer par types de procédure, ou de filtrer par tâche et sous-tâche en cours.

Au dessus du tableau se trouve des fonctionalités de recherche. Il est par exemple possible de filtrer les suivis de permis par utilisateur assigné, pour qu'un agent ne voie que les permis qui lui sont assignés.

Lorsqu'une tâche a été effectuée et que la procédure du permis en question a été mise à jour, le suivi va passer automatiquement à la tâche suivante dans la procédure de permis.


Exporter la liste 220
=====================

Cette fonctionalité permet d'obtenir le fichier correspondant à la liste 220 à utiliser dans l'application URBAIN du SPF.

#. Sélectionner une procédure.
#. Dans la recherche avancée, entrer un intervalle de temps pour les dates de décision.
#. Un bouton "Liste 220" apparait en haut à droite des résultats de la recherche, qui enregistre la liste au format :samp:`.xml`.

Si au moment d'enregistrer la liste, une page d'erreur apparait à la place, certains champs obligatoires pour la liste 220 n'ont pas été renseignés.
Exemple, si une erreur :samp:`unknown worktype  on licence PU/2017/4161/DC` apparait: le type de travaux n'a pas été renseigné pour le permis qui a comme référence ``PU/2017/4161/DC``. Il faut alors rechercher ce permis par référence et modifier les champs nécessaires.
Seuls les permis avec un statut "Accepté" sont repris.

Exporter le fichier de statistiques INS
=======================================

Similaire à l'exportation de la liste 220, cette fonctionalité permet d'obtenir le fichier correspondant aux statistiques INS.

#. Sélectionner une procédure.
#. Optionnellement, sélectionner des critères de recherche pour sortir un fichier INS plus ciblé.
#. Un bouton "Statistiques INS" apparait en haut à droite des résultats de recherche, et permet d'enregistrer le document.

Le canevas du fichier de statistiques INS se trouve lui dans les modèles généraux de la configuration urban. Il ne faut normalement pas le modifier.

Utiliser l'édition externe avec ZopeEdit
========================================

Il est possible d'utiliser un éditeur externe pour éditer les documents présents dans l'application Urban. Par exemple, ouvrir dans Word ou LibreOffice un document afin de l'éditer et d'enregistrer les modifications: celles-ci sont directement répercutées dans Urban.

On utilise le logiciel ZopeEdit (diminutif de Zope External Editor) afin de faire le lien entre l'éditeur de texte et l'application Urban. Il est donc nécessaire de compléter l'installation de ce logiciel, étape par étape.

La première étape est l'activation de l'édition externe dans Urban (sur certains types d'éléments seulement). On obtiendra alors pour ces éléments un lien pour l'édition externe, représentée par un crayon rouge. Ce lien va créer un fichier :samp:`.zem`, qu'il est nécessaire d'ouvrir via le logiciel ZopeEdit.

La seconde étape consiste donc en l'installation sur le poste client du logiciel ZopeEdit, qui pourra faire le lien entre ces fichiers et un éditeur de texte classique.

Ces étapes sont normalement faites à la mise en place de l'application Urban. Si un problème survenait avec l'édition externe, il est quand même intéressant de vérifier que ces deux étapes sont correctes.

Activation et configuration dans Urban
--------------------------------------

#. En tant qu'administrateur, aller dans la "Configuration du site" puis "Modules". Il faut activer sur cette page le module "collective.externaleditor".
#. Une fois le module activé, retourner à la "Configuration du site", un lien "Édition externe" est maintenant disponible. Cocher la case "Activer la fonctionalité d'édition externe" si ce n'est pas déjà fait. Il est aussi possible de choisir sur quels éléments l'édition externe est activée.
#. Il est aussi nécessaire d'activer cette option par utilisateur. Dans les "Préférences" d'un utilisateur, aller dans l'onglet "Préférences personnelles" et cocher la case "Activer l'édition externe".


Installation de ZopeEdit
------------------------

La procédure est différente suivant le système d'exploitation.

Windows
^^^^^^^

#. `Téléchargez le logiciel à cette adresse. <http://www.imio.be/support/documentation/fichiers/zopeedit>`_
#. Suivez les instructions pour l'installation.
#. Redémarrez le PC.

Mac
^^^

#. `Téléchargez le logiciel à cette adresse <http://download.gocept.com/packages/ZopeEditManager-0.9.8.dmg>`_
#. Dans les préférences, onglet "Helper Apps", ajouter le format odt comme suit:

	* Type: applications/odt **OU** si ça ne fonctionne pas: application/vnd.oasis.opendocument.text
	* Editor: LibreOffice
	* Extension : .odt

Linux
^^^^^

.. todo::

Résolution des problèmes
------------------------

Problèmes à l'ouverture du fichier
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Il faut vérifier en premier lieu si Firefox est bien configuré pour ouvrir les fichiers ZopeEdit.

#. Si c'est bien le cas et que le problème d'ouverture persiste, il est possible de modifier la configuration de ZopeEdit.

#. En dernier recours, consulter le fichier de log et nous l'envoyer via un ticket de support.

**Note:** Pour les applications iA.Urban et iA.Docs, les documents générés et les modèles à éditer sont au format :samp:`.odt` et il est impératif de les ouvrir avec LibreOffice, comme indiqué dans les prérequis.

Si un autre éditeur de texte ouvre le document, se référer à la `Configuration de ZopeEdit`_  et modifier aussi la ligne :samp:`editor=` avec le chemin de l'exécutable de LibreOffice Writer. Sur une installation par défaut, ce sera par exemple: :samp:`editor=C:\\Program Files\\LibreOffice\\program\\swriter.exe`.

Configuration de Firefox
^^^^^^^^^^^^^^^^^^^^^^^^

A la première utilisation de la fonction d'édition externe, le navigateur demande quoi faire avec le fichier :samp:`.zem`. Si ZopeEdit a bien été installé, le navigateur va proposer automatiquement l'association dans le choix "Ouvrir avec".

Toutefois, si ZopeEdit n'est pas proposé par le navigateur, il faut aller le chercher manuellement. Il faut cliquer dans la liste déroulante sur "Autre", une fenêtre de sélection apparait permettant de choisir dans la liste des programmes. Si ZopeEdit n'est toujours pas dans cette liste, cliquer sur le bouton "Parcourir..." et sélectionner :samp:`zopeedit.exe` dans le répertoire d'installation (si il n'a pas été modifié à l'installation : :samp:`C:\\ProgramFiles\\ZopeExternalEditor`).

Il est toujours possible de modifier ultérieurement une mauvaise association. Pour ce faire, aller dans le menu "Préférences" de Firefox, et dérouler jusqu'à "Applications". En recherchant "Zope" dans la boite de dialogue, on peut à nouveau définir l'utilisation de :samp:`zopeedit.exe` pour le type de contenu ZopeEdit.

Configuration de ZopeEdit
^^^^^^^^^^^^^^^^^^^^^^^^^

Une fois installé, ZopeEdit dispose d'un fichier de configuration, placé dans un dossier de configuration de Windows.

Il n'est pas recommandé de changer les options de ce fichier, sauf si les réglages par défaut ne sont pas suffisants. En effet, par défaut, ZopeEdit laisse faire le système d'exploitation (Windows) et le navigateur (Firefox) pour associer les fichiers ZopeEdit. Parfois, ces associations ne sont pas correctes malgré les réglages dans Firefox, il est alors possible de les forcer via le fichier de configuration.

Avant de modifier ce fichier de configuration, il faut donc être certain que le navigateur est bien configuré.

Pour ouvrir ce fichier, le plus simple est de passer par le menu "Démarrer" et de lancer "Zope External Editor". La première fois, le fichier de configuration s'ouvre dans un éditeur de texte.

La seconde partie du fichier contient les associations entre le type de fichiers, son extension et le programme à utiliser pour l'ouvrir. C'est cette partie qu'il faut modifier ou compléter.

Voici ce qu'il faut y mettre::

	[content-type:application/vnd.oasis.opendocument.text]
	extension=.odt
	editor=
	
Il est nécessaire d'enregistrer le fichier.

Si l'on lance à nouveau Zope External Editor, une fenêtre demande de réinitialiser le fichier avec les valeurs par défaut: il faut répondre "Non".

Fichier de log
^^^^^^^^^^^^^^

ZopeEdit écrit ses messages d'erreur dans un fichier de log. En cas de problème, il est recommandé de consulter ce fichier afin d'avoir le maximum d'informations concernant le problème rencontré.

Le fichier de log se situe dans le dossier :samp:`%TEMP%`, qui est un dossier spécial sur Windows. Vous pouvez y accéder soit en tapant %TEMP% dans la barre d'adresse des dossiers, ou via :samp:`C:\\Documents and Settings\\{utilisateur}\\Local Settings\\Temp`.
