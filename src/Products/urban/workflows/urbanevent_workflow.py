# -*- coding: utf-8 -*-

from Products.urban.interfaces import ICODT_UniqueLicence
from Products.urban.interfaces import IEnvironmentBase
from Products.urban.interfaces import IEnvironmentOnlyEvent
from Products.urban.interfaces import IIntegratedLicence
from Products.urban.interfaces import IUniqueLicence
from Products.urban.interfaces import IUrbanAndEnvironmentEvent
from Products.urban.interfaces import IUrbanOrEnvironmentEvent
from Products.urban.workflows.adapter import LocalRoleAdapter


class StateRolesMapping(LocalRoleAdapter):
    """
    """

    def __init__(self, context):
        self.context = context
        self.event = context
        self.licence = self.context.aq_parent

    def get_allowed_groups(self, licence, event):
        integrated_licence = IIntegratedLicence.providedBy(licence)
        if IEnvironmentBase.providedBy(licence) or integrated_licence:
            if IUniqueLicence.providedBy(licence) or ICODT_UniqueLicence.providedBy(licence):
                if IEnvironmentOnlyEvent.providedBy(event):
                    return 'environment_only'
                elif IUrbanOrEnvironmentEvent.providedBy(event):
                    if 'urb' in licence.getFolderTendency():
                        return 'urban_only'
                    elif 'env' in licence.getFolderTendency():
                        return 'environment_only'
                elif IUrbanAndEnvironmentEvent.providedBy(event):
                    return 'urban_and_environment'
                else:
                    return 'urban_only'
            else:
                return 'environment_only'
        else:
            return 'urban_only'

    def get_editors(self):
        """ """
        event = self.event
        licence = self.licence
        mapping = {
            'urban_only': [
                'urban_editors',
            ],
            'environment_only': [
                'environment_editors',
            ],
            'urban_and_environment': [
                'urban_editors',
                'environment_editors',
            ]
        }
        allowed_group = self.get_allowed_groups(licence, event)
        if allowed_group in mapping:
            return mapping.get(allowed_group)

    def get_readers(self):
        """ """
        event = self.event
        licence = self.licence
        mapping = {
            'urban_only': [
                'urban_readers',
            ],
            'environment_only': [
                'environment_readers',
            ],
            'urban_and_environment': [
                'urban_readers',
                'environment_readers',
            ]
        }
        allowed_group = self.get_allowed_groups(licence, event)
        if allowed_group in mapping:
            return mapping.get(allowed_group)

    mapping = {
        'in_progress': {
            get_editors: ('Editor',),
            get_readers: ('Reader',),
            LocalRoleAdapter.get_opinion_editors: ('Reader',),
        },

        'closed': {
            get_editors: ('Editor',),
            get_readers: ('Reader',),
            LocalRoleAdapter.get_opinion_editors: ('Reader',),
        },
    }
