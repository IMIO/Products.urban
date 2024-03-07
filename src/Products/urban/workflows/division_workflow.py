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
        },
        "need_parceloutlicence": {
            LocalRoleAdapter.get_readers: ("Reader",),
            LocalRoleAdapter.get_editors: ("Reader", "Reviewer"),
        },
        "accepted": {
            LocalRoleAdapter.get_readers: ("Reader",),
            LocalRoleAdapter.get_editors: ("Reader", "Reviewer"),
        },
    }
