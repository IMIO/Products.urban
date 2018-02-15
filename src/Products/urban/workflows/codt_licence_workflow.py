# -*- coding: utf-8 -*-

from Products.urban.workflows.licence_workflow import StateRolesMapping as BaseRoleMapping


class StateRolesMapping(BaseRoleMapping):
    """ """

    mapping = {
        'deposit': {
            BaseRoleMapping.get_readers: ('Reader',),
            BaseRoleMapping.get_editors: ('Reader', 'Editor', 'Contributor'),
        },

        'accepted': {
            BaseRoleMapping.get_readers: ('Reader',),
            BaseRoleMapping.get_editors: ('Reader', 'Reviewer'),
        },

        'incomplete': {
            BaseRoleMapping.get_readers: ('Reader',),
            BaseRoleMapping.get_editors: ('Reader', 'Editor', 'Contributor'),
        },

        'complete': {
            BaseRoleMapping.get_readers: ('Reader',),
            BaseRoleMapping.get_editors: ('Reader', 'Editor', 'Contributor'),
        },

        'refused': {
            BaseRoleMapping.get_readers: ('Reader',),
            BaseRoleMapping.get_editors: ('Reader', 'Contributor'),
        },

        'retired': {
            BaseRoleMapping.get_readers: ('Reader',),
            BaseRoleMapping.get_editors: ('Reader', 'Contributor'),
        },

        'inacceptable': {
            BaseRoleMapping.get_readers: ('Reader',),
            BaseRoleMapping.get_editors: ('Reader', 'Contributor'),
        },

    }
