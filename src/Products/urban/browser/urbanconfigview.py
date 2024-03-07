# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.urban import UrbanMessage as _
from Products.urban.setuphandlers import _create_task_configs
from Products.urban.browser.table.urbantable import InternalOpinionServicesTable
from Products.urban.browser.offdays_settings import OffDaysEditForm
from Products.urban.browser.gig_coring_settings import GigCoringLinkEditForm
from Products.urban.browser.schedule_settings import ScheduleEditForm

from imio.schedule.content.object_factories import CreationConditionObject
from imio.schedule.content.object_factories import RecurrenceConditionObject

from plone import api

from z3c.form import button
from z3c.form import form, field

from zope.interface import Interface
from zope.schema import TextLine


class UrbanConfigView(BrowserView):
    """ """

    def __init__(self, context, request):
        super(UrbanConfigView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.default_values_form = UpdateDefaultValuesForm(context, request)
        self.default_values_form.update()
        self.internal_services_form = AddInternalServiceForm(context, request)
        self.internal_services_form.update()
        self.offdays_form = OffDaysEditForm(context, request)
        self.offdays_form.update()
        self.schedule_form = ScheduleEditForm(context, request)
        self.schedule_form.update()
        self.gig_coring_form = GigCoringLinkEditForm(context, request)
        self.gig_coring_form.update()

    def getTabMacro(self, tab):
        context = aq_inner(self.context)
        macro_name = "%s_macro" % tab
        macro = context.unrestrictedTraverse("@@urbanconfigmacros/%s" % macro_name)
        return macro

    def getTabs(self):
        return [
            "public_settings",
            "licences_config",
            "vocabulary_folders",
            "schedule",
            "internal_services",
            "admin_settings",
            "gig_coring",
        ]

    def getMiscConfigFolders(self):
        context = aq_inner(self.context)
        names = ["globaltemplates", "dashboardtemplates", "foldermanagers", "streets"]
        folders = [
            folder for folder in context.objectValues("ATFolder") if folder.id in names
        ]
        return folders

    def getVocabularyFolders(self):
        context = aq_inner(self.context)
        other_folders = self.getMiscConfigFolders()
        folders = [
            folder
            for folder in context.objectValues("ATFolder")
            if folder not in other_folders
        ]
        return folders

    def getScheduleConfigs(self):
        context = aq_inner(self.context)
        survey_schedule = getattr(context, "survey_schedule", None)
        opinions_schedule = getattr(context, "opinions_schedule", None)
        schedules = [
            schedule for schedule in [survey_schedule, opinions_schedule] if schedule
        ]
        return schedules

    def renderInternalServicesListing(self):
        table = InternalOpinionServicesTable(self.context, self.request)
        table.update()
        return table.render()


class IAddInternalServiceForm(Interface):

    service_name = TextLine(title=_(u"Service full name"), required=True)

    service_id = TextLine(title=_(u"Service id"), required=True)


class AddInternalServiceForm(form.Form):

    method = "get"
    fields = field.Fields(IAddInternalServiceForm)
    ignoreContext = True

    @button.buttonAndHandler(u"Add")
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        service_id = data["service_id"].lower()
        service_name = data["service_name"]
        editor_group_id, validator_group_id = self.create_groups(
            service_id.capitalize(), service_name
        )
        with api.env.adopt_roles(["Manager"]):
            task_config_answer, task_config_validate = self.create_task_configs(
                service_id, service_name, editor_group_id, validator_group_id
            )
        self.set_registry_mapping(
            service_id,
            service_name,
            editor_group_id,
            validator_group_id,
            task_config_answer,
            task_config_validate,
        )

    @button.buttonAndHandler(u"Disable")
    def handleDisable(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        service_id = data["service_id"].lower()
        registry = api.portal.get_tool("portal_registry")
        registry_field = registry[
            "Products.urban.interfaces.IInternalOpinionServices.services"
        ]

        values = registry_field.get(service_id, None)

        if values:
            portal_urban = api.portal.get_tool("portal_urban")
            schedule_folder = portal_urban.opinions_schedule

            task_configs = [getattr(schedule_folder, id_) for id_ in values["task_ids"]]
            for task_config in task_configs:
                task_config.enabled = False

    @button.buttonAndHandler(u"Delete")
    def handleDelete(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        service_id = data["service_id"].lower()
        registry = api.portal.get_tool("portal_registry")
        registry_field = registry[
            "Products.urban.interfaces.IInternalOpinionServices.services"
        ]

        values = registry_field.pop(service_id, None)

        if values:
            portal_urban = api.portal.get_tool("portal_urban")
            schedule_folder = portal_urban.opinions_schedule

            with api.env.adopt_roles(["Manager"]):
                task_config_answer = getattr(schedule_folder, values["task_answer_id"])
                task_config_validate = getattr(
                    schedule_folder, values["task_validate_id"]
                )
                api.content.delete(objects=[task_config_answer, task_config_validate])

            api.group.delete(groupname=values["editor_group_id"])
            api.group.delete(groupname=values["validator_group_id"])
            registry[
                "Products.urban.interfaces.IInternalOpinionServices.services"
            ] = registry_field.copy()

    def create_groups(self, service_id, service_name):
        """ """
        editor_group = api.group.create(
            groupname="{}_editors".format(service_id),
            title="{} Editors".format(service_name),
        )
        validator_group = api.group.create(
            groupname="{}_validators".format(service_id),
            title="{} Validators".format(service_name),
        )
        portal_groups = api.portal.get_tool("portal_groups")
        portal_groups.addPrincipalToGroup(editor_group.id, "opinions_editors")
        portal_groups.addPrincipalToGroup(validator_group.id, "opinions_editors")

        return editor_group.id, validator_group.id

    def create_task_configs(
        self, service_id, service_name, editor_group, validator_group
    ):
        """ """
        portal_urban = api.portal.get_tool("portal_urban")
        schedule_folder = portal_urban.opinions_schedule
        ask_opinion_task_id = "ask_{}_opinion".format(service_id)
        give_opinion_task_id = "give_{}_opinion".format(service_id)
        task_configs = [
            {
                "type_name": "TaskConfig",
                "id": ask_opinion_task_id,
                "title": "Réception d'avis pour {}".format(service_name),
                "default_assigned_group": editor_group,
                "default_assigned_user": "to_assign",
                "creation_state": ("creation",),
                "starting_states": ("waiting_opinion",),
                "ending_states": ("opinion_validation",),
                "recurrence_states": ("waiting_opinion",),
                "creation_conditions": (
                    CreationConditionObject(
                        "urban.schedule.condition.is_internal_opinion"
                    ),
                ),
                "recurrence_conditions": (
                    RecurrenceConditionObject(
                        "urban.schedule.condition.is_internal_opinion"
                    ),
                ),
                "activate_recurrency": True,
                "start_date": "urban.schedule.start_date.asking_date",
                "calculation_delay": ("schedule.calculation_default_delay",),
                "additional_delay": 15,
            },
            {
                "type_name": "TaskConfig",
                "id": give_opinion_task_id,
                "title": "Remise d'avis {}".format(service_name),
                "default_assigned_group": validator_group,
                "default_assigned_user": "to_assign",
                "creation_state": ("opinion_validation",),
                "starting_states": ("opinion_validation",),
                "ending_states": ("opinion_given", "waiting_opinion"),
                "recurrence_states": ("opinion_validation",),
                "creation_conditions": (
                    CreationConditionObject(
                        "urban.schedule.condition.is_internal_opinion"
                    ),
                ),
                "recurrence_conditions": (
                    RecurrenceConditionObject(
                        "urban.schedule.condition.is_internal_opinion"
                    ),
                ),
                "activate_recurrency": True,
                "start_date": "urban.schedule.start_date.asking_date",
                "calculation_delay": ("schedule.calculation_default_delay",),
                "additional_delay": 15,
            },
        ]
        _create_task_configs(schedule_folder, task_configs)
        return ask_opinion_task_id, give_opinion_task_id

    def set_registry_mapping(
        self,
        service_id,
        service_name,
        editor_group,
        validator_group,
        task_answer_id,
        task_validate_id,
    ):
        """ """
        registry = api.portal.get_tool("portal_registry")
        registry_field = registry[
            "Products.urban.interfaces.IInternalOpinionServices.services"
        ]
        if not registry_field:
            registry["Products.urban.interfaces.IInternalOpinionServices.services"] = {}

        services = registry[
            "Products.urban.interfaces.IInternalOpinionServices.services"
        ]
        services[service_id.encode("utf-8")] = {
            "validator_group_id": validator_group,
            "editor_group_id": editor_group,
            "full_name": service_name.encode("utf-8"),
            "task_answer_id": task_answer_id,
            "task_validate_id": task_validate_id,
        }
        registry[
            "Products.urban.interfaces.IInternalOpinionServices.services"
        ] = services.copy()


class UpdateDefaultValuesForm(form.Form):

    method = "get"
    ignoreContext = True

    @button.buttonAndHandler(u"Update voc cache")
    def handleUpdate(self, action):
        """ """
        portal_urban = api.portal.get_tool("portal_urban")
        cache_view = portal_urban.unrestrictedTraverse("urban_vocabulary_cache")
        cache_view.update_all_cache()

    @button.buttonAndHandler(u"Clear voc cache")
    def handleClear(self, action):
        """ """
        portal_urban = api.portal.get_tool("portal_urban")
        cache_view = portal_urban.unrestrictedTraverse("urban_vocabulary_cache")
        cache_view.reset_all_cache()
