# -*- coding: utf-8 -*-

from Products.urban.interfaces import ICODT_UniqueLicence
from Products.urban.interfaces import IEnvironmentBase
from Products.urban.interfaces import IUniqueLicence
from Products.urban.workflows.adapter import LocalRoleAdapter


class StateRolesMapping(LocalRoleAdapter):
    """ """

    def __init__(self, context):
        self.context = context
        self.licence = self.context

    def get_allowed_groups(self, licence):
        if IEnvironmentBase.providedBy(licence):
            if IUniqueLicence.providedBy(licence) or ICODT_UniqueLicence.providedBy(licence):
                return 'urban_and_environment'
            else:
                return 'environment_only'
        else:
            return 'urban_only'

    def get_editors(self):
        """ """
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
        allowed_group = self.get_allowed_groups(licence)
        if allowed_group in mapping:
            return mapping.get(allowed_group)

    def get_readers(self):
        """ """
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
        allowed_group = self.get_allowed_groups(licence)
        if allowed_group in mapping:
            return mapping.get(allowed_group)

    mapping = {
        'in_progress': {
            get_readers: ('Reader',),
            get_editors: ('Reader', 'Editor', 'Contributor'),
        },

        'accepted': {
            get_readers: ('Reader',),
            get_editors: ('Reader', 'Reviewer'),
        },

        'incomplete': {
            get_readers: ('Reader',),
            get_editors: ('Reader', 'Editor', 'Contributor'),
        },

        'refused': {
            get_readers: ('Reader',),
            get_editors: ('Reader', 'Reviewer'),
        },

        'retired': {
            get_readers: ('Reader',),
            get_editors: ('Reader', 'Reviewer'),
        },

    }
