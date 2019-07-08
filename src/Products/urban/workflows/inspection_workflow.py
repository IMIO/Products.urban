# -*- coding: utf-8 -*-

from Products.urban.workflows.licence_workflow import StateRolesMapping as BaseRoleMapping


class StateRolesMapping(BaseRoleMapping):
    """ """

    mapping = {
        'creation': {
            BaseRoleMapping.get_readers: ('Reader',),
            BaseRoleMapping.get_editors: ('Reader', 'Editor', 'Contributor', 'Reviewer'),
            BaseRoleMapping.get_opinion_editors: ('Reader',),
        },

        'analysis': {
            BaseRoleMapping.get_readers: ('Reader',),
            BaseRoleMapping.get_editors: ('Reader', 'Editor', 'Contributor', 'Reviewer'),
            BaseRoleMapping.get_opinion_editors: ('Reader',),
        },

        'administrative_answer': {
            BaseRoleMapping.get_readers: ('Reader',),
            BaseRoleMapping.get_editors: ('Reader', 'Editor', 'Contributor', 'Reviewer'),
            BaseRoleMapping.get_opinion_editors: ('Reader',),
        },

        'ended': {
            BaseRoleMapping.get_readers: ('Reader',),
            BaseRoleMapping.get_editors: ('Reader', 'Reviewer'),
            BaseRoleMapping.get_opinion_editors: ('Reader',),
        },
    }
