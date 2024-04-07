Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

2.5.0.dev7 (2024-04-07)
-----------------------

Bug fixes:


- Avoid an error if an advice was not defined
  [mpeeters] (SUP-36385)


2.5.0.dev6 (2024-04-01)
-----------------------

Bug fixes:


- Move method methods to be available for every events.
  Change `is_CODT2024` to be true if there is no deposit but current date is greater than 2024-03-31.
  [mpeeters] (URB-3008)


Internal:


- Update setup for tests
  [mpeeters]
  Test checking completion task
  [daggelpop] (URB-3005)


2.5.0.dev5 (2024-03-20)
-----------------------

New features:


- Make caduc and abandoned workflow state grey
  [jchandelle] (URB-3007)
- Add `is_not_CODT2024` method that can be used in templates
  [mpeeters] (URB-3008)


Bug fixes:


- Fix update of vocabularies
  [mpeeters] (URB-3002)
- Invert Refer FD delay 30 <-> 40 days
  [mpeeters] (URB-3008)


2.5.0.dev4 (2024-03-18)
-----------------------

New features:


- Add `getCompletenessDelay`, `getReferFDDelay` and `getFDAdviceDelay` methods that can be used in templates
  [mpeeters] (URB-3008)


2.5.0.dev3 (2024-03-16)
-----------------------

New features:


- Add `is_CODT2024` and `getProrogationDelay` methods that can be used in template
  [mpeeters] (URB-2956)
- Adapt vocabulary logic to include start and end validity dates
  [mpeeters] (URB-3002)
- Adapt vocabulary terms for 2024 CODT reform
  [daggelpop] (URB-3003)
- Add `urban.schedule` dependency
  [mpeeters] (URB-3005)
- Add event fields `videoConferenceDate`, `validityEndDate` & marker `IIntentionToSubmitAmendedPlans`
  [daggelpop] (URB-3006)


Bug fixes:


- Fix delay vocabularies value order
  [mpeeters] (URB-3003)
- Fix an issue with zope users on urban homepage
  [mpeeters] (URB-3004)
- Remove broken Liege browser layer
  [daggelpop] (URB-3006)


Internal:


- Provided prorogation field for environment license
  [fngaha] (URB-2924)
- Move some schedule logic into `urban.schedule`
  [mpeeters] (URB-3005)


2.5.0.dev2 (2024-01-11)
-----------------------

Bug fixes:


- Validate CSV before claimant import
  [daggelpop] (SUP-33538)
- Fix a silent error with portlet on overlays
  [mpeeters] (URB-2926)


2.5.0.dev1 (2023-11-21)
-----------------------

Bug fixes:


- Restore commented out URBAN_TYPES elements in config (most likely an error)
  [daggelpop] (SUP-28903)
- Fix url for exploitation conditions, `getRaw` is no longer accessible through urls
  [mpeeters] (SUP-33698)


Internal:


- Reduce logging for sql queries
  [mpeeters] (URB-2926)


2.5.0.dev0 (2023-11-09)
-----------------------

- Fix extra profile setup causing too big transaction
  Error was: "TypeError: Can't pickle objects in acquisition wrappers"
  [laulaz]

- provides organizations to consult based on external directions
  [fngaha]

- Add an Ultimate date field in the list of activatable fields
  [fngaha]

- provide the add company feature to the CU1 process
  [fngaha]

- Update documentation with cadastre downloading
  [fngaha]

- Translate liste_220 errors
  [fngaha]

- Provide the add company feature to the CU1 process
  [fngaha]

- Improve mailing. Add the possibility to delay mailing during the night [SUP-12289]
  [sdelcourt]

- Fix default schedule config for CODT Buildlicence [SUP-12344]
  [sdelcourt]

- Allow shortcut transition to 'inacceptable' state for CODT licence wofklow. [SUP-6385]
  [sdelcourt]

- Set default foldermanagers view to sort the folder with z3c.table on title [URB-1151]
  [jjaumotte]

- Add some applicants infos on urban_description schemata. [URB-1171]
  [jjaumotte]

- Improve default reference expression for licence references. [URB-2046]
  [sdelcourt]


2.4 (2019-03-25)
----------------
- add tax field in GenericLicence
  [fngaha]

- add communalReference field in ParcellingTerm
  [fngaha]

- Fix format_date
  [fngaha]
  
- Update getLimitDate
  [fngaha]

- Fix translations
- Update the mailing merge fields in all the mailing templates
  [fngaha]

- Specify at installation the mailing source of the models that can be mailed via the context variable
  [fngaha]

- Select at the installation the mailing template in all models succeptible to be mailed
  [fngaha]

- Referencing the mailing template in the general templates configuration (urban and environment)
  [fngaha]

- Allow content type 'MailingLoopTemplate' in general templates
  [fngaha]

- added the mailing template
  [fngaha]

- add mailing_list method
  [fngaha]

- add a z3c.table column for mailing with his icon
  [fngaha]

- fix translations
  [fngaha]

- update signaletic for corporation's applicant
  [fngaha]

- fix the creation of an applicant from a parcel
  [fngaha]

- add generic "Permis Publics" templates and linked event configuration
  [jjaumotte]

- add generic "Notary Letters" template and linked event configuration
  [jjaumotte]

- fix advanced searching Applicant field for all licences, and not just 'all'
  [jjaumotte]

2.3.0
-----
- Add attributes SCT, sctDetails
  [fngaha]

- Add translations for SCT, sctDetails
  [fngaha]

- Add vocabularies configuration for SCT
  [fngaha]

- Add migration source code
  [fngaha]


1.11.1 (unreleased)
-------------------
- add query_parcels_in_radius method to view
  [fngaha]

- add get_work_location method to view
  [fngaha]

- add gsm field in contact
  [fngaha]

- improve removeItems utils
  [fngaha]

- Refactor rename natura2000 field because of conflict name in thee
  [fngaha]

- Refactor getFirstAdministrativeSfolderManager to getFirstGradeIdSfolderManager
  The goal is to use one method to get any ids
  [fngaha]

- Add generic SEVESO optional fields
  [fngaha]

- Fix concentratedRunoffSRisk and details optional fields
  [fngaha]

- Add getFirstAdministrativeSfolderManager method
  [fngaha]

- Add removeItems utils and listSolicitOpinionsTo method
  [fngaha]

- Add getFirstDeposit and _getFirstEvent method
  [fngaha]

- remove the character 'à' in the address signaletic
  [fngaha]

- use RichWidget for 'missingPartsDetails', 'roadMissingPartsDetails', 'locationMissingPartsDetails'
  [fngaha]

- Fix local workday's method"
  [fngaha]

- Add a workday method from collective.delaycalculator
  refactor getUrbanEvents by adding UrbanEventOpinionRequest
  rename getUrbanEventOpinionRequest to getUrbanEvent
  rename containsUrbanEventOpinionRequest to containsUrbanEvent
  [fngaha]

- Add methods
  getUrbanEventOpinionRequests
  getUrbanEventOpinionRequest
  containsUrbanEventOpinionRequest
  [fngaha]

- Update askFD() method
  [fngaha]

- Add generic Natura2000 optional fields
  [fngaha]

- Fix codec in getMultipleClaimantsCSV (when use a claimant contat)
  [fngaha]

- Add generic concentratedRunoffSRisk and details optional fields
  [fngaha]

- Add generic karstConstraint field and details optional fields
  [fngaha]


1.11.0 (2015-10-01)
-------------------

- Nothing changed yet.


1.10.0 (2015-02-24)
-------------------

- Can add attachments directly on the licence (#10351).


1.9.0 (2015-02-17)
------------------

- Add environment licence class two.

- Use extra value for person title signaletic in mail address.


1.8.0 (2015-02-16)
------------------

- Add environment licence class one.

- Bug fix: config folder are not allowed anymore to be selected as values
  for the field 'additionalLegalConditions'.


1.7.0
-----

- Add optional field RGBSR.

- Add field "deposit type" for UrbanEvent (#10263).


1.6.0
-----

- Use sphinx to generate documentation

- Add field "Périmètre de Rénovation urbaine"

- Add field "Périmètre de Revitalisation urbaine"

- Add field "Zones de bruit de l'aéroport"


1.5.0
-----

- Update rubrics and integral/sectorial conditions vocabularies


1.4.0
-----

- Add schedule view


1.3.0
-----

- Use plonetheme.imioapps as theme rather than urbasnkin

- Add fields "pm Title" and "pm Description" on urban events to map the fields "Title"
  and "Description" on plonemeeting items (#7147).

- Add a richer context for python expression in urbanEvent default text.

- Factorise all licence views through a new generic, extendable and customisable view (#6942).
  The fields display order is now given by the licence class schemata and thus this order
  is always consistent between the edit form and the view form.


1.2.0
------

- Added search on parcel Historic and fixed search on old parcels (#6681).


1.1.9
-----

- Opinion request fields are now active for MiscDemand licences (#5933).

- Added custom view for urban config and licence configs (#5892).

- Fixed urban formtabbing for plone 4.2.5 (#6423).

- Python expression can now be used in urbanEvent default text (#6406).

- "Deliberation college" documents are now disabled when using pm.wsclient (#6407).

- Added configuration step for pm.wsclient (#6400).

- Added rubrics and conditions config values for environment procedures (#5027).

- Fixed search on parcel historic (#6681).

- Added popup to see all licences related to a parcel historic (#5858).

- Generate mailing lists from contacts folder (architects, notaries, geometrcicians) (#6378).

- Adds pm.wsclient dependency.


1.1.8
-----

- Converted all urban listings into z3c tables.

- Simplified the opinion request configuration system (#5711).

- Added more columns on search result listing (#5535).

- Vocabulary term now have a the possibility to have a custom numbering that will only be displayed in forms but
  not in generated documents (#5408).

- An alternative name of divisions can be configured for generated documents (#5507).

- Address names of mailing documents can now be inverted (#4763).

- [bugfix] Create the correct link for UrbanDoc in the urban events when the licence is not
  in 'edit' state anymore.


1.1.7
-----

- Added options bar to licences listing (#5476, #5250).

- Use events rather than archetype built-in default method system to fill licence fields with default values
  because of performance issues (#5423).

- Parcels can be added on ParcellingTerm objects. Now, parcellingterm objects can be found by parcel references (#5537).

- A helper popup is now available on specific features datagrid to edit related fields without navigating through the
  edit form (#5576).

- Default text can be defined for urban event text fields as well (#5508).

bugfixes:
- Folder search by parcel reference is now working with lowercase inputs.


1.1.6
-----

- Added field Transparence on class Layer (#5197).

- Added style 'UrbanAdress' used to customize style in the adress field of documents (#4764).

- Added beta version of licence type 'Environmental Declaration'.

- Use an autocomplete for the licence search by street (#5163).

- Text of the specificFeatures fields are now editable within a licence (CU1, CU2, notaryletter) (#5280).

- Added an optional field 'architects' on MiscDemand class (#5286).

- Added field 'represented by society' on applicant/proprietary (#5282).

- Now, the licence search works with old parcels references and also works with incomplete parcels references as well (#5099).

- Urban editors can now add parcels manually (#5285).

- Added validator on reference field to check that each reference is unique (#5430).

- Show historic of old parcels on licences "map" tab and allow to show the location of their "children" (#4754).

- Urban editors can now add parcel owner manually on inquiry events (#5289).

- Added search by "folder reference" in urban folder search (#4878).

- Licences tabs can be renamed and reordered (#5465).

bugfixes:
- UrbanEvent view doesnt crash anymore when a wrong TAL condition is defined on an UrbanDoc.
- corrected template "accuse de reception d'une reclamation" (#5168, #5198).
- corrected the display of the specificFeatures for notary letters.
- The "50m area" used in inquiries doesnt crash anymore when finding parcel owner without address (#5376).
- Added warning on inquiry event when parcel owners without adress are found (#5289).
