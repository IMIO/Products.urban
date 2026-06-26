# -*- coding: utf-8 -*-

from Products.urban.workflows.urbanevent_workflow import (
    StateRolesMapping as BaseRolesMapping
)


class StateRolesMapping(BaseRolesMapping):
    """
    """

    mapping = {
        "draft": {
            BaseRolesMapping.get_editors: ("Editor",),
            BaseRolesMapping.get_readers: ("Reader",),
        },

        "to_validate": {
            BaseRolesMapping.get_editors: ("Editor", "Contributor"),
            BaseRolesMapping.get_readers: ("Reader",),
        },

        "to_send": {
            BaseRolesMapping.get_editors: ("Editor", "Contributor"),
            BaseRolesMapping.get_readers: ("Reader",),
        },

        "closed": {
            BaseRolesMapping.get_editors: ("Editor", "Contributor"),
            BaseRolesMapping.get_readers: ("Reader",),
        },

    }
