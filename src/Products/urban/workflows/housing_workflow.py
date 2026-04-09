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
                "Editor",
                "Reviewer",
                "Contributor",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reviewer", "Contributor"),
        },
        "analysis": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Editor",
                "Reviewer",
                "Contributor",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reviewer", "Contributor"),
        },
        "1st_observation": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Editor",
                "Reviewer",
                "Contributor",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reviewer", "Contributor"),
        },
        "2nd_observation": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Editor",
                "Reviewer",
                "Contributor",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reviewer", "Contributor"),
        },
        "ended": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Editor",
                "Reviewer",
                "Contributor",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reviewer", "Contributor"),
        },
        "annual_observation": {
            BaseRoleMapping.get_readers: ("Reader",),
            BaseRoleMapping.get_editors: (
                "Editor",
                "Reviewer",
                "Contributor",
            ),
            BaseRoleMapping.get_opinion_editors: ("Reviewer", "Contributor"),
        },
    }
