# -*- coding: utf-8 -*-

from Products.urban.workflows.licence_workflow import (
    StateRolesMapping as BaseRoleMapping,
)


class StateRolesMapping(BaseRoleMapping):
    """
    As for now codt_licence states and env licences states are the same.
    """

    mapping = {
        "deposit": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Reader",
                "Editor",
                "Contributor",
                "Reviewer",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "accepted": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: ("Reader", "Reviewer"),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "incomplete": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Reader",
                "Editor",
                "Contributor",
                "Reviewer",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "complete": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Reader",
                "Editor",
                "Contributor",
                "Reviewer",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "college_opinion": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Reader",
                "Editor",
                "Contributor",
                "Reviewer",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "FT_opinion": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Reader",
                "Editor",
                "Contributor",
                "Reviewer",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "final_decision_in_progress": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Reader",
                "Editor",
                "Contributor",
                "Reviewer",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "refused": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: ("Reader", "Reviewer"),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "retired": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: ("Reader", "Reviewer"),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "inacceptable": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: ("Reader", "Reviewer"),
        },
    }
