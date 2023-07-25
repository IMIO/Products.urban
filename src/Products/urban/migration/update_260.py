from plone import api
import logging


def add_couple_to_preliminary_notice(context):
    """
    """
    logger = logging.getLogger('urban: add Couple to Preliminary Notice')
    logger = logging.getLogger('urban: add Couple to Project Meeting')
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'typeinfo')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'workflow')
    logger.info("upgrade step done!")


def add_justice_contacts(context):
    from Products.urban.setuphandlers import _
    from Products.urban.setuphandlers import setFolderAllowedTypes

    # import new person titles
    new_person_titles = [
        {'id': "inspector", 'title': u"Inspecteur", 'extraValue': "Inspecteur", 'abbreviation': "Insp",
         'gender': "male", 'multiplicity': "single", 'reverseTitle': "Inspecteur"},
        {'id': "substitute", 'title': u"Substitut du roi", 'extraValue': "Substitut du roi", 'abbreviation': "Subst",
         'gender': "male", 'multiplicity': "single", 'reverseTitle': "Substitut du roi"},
    ]
    portal_urban = api.portal.get_tool('portal_urban')
    persons_title_folder = portal_urban.persons_titles
    for obj in new_person_titles:
        if obj['id'] not in persons_title_folder.objectIds():
            persons_title_folder.invokeFactory('PersonTitleTerm', **obj)

    # import profile steps
    logger = logging.getLogger('urban: add justice contacts')
    logger.info("starting upgrade step")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'typeinfo')
    setup_tool.runImportStepFromProfile('profile-Products.urban:preinstall', 'workflow')
    setup_tool.runImportStepFromProfile('profile-Products.urban:default', 'cssregistry')

    # add reference integrity for justice contacts
    values = api.portal.get_registry_record('plone.app.referenceintegrity.interfaces.ISettings.reference_types')
    if u'ticketJusticeContacts' not in values:
        values.append(u'ticketJusticeContacts')
        api.portal.set_registry_record('plone.app.referenceintegrity.interfaces.ISettings.reference_types', values)

    # add a folder that will contain justice contacts
    site = api.portal.get()
    urban = getattr(site, 'urban')
    if not hasattr(urban, "justicecontacts"):
        newFolderid = urban.invokeFactory(
            "Folder",
            id="justicecontacts",
            title=_("justice_contact_folder_title", 'urban')
        )
        newSubFolder = getattr(urban, newFolderid)
        setFolderAllowedTypes(newSubFolder, 'JusticeContact')
        newSubFolder.setLayout('justice_contact_folderview')
        # manage the 'Add' permissions...
        newSubFolder.manage_permission('urban: Add Contact', ['Manager', 'Editor', ], acquire=0)
    urban.moveObjectsToBottom(['justicecontacts'])

    logger.info("upgrade step done!")
