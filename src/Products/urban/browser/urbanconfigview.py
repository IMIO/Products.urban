# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.urban import UrbanMessage as _
from Products.urban.setuphandlers import _create_task_configs
from Products.urban.browser.table.urbantable import InternalOpinionServicesTable

from imio.schedule.content.object_factories import CreationConditionObject

from plone import api

from z3c.form import button
from z3c.form import form, field

from zope.interface import Interface
from zope.schema import TextLine


class UrbanConfigView(BrowserView):
    """
    """
    def __init__(self, context, request):
        super(UrbanConfigView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.form = AddInternalServiceForm(context, request)
        self.form.update()

    def getTabMacro(self, tab):
        context = aq_inner(self.context)
        macro_name = '%s_macro' % tab
        macro = context.unrestrictedTraverse('@@urbanconfigmacros/%s' % macro_name)
        return macro

    def getTabs(self):
        return [
            'public_settings',
            'licences_config',
            'vocabulary_folders',
            'schedule',
            'internal_services',
            'admin_settings'
        ]

    def getAdminFolders(self):
        context = aq_inner(self.context)
        names = ['additional_layers']
        folders = [folder for folder in context.objectValues('ATFolder') if folder.id in names]
        return folders

    def getMiscConfigFolders(self):
        context = aq_inner(self.context)
        names = ['globaltemplates', 'dashboardtemplates', 'foldermanagers', 'streets']
        folders = [folder for folder in context.objectValues('ATFolder') if folder.id in names]
        return folders

    def getVocabularyFolders(self):
        context = aq_inner(self.context)
        other_folders = self.getAdminFolders() + self.getMiscConfigFolders()
        folders = [folder for folder in context.objectValues('ATFolder') if folder not in other_folders]
        return folders

    def getScheduleConfigs(self):
        context = aq_inner(self.context)
        survey_schedule = getattr(context, 'survey_schedule', None)
        opinions_schedule = getattr(context, 'opinions_schedule', None)
        schedules = [schedule for schedule in [survey_schedule, opinions_schedule] if schedule]
        return schedules

    def renderInternalServicesListing(self):
        table = InternalOpinionServicesTable(self.context, self.request)
        table.update()
        return table.render()


class IAddInternalServiceForm(Interface):

    service_name = TextLine(
        title=_(u'Service full name'),
        required=True
    )

    service_id = TextLine(
        title=_(u'Service id'),
        required=True
    )


class AddInternalServiceForm(form.Form):

    method = 'get'
    fields = field.Fields(IAddInternalServiceForm)
    ignoreContext = True

    def updateWidgets(self):
        super(AddInternalServiceForm, self).updateWidgets()

    @button.buttonAndHandler(u'Add')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        service_id = data['service_id']
        service_name = data['service_name']
        editor_group_id, validator_group_id = self.create_groups(service_id, service_name)
        with api.env.adopt_roles(['Manager']):
            task_config_ids = self.create_task_configs(service_id, service_name, editor_group_id, validator_group_id)
        self.set_registry_mapping(service_id, service_name, editor_group_id, validator_group_id, task_config_ids)

    @button.buttonAndHandler(u'Disable')
    def handleDisable(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        service_id = data['service_id']
        registry = api.portal.get_tool('portal_registry')
        registry_field = registry['Products.urban.interfaces.IInternalOpinionServices.services']

        values = registry_field.get(service_id, None)

        if values:
            portal_urban = api.portal.get_tool('portal_urban')
            schedule_folder = portal_urban.opinions_schedule

            task_configs = [getattr(schedule_folder, id_) for id_ in values['task_ids']]
            for task_config in task_configs:
                task_config.enabled = False

    @button.buttonAndHandler(u'Delete')
    def handleDelete(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        service_id = data['service_id']
        registry = api.portal.get_tool('portal_registry')
        registry_field = registry['Products.urban.interfaces.IInternalOpinionServices.services']

        values = registry_field.pop(service_id, None)

        if values:
            portal_urban = api.portal.get_tool('portal_urban')
            schedule_folder = portal_urban.opinions_schedule

            with api.env.adopt_roles(['Manager']):
                task_configs = [getattr(schedule_folder, id_) for id_ in values['task_ids']]
                api.content.delete(objects=task_configs)

            api.group.delete(groupname=values['editor_group_id'][0])
            api.group.delete(groupname=values['validator_group_id'][0])
            registry['Products.urban.interfaces.IInternalOpinionServices.services'] = registry_field

    def create_groups(self, service_id, service_name):
        """
        """
        editor_group = api.group.create(
            groupname='{}_editor'.format(service_id),
            title='{} Editors'.format(service_name),
        )
        validator_group = api.group.create(
            groupname='{}_validator'.format(service_id),
            title='{} Validators'.format(service_name),
        )
        portal_groups = api.portal.get_tool('portal_groups')
        portal_groups.addPrincipalToGroup(editor_group.id, 'opinions_editors')
        portal_groups.addPrincipalToGroup(validator_group.id, 'opinions_editors')

        return editor_group.id, validator_group.id

    def create_task_configs(self, service_id, service_name, editor_group, validator_group):
        """
        """
        portal_urban = api.portal.get_tool('portal_urban')
        schedule_folder = portal_urban.opinions_schedule
        ask_opinion_task_id = 'ask_{}_opinion'.format(service_id)
        give_opinion_task_id = 'give_{}_opinion'.format(service_id)
        task_configs = [
            {
                'type_name': 'TaskConfig',
                'id': ask_opinion_task_id,
                'title': 'Réception d\'avis pour {}'.format(service_name),
                'default_assigned_group': editor_group,
                'default_assigned_user': 'to_assign',
                'creation_state': ('creation',),
                'starting_states': ('waiting_opinion',),
                'ending_states': ('opinion_validation',),
                'creation_conditions': (
                    CreationConditionObject('urban.schedule.condition.is_internal_opinion'),
                ),
                'start_date': 'liege.urban.schedule.asking_date',
                'calculation_delay': (
                    'schedule.calculation_default_delay',
                ),
                'additional_delay': 15,
            },
            {
                'type_name': 'TaskConfig',
                'id': give_opinion_task_id,
                'title': 'Remise d\'avis {}'.format(service_name),
                'default_assigned_group': validator_group,
                'default_assigned_user': 'to_assign',
                'creation_state': ('waiting_opinion',),
                'starting_states': ('opinion_validation',),
                'ending_states': ('opinion_given',),
                'creation_conditions': (
                    CreationConditionObject('urban.schedule.condition.is_internal_opinion'),
                ),
                'start_date': 'liege.urban.schedule.asking_date',
                'calculation_delay': (
                    'schedule.calculation_default_delay',
                ),
                'additional_delay': 15,
            }
        ]
        _create_task_configs(schedule_folder, task_configs)
        return [ask_opinion_task_id, give_opinion_task_id]

    def set_registry_mapping(self, service_id, service_name, editor_group, validator_group, task_config_ids):
        """
        """
        registry = api.portal.get_tool('portal_registry')
        registry_field = registry['Products.urban.interfaces.IInternalOpinionServices.services']
        if not registry_field:
            registry['Products.urban.interfaces.IInternalOpinionServices.services'] = {}

        services = registry['Products.urban.interfaces.IInternalOpinionServices.services']
        services[service_id] = {
            'validator_group_id': [validator_group],
            'editor_group_id': [editor_group],
            'full_name': [service_name],
            'task_ids': task_config_ids,
        }
