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
