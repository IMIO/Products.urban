# -*- coding: utf-8 -*-

from Products.urban.workflows.adapter import LocalRoleAdapter


class StateRolesMapping(LocalRoleAdapter):
    """
    """

    mapping = {
        'in_progress': {
            'urban_managers': ('Editor',),
            'urban_editors': ('Editor',),
            'urban_readers': ('Reader',),
        },

        'closed': {
            'urban_managers': ('Editor',),
            'urban_editors': ('Editor',),
            'urban_readers': ('Reader',),
        },
    }
