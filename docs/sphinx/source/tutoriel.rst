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

Voici un chapitre traitant des fonctionnalités accessibles dans le menu "Configuration urban" accessible en bas à gauche sur l'accueil. Un rôle "Urban Manager" est requis.

Configuration générale
----------------------

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

Sortir la liste 220
===================

Cette fonctionnalité permet d'obtenir le fichier correspondant à la liste 220 à utiliser dans l'application URBAIN.

#. Sélectionner une procédure.
#. Dans la recherche avancée, entrer un intervalle de temps pour les dates de décision.
#. Un bouton "Liste 220" apparait en haut à droite des résultats de la recherche, qui enregistre la liste au format :samp:`.xml`.

Si au moment d'enregistrer la liste, une page d'erreur apparait à la place, certains champs obligatoires pour la liste 220 n'ont pas été renseignés.
Exemple, si une erreur :samp:`unknown worktype  on licence PU/2017/4161/DC` apparait: le type de travaux n'a pas été renseigné pour le permis qui a comme référence ``PU/2017/4161/DC``. Il faut alors rechercher ce permis par référence et modifier les champs nécessaires.

Utiliser l'édition externe avec ZopeEdit
========================================

