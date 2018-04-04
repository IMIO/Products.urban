.. Urban documentation master file, created by
   sphinx-quickstart on Tue Mar  6 11:32:14 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tutoriels
=========

Contents:

.. toctree::
   :maxdepth: 2


#############
Configuration
#############

Voici un chapitre traitant des fonctionnalités accessibles dans le menu "Configuration urban" accessible en bas à gauche sur l'accueil. Un rôle "Urban Manager" est requis.

**********************
Configuration générale
**********************

*********************************
Mise en place des demandes d'avis
*********************************

Cette procédure permet de créer de nouvelles demandes d'avis à partir d'un canevas existant, l'événement \*\*\*Demande d'avis CONFIG\*\*\*.

1) Se positionner dans la liste des types d'événement d'une procédure.
2) Ajouter un élément et choisir "OpinionRequestEventType".
3) Remplir les champs suivants :

	* Titre.
	* Observation: les données de contact (nom de l'organisation, rue, ville,...).
	* Catégorie du type d'événement: sélectionner "Demande d'avis".
	* Eventportaltype: sélectionner "Evénement lié à une demande d'avis".
	* Valeur supplémentaire: label permettant de la retrouver facilement, exemple: fluxys pour une demande concernant cette organisation.
	
	* (optionnel) Champs activés: sélectionner les champs qui apparaitront à la création de l'événement dans une procédure. Un champ de date d'événement existe par défaut.

4) Enregistrer, et récupérer l'identifiant de l'événement situé à la fin de l'url, exemple : :samp:`macommune-urban.imio-app.be/portal_urban/codt_buildlicence/urbaneventtypes/{demande-davis-fluxys}`

5) Modifier à nouveau la demande, et placer dans le champ "Condition TAL": :samp:`python: here.mayAddOpinionRequestEvent('{demande-davis-fluxys}')` avec l'identifiant de la demande entre les apostrophes.

6) Enregistrer, puis tester sur un dossier de test si besoin. C'est terminé !

Par défaut, les nouvelles demandes vont utiliser le modèle de base dans \*\*\*Demande d'avis CONFIG\*\*\*, avec les données de contact renseignées dans le champ "Organisation".

Pour utiliser un modèle spécifique à une demande, le rajouter dans la page de la demande (ajout d'un élément -> UrbanTemplate). Attention, le modèle de base ne sera **plus** utilisé.

###################
Sortir la liste 220
###################


