# -*- coding: utf-8 -*-

from Products.urban.workflows.urbanevent_workflow import StateRolesMapping as BaseRolesMapping

from collections import OrderedDict


class StateRolesMapping(BaseRolesMapping):
    """
    """

    mapping = {
        'draft': OrderedDict([
            (BaseRolesMapping.get_readers, ('Reader',)),
            (BaseRolesMapping.get_editors, ('Editor',)),
            (BaseRolesMapping.get_opinion_editors, ('Reader',)),
        ]),

        'decision_in_progress': OrderedDict([
            (BaseRolesMapping.get_readers, ('Reader',)),
            (BaseRolesMapping.get_editors, ('Editor',)),
            (BaseRolesMapping.get_opinion_editors, ('Reader',)),
        ]),

        'closed': OrderedDict([
            (BaseRolesMapping.get_readers, ('Reader',)),
            (BaseRolesMapping.get_editors, ('Editor',)),
            (BaseRolesMapping.get_opinion_editors, ('Reader',)),
        ]),

    }
