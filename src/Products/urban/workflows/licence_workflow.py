# -*- coding: utf-8 -*-

from Products.urban.workflows.adapter import LocalRoleAdapter


class StateRolesMapping(LocalRoleAdapter):
    """ """

    def __init__(self, context):
        self.context = context
        self.licence = self.context

    mapping = {
        "in_progress": {
            LocalRoleAdapter.get_readers: ("Reader",),
            LocalRoleAdapter.get_editors: ("Reader", "Editor", "Contributor"),
            LocalRoleAdapter.get_opinion_editors: ("Reader",),
        },
        "accepted": {
            LocalRoleAdapter.get_readers: ("Reader",),
            LocalRoleAdapter.get_editors: ("Reader", "Reviewer"),
            LocalRoleAdapter.get_opinion_editors: ("Reader",),
        },
        "incomplete": {
            LocalRoleAdapter.get_readers: ("Reader",),
            LocalRoleAdapter.get_editors: ("Reader", "Editor", "Contributor"),
            LocalRoleAdapter.get_opinion_editors: ("Reader",),
        },
        "refused": {
            LocalRoleAdapter.get_readers: ("Reader",),
            LocalRoleAdapter.get_editors: ("Reader", "Reviewer"),
            LocalRoleAdapter.get_opinion_editors: ("Reader",),
        },
        "retired": {
            LocalRoleAdapter.get_readers: ("Reader",),
            LocalRoleAdapter.get_editors: ("Reader", "Reviewer"),
            LocalRoleAdapter.get_opinion_editors: ("Reader",),
        },
    }
