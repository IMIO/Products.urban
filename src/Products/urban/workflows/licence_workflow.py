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

    mapping = {
        'in_progress': {
            LocalRoleAdapter.get_readers: ('Reader',),
            LocalRoleAdapter.get_editors: ('Reader', 'Editor', 'Contributor'),
        },

        'accepted': {
            LocalRoleAdapter.get_readers: ('Reader',),
            LocalRoleAdapter.get_editors: ('Reader', 'Reviewer'),
        },

        'incomplete': {
            LocalRoleAdapter.get_readers: ('Reader',),
            LocalRoleAdapter.get_editors: ('Reader', 'Editor', 'Contributor'),
        },

        'refused': {
            LocalRoleAdapter.get_readers: ('Reader',),
            LocalRoleAdapter.get_editors: ('Reader', 'Reviewer'),
        },

        'retired': {
            LocalRoleAdapter.get_readers: ('Reader',),
            LocalRoleAdapter.get_editors: ('Reader', 'Reviewer'),
        },

    }
