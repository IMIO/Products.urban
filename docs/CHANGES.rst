Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

2.6.18 (2023-11-23)
-------------------

Bug fixes:


- Add `fix_schedule_config` external method ta fix class of condition objects
  [mpeeters] (SUP-33739)


2.6.17 (2023-11-16)
-------------------

Bug fixes:


- Adapt opinion request worklflow to bypass guard check for managers
  [mpeeters] (SUP-33308)


Internal:


- Provide getFirstAcknowledgment method
  [fngaha] (SUP-32215)


2.6.16 (2023-11-06)
-------------------

Bug fixes:


- Fix serializer to include disable street in uid resolver
  [jchandelle] (MURBMSGA-37)
- Fix street search to include disable street
  [jchandelle] (URB-2696)


2.6.15 (2023-10-12)
-------------------

Internal:


- Fix tests
  [mpeeters] (URB-2855)
- Improve performances for add views
  [mpeeters] (URB-2903)


2.6.14 (2023-09-13)
-------------------

Bug fixes:


- Avoid an error if a vocabulary value was removed, instead log the removed value and display the key to the user
  [mpeeters] (SUP-32338)


Internal:


- Reduce logging for sql queries
  [mpeeters] (URB-2788)
- Fix tests
  [mpeeters] (URB-2855)


2.6.13 (2023-09-05)
-------------------

Bug fixes:


- Move catalog import in urban type profile
  [jchandelle] (URB-2868)
- Fix facet config xml
  [jchandelle] (URB-2870)


2.6.12 (2023-09-01)
-------------------

Bug fixes:


- Fix new urban instance install
  [jchandelle] (URB-2868)
- Fix facet xml configuration
  [jchandelle] (URB-2870)


2.6.11 (2023-08-29)
-------------------

Bug fixes:


- Fix icon tag in table
  [jchandelle] (SUP-31983)


2.6.10 (2023-08-28)
-------------------

Bug fixes:


- Avoid an error if a task was not correctly removed from catalog
  [mpeeters] (URB-2873)


2.6.9 (2023-08-27)
------------------

Bug fixes:


- Fix UnicodeDecodeError on getFolderManagersSignaletic(withGrade=True)
  [fngaha] (URB-2871)


2.6.8 (2023-08-24)
------------------

Bug fixes:


- fix select2 widget on folder manager
  [jchandelle] (SUP-31898)
- Fix opinion schedules assigned user column
  [mpeeters] (URB-2819)


2.6.7 (2023-08-14)
------------------

Bug fixes:


- Hide old document generation links viewlet
  [mpeeters] (URB-2864)


2.6.6 (2023-08-10)
------------------

Bug fixes:


- Fix an issue with autocomplete view results format that was generating javascript errors
  [mpeeters] (SUP-31682)


2.6.5 (2023-07-27)
------------------

Bug fixes:


- Avoid errors on inexpected values on licences and log them
  [mpeeters] (SUP-31554)
- Fix translation for road adaptation vocabulary values
  [mpeeters] (URB-2575)
- Avoid an error if a vocabulary does not exist, this can happen when multiple upgrade steps interract with vocabularies
  [mpeeters] (URB-2835)


2.6.4 (2023-07-24)
------------------

New features:


- Add parameter to autocomplete to search with exact match
  [jchandelle] (URB-2696)


Bug fixes:


- Fix an issue with some urban instances with lists that contains empty strings or `None`
  [mpeeters] (URB-2575)
- Fix inspection title
  [jchandelle] (URB-2830)
- Add an external method to set profile version for Products.urban
  [mpeeters] (URB-2835)


2.6.3 (2023-07-18)
------------------

- Add missing translations [URB-2823]
  [mpeeters, anagant]

- Fix different type of vocabulary [URB-2575]
  [jchandelle]

- Change NN field position [SUP-27165]
  [jchandelle]

- Add Couple to Preliminary Notice [URB-2824]
  [ndemonte]

- Fix Select2 view display [URB-2575]
  [jchandelle]

- Provide getLastAcknowledgment method for all urbancertificates [SUP-30852]
  [fngaha]

- Fix encoding error [URB-2805]
  [fngaha]

- Add a explicit dependency to collective.exportimport
  [mpeeters]

- Cadastral historic memory error [SUP-30310]
  [sdelcourt]

- Add option to POST endpoint when creating a licence to disable check ref format [SUP-31043]
  [jchandelle]


2.6.2 (2023-07-04)
------------------

- Explicitly include `urban.restapi` zcml dependency [URB-2790]
  [mpeeters]


2.6.1 (2023-07-04)
------------------

- Fix zcml for migrations
  [mpeeters]


2.6.0 (2023-07-03)
------------------

- Fix `hidealloption` and `hide_category` parameters for dashboard collections
  [mpeeters]

- Fix render of columns with escape parameter
  [mpeeters, sdelcourt]

- Avoid a traceback if an UID was not found for inquiry cron [URB-2721]
  [mpeeters]

- Migrate to the latest version of `imio.dashboard`
  [mpeeters]


2.5.4 (2023-07-03)
------------------

- Change collection column name [URB-1537]
  [jchandelle]

- Fix class name in external method fix_labruyere_envclassthrees [SUP-29587]
  [ndemonte]


2.5.3 (2023-06-23)
------------------

- Add parcel and applicants contents to export content [URB-2733]
  [jchandelle]


2.5.2 (2023-06-15)
------------------

- Fix tests and update package metadata
  [sdelcourt, mpeeters]

- Add CSV import of recipients to an inquiry [URB-2573]
  [ndemonte]

- Fix bound licence allowed type [SUP-27062]
  [jchandelle]

- Add vat field to notary [SUP-29450]
  [jchandelle]

- Change MultiSelectionWidget to MultiSelect2Widget [URB-2575]
  [jchandelle]

- Add fields to legal aspect of generic licence [SUP-22944]
  [jchandelle]

- Add national register number to corporation form [SUP-27165]
  [jchandelle]

- Add an external method to update task delay [SUP-28870]
  [jchandelle]

- Add external method to fix broken environmental declarations [SUP-29587]
  [ndemonte]

- Fix export data with c.exportimport [URB-2733]
  [jchandelle]


2.5.1 (2023-04-06)
------------------

- Added 'retired' transition to 'deposit' and 'incomplete' states for codt_buildlicence_workflow
  [fngaha]

- Manage the display of licences linked to several applicants
  [fngaha]

- Add an import step to activate 'announcementArticlesText' optional field
  [fngaha]

- Fix external method [SUP-28740]
  [jchandelle]

- Add external method for fixing corrupted description. [SUP-28740]
  [jchandelle]

- Allow to encode dates going back to 1930
  [fngaha]

- Update MailingPersistentDocumentGenerationView call with generated_doc_title param. [URB-1862]
  [jjaumotte]

- Fix 0 values Bis & Puissance format for get_parcels [SUP-16626]
  [jjaumotte]

- Fix 0 values Bis & Puissance format for getPortionOutText
  [jjaumotte]

- Remove 'provincial' in folderroadtypes vocabulary [URB-2129]
  [jjaumotte]

- Remove locality name in default text [URB-2124]
  [jjaumotte]

- Remove/disable natura2000 folderzone [URB-2052]
  [jjaumotte]

- Add notaries mailing [URB-2110]
  [jjaumotte]

- Add copy to claymant action for recipient_cadastre in inquiry event
  [sdelcourt / jjaumotte]

- Fix liste_220 title encoding error + translation [SUP-15084]
  [jjaumotte]

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

- Add search filter on public config folders (geometricians, notaries, architects, parcellings). [SUP-10537]
  [sdelcourt]

- Migrate PortionOut (Archetype) type to Parcel (dexterity) type. [URB-2009]
  [sdelcourt]

- Fix add permissions for Inquiries. [SUP-13679]
  [sdelcourt]

- Add custom division 99999 for unreferenced parcels. [SUP-13835]
  [sdelcourt]

- Migrate ParcellingTerm (Archetype) type to Parcelling (dexterity) type.
  [sdelcourt]

- Pre-check all manageable licences for foldermanager creation. [URB-1935]
  [jjaumotte]

- Add field to define final states closing all the urban events on a licence. [URB-2082]
  [sdelcourt]

- Refactor key date display to include urban event custom titles. [SUP-13982]
  [sdelcourt]

- Add Basebuildlicence reference field reprensentativeContacts + tests [URB-2335]
  [jjaumotte]

- Licences can created as a copy of another licence (fields, applicants and parcels can be copied). [URB-1934]
  [sdelcourt]

- Add collective.quickupload to do multiple file upload on licences and events.
  [sdelcourt]

- Fix empty value display on select fields. [URB-2073]
  [sdelcourt]

- Add new value 'simple procedure' for CODT BuildLicence procedure choice. [SUP-6566]
  [sdelcourt]

- Allow multiple parcel add from the 'search parcel' view. [URB-2126]
  [sdelcourt]

- Complete codt buildlicence config with 'college repport' event. [URB-2074]
  [sdelcourt]

- Complete codt buildlicence schedule.
  [sdelcourt]

- Add default codt notary letters schedule.
  [sdelcourt]

- Add parking infos fields on road tab.
  [sdelcourt]

- Remove pod templates styles form urban. [URB-2080]
  [sdelcourt]

- Add authority default values to CODT_integrated_licence, CODT_unique_licence, EnvClassBordering. [URB-2269]
  [mdhyne]

- Add default person title when creating applicant from a parcel search. [URB-2227]
  [mdhyne]
  [sdelcourt]

- Update vocabularies CODT Build Licence (folder categories, missing parts)
  [lmertens]

- Add dashboard template 'listing permis'
  [lmertens]

- Add translations [URB-1997]
  [mdhyne]

-add boolean field 'isModificationParceloutLicence'. [URB-2250]
  [mdhyne]

- Add logo urban to the tab, overriding the favicon.ico viewlet. [URB-2209]
  [mdhyne]

- Add all applicants to licence title. [URB-2298]
  [mdhyne]

- Add mailing loop for geometricians. [URB-2327]
  [mdhyne]

- Add parcel address to parcel's identity card.[SUP-20438]
  [mdhyne]

- Adapt ComputeInquiryDelay for EnvClassOne licences and Announcements events.[SUP20443]
  [mdhyne]

- Include parcels owners partner in cadastral queries.[SUP-20092]
  [sdelcourt]

- Add fields trail, watercourse, trailDetails, watercourseCategory and add vocabulary in global config for the fields.[MURBECAA-51]
  [mdhyne]

- To use 50m radius in announcement : changes setLinkedInquiry getAllInquiries() call by getAllInquiriesAndAnnouncements() and changes condition in template urbaneventinquiryview.pt. [MURBWANAA-23]
  [mdhyne]

- add new 'other' tax vocabulary entry and new linked TextField taxDetails
  [jjaumotte]

- Add contact couples.
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

2.3.x (unreleased)
-------------------
- Update MultipleContactCSV methods with an optional number_street_inverted (#17811)
  [jjaumotte]

1.11.1 (unknown release date)
-----------------------------
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
