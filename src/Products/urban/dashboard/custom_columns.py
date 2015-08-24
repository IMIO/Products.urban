# encoding: utf-8

from Products.Archetypes.atapi import DisplayList

from imio.dashboard.adapters import CustomViewFieldsVocabularyAdapter


class UrbanCustomViewFields(CustomViewFieldsVocabularyAdapter):
    """ """

    def additionalViewFields(self):
        """See docstring in interfaces.py."""
        return DisplayList((('folder_managers', 'Folder managers'),))
