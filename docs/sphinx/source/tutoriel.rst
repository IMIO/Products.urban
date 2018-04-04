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

Cette procédure permet de créer de nouvelles demandes d'avis.

1) Se positionner dans la liste des types d'événement d'une procédure: paramètres des procédures -> choisir la procédure -> événements -> types d'événements.
2) Ajouter un élément et choisir "OpinionRequestEventType".
3) Remplir les champs suivants :

	* Titre
	* Observation: indiquer les données de contact (organisation, adresse, ville,...), celles-ci seront reprises dans le cadre du destinataire à la génération de la demande d'avis.
	* Catégorie du type d'événement: sélectionner "Demande d'avis"
	* Eventportaltype: sélectionner "Evénement lié à une demande d'avis"
	* Valeur supplémentaire: indiquer un identifiant permettant de retrouver facilement la demande d'avis parmi les autres, par exemple le nom de l'organisation (Fluxys, Service Incendie, etc). Cette valeur sera utilisée dans l'onglet "Avis" d'un procédure: en tapant "Fluxys" l'application proposera alors la demande d'avis pour Fluxys.
	Puis enregistrer.
	Une dernière étape est nécessaire: modifier le document	
4) Enregistrer, puis modifier à nouveau la demande d'avis pour remplir le champ "Condition TAL" par : python: here.mayAddOpinionRequestEvent('*demande-davis-fluxys*'). Modifier la valeur en gras entre apostrophe par la valeur se trouvant à la fin de l'url. Exemple : https://macommune-urban.imio-app.be/portal_urban/codt_buildlicence/urbaneventtypes/*demande-davis-fluxys*

	


###################
Sortir la liste 220
###################


