# -*- coding: utf-8 -*-

from imio.history.adapters import BaseImioHistoryAdapter
from plone.memoize.instance import memoize


class BaseEnvironmentHistoryAdapter(BaseImioHistoryAdapter):

    def format_history(self, line):
        if line['action'].endswith('_history'):
            return self.format_history_register(line)
        elif line['action'].startswith('update_'):
            return self.format_update_history(line)
        return line

    def format_history_register(self, line):
        """Format the comment for an history register event"""
        keys = [k.replace('comment_', '') for k in line.keys()
                if k.startswith('comment_')]
        values = [
            u'<span class="discreet">{0}: {1}</span>'.format(
                k, line['comment_{0}'.format(k)]
            )
            for k in keys
        ]
        line['comments'] = u'{0}'.format(u'<br>'.join(values))
        return line

    def format_update_history(self, line):
        """Format the comment for an update"""
        key = '{0}_history'.format(line['action'].replace('update_', ''))
        line['comments'] = u'<span class="discreet">{0}</span>'.format(
            u', '.join(line[key]),
        )
        return line


class EnvironmentRubricsHistory(BaseEnvironmentHistoryAdapter):
    history_attr_name = 'rubrics_history'
    history_type = 'rubrics_history'

    @memoize
    def get_history_data(self):
        history = super(EnvironmentRubricsHistory, self).get_history_data()
        history = [l for l in history if l['action'] != 'history_register']
        return map(self.format_history, history)


class EnvironmentAdditionalLegalConditionsHistory(BaseEnvironmentHistoryAdapter):
    history_attr_name = 'additionalLegalConditions_history'
    history_type = 'additionalLegalConditions_history'

    @memoize
    def get_history_data(self):
        history = super(EnvironmentAdditionalLegalConditionsHistory, self).get_history_data()
        history = [l for l in history if l['action'] != 'history_register']
        return map(self.format_history, history)
