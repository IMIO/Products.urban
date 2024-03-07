# -*- coding: utf-8 -*-

from collections import OrderedDict

from Products.Five import BrowserView

from Products.urban.interfaces import IUrbanConfigurationValue

from zope.annotation import IAnnotations


class UrbanVocabulariesCache(BrowserView):
    def update_all_cache(self):
        portal_urban = self.context
        self.update_procedure_all_vocabulary_cache(portal_urban)

        licences_configs = portal_urban.get_all_licence_configs()
        for config in licences_configs:
            self.update_procedure_all_vocabulary_cache(config)

    def _to_dict(self, list_of_dicts):
        dict_ = OrderedDict([(v["id"], v) for v in list_of_dicts])
        return dict_

    def update_procedure_all_vocabulary_cache(self, config_folder):
        voc_folders = config_folder.get_vocabulary_folders()
        self._update_procedure_vocabulary_cache(config_folder, voc_folders)

    def update_procedure_vocabulary_cache(self, config_folder, voc_folder):
        voc_folders = [voc_folder]
        self._update_procedure_vocabulary_cache(config_folder, voc_folders)

    def _update_procedure_vocabulary_cache(self, config_folder, voc_folders=[]):
        annotations = IAnnotations(config_folder)
        vocabularies = annotations.get("Products.urban.vocabulary_cache", {})
        for voc_folder in voc_folders:
            stored_value = self._to_dict(vocabularies.get(voc_folder.id, []))
            updated_values = self._to_dict(
                self.voc_folder_to_vocabulary_list(voc_folder)
            )
            # disable deleted voc terms but still keep them in the cache
            updated_values_UIDS = set([v["UID"] for v in updated_values.values()])
            for k, v in stored_value.iteritems():
                if k not in updated_values and v["UID"] not in updated_values_UIDS:
                    v["enabled"] = False
                    # use updated_values as the base for the result to ensures
                    # we also keep track of the values reordering
                    updated_values[k] = v
            vocabularies[voc_folder.id] = updated_values.values()
        annotations["Products.urban.vocabulary_cache"] = vocabularies

    def voc_folder_to_vocabulary_list(self, folder):
        vocabulary_list = []
        for voc_term in folder.objectValues():
            if IUrbanConfigurationValue.providedBy(voc_term):
                vocterm_dict = voc_term.to_dict()
                vocabulary_list.append(vocterm_dict)
        return vocabulary_list

    def reset_all_cache(self):
        portal_urban = self.context

        configs = portal_urban.get_all_licence_configs() + [portal_urban]
        for config in configs:
            annotations = IAnnotations(config)
            annotations["Products.urban.vocabulary_cache"] = {}
