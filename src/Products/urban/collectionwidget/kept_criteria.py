# -*- coding: utf-8 -*-


class KeptCriteria(object):
    """This adapter makes it possible to override default implementation
    of which criteria are kept when changing from a collection to another.
    By default, this is done smartly by disabling criteria using indexes
    already managed by the selected collection."""

    def __init__(self, context, widget):
        self.context = context
        self.widget = widget
        self.request = self.context.REQUEST

    def compute(self, collection_uid):
        """
        Do not disable filter widget values 'forced' in collection.
        """
        return {}
