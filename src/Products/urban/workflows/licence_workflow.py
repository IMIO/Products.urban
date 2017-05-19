# -*- coding: utf-8 -*-

from Products.urban.workflows.adapter import LocalRoleAdapter


class StateRolesMapping(LocalRoleAdapter):
    """ """

    mapping = {
        'in_progress': {
            'urban_readers': ('Reader',),
            'urban_editors': ('Reader', 'Editor', 'Contributor'),
            'urban_managers': ('Reader', 'Editor', 'Contributor', 'Reviewer'),
        },

        'accepted': {
            'urban_readers': ('Reader',),
            'urban_editors': ('Reader', 'Reviewer'),
            'urban_managers': ('Reader', 'Reviewer'),
        },

        'incomplete': {
            'urban_readers': ('Reader',),
            'urban_editors': ('Reader', 'Editor', 'Contributor'),
            'urban_managers': ('Reader', 'Editor', 'Contributor', 'Reviewer'),
        },

        'complete': {
            'urban_readers': ('Reader',),
            'urban_editors': ('Reader', 'Editor', 'Contributor'),
            'urban_managers': ('Reader', 'Editor', 'Contributor', 'Reviewer'),
        },

        'refused': {
            'urban_readers': ('Reader',),
            'urban_editors': ('Reader', 'Contributor'),
            'urban_managers': ('Reader', 'Contributor'),
        },

        'retired': {
            'urban_readers': ('Reader',),
            'urban_editors': ('Reader', 'Contributor'),
            'urban_managers': ('Reader', 'Contributor'),
        },

    }
