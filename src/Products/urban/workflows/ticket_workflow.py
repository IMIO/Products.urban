# -*- coding: utf-8 -*-

from Products.urban.workflows.licence_workflow import (
    StateRolesMapping as BaseRoleMapping,
)


class StateRolesMapping(BaseRoleMapping):
    """ """

    mapping = {
        "creation": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Reader",
                "Editor",
                "Contributor",
                "Reviewer",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "prosecution_analysis": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Reader",
                "Editor",
                "Contributor",
                "Reviewer",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "in_progress_with_prosecutor": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Reader",
                "Editor",
                "Contributor",
                "Reviewer",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "in_progress_without_prosecutor": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Reader",
                "Editor",
                "Contributor",
                "Reviewer",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
        "ended": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: ("Reader", "Reviewer"),
            BaseRoleMapping.get_opinion_editors: ("Reader",),
        },
    }
