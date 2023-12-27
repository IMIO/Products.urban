from plone.registry.interfaces import IRegistry
from zope.component import getUtility

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


def remove_generation_link_viewlet(context):
    logger = logging.getLogger("urban: Remove generation-link viewlet")
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool("portal_setup")
    setup_tool.runImportStepFromProfile("profile-Products.urban:default", "viewlets")
    logger.info("upgrade step done!")


def _update_collection_assigned_user(context):
    dashboard_collection = getattr(context, 'dashboard_collection', None)
    if "assigned_user_column" in dashboard_collection.customViewFields:
        customViewFields = list(dashboard_collection.customViewFields)
        customViewFields = ["assigned_user" if field == "assigned_user_column"
                            else field for field in customViewFields]
        dashboard_collection.customViewFields = tuple(customViewFields)


def fix_opinion_schedule_column(context):
    logger = logging.getLogger('urban: Update Opinion Schedule Collection Column')
    logger.info("starting upgrade steps")

    portal_urban = api.portal.get_tool('portal_urban')
    if "opinions_schedule" in portal_urban:
        schedule = getattr(portal_urban, "opinions_schedule")
        _update_collection_assigned_user(schedule)

        for task_id in schedule.keys():
            if task_id == "dashboard_collection":
                continue
            task = getattr(schedule, task_id)
            _update_collection_assigned_user(task)

            for subtask_id in task.keys():
                if subtask_id == "dashboard_collection":
                    continue
                subtask = getattr(schedule, subtask_id)
                _update_collection_assigned_user(subtask)

    logger.info("upgrade step done!")


def fix_opinion_workflow(context):
    logger = logging.getLogger('urban: update opinion workflow')
    logger.info("starting upgrade steps")
    setup_tool = api.portal.get_tool('portal_setup')
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
