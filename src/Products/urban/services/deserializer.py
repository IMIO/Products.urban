# -*- coding: utf-8 -*-
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.atcontent import DeserializeFromJson
from plone.restapi.interfaces import IDeserializeFromJson
from Products.Archetypes.interfaces import IBaseObject
from Products.urban.interfaces import IProductUrbanLayer
from Products.urban.browser.exportimport.interfaces import IConfigImportMarker
from zope.component import adapter
from zope.interface import implementer


@implementer(IDeserializeFromJson)
@adapter(IBaseObject, IProductUrbanLayer)
class DeserializeFromJsonUrban(DeserializeFromJson):
    def validate(self):
        if IConfigImportMarker.providedBy(self.request):
            return self.urban_config_validate()
        return self.common_validate()

    def common_validate(self):
        """
        Add a key "disable_check_ref_format" with a value true in the body json
        to disable the check of the format of the reference field
        """
        data = json_body(self.request)
        errors = super(DeserializeFromJsonUrban, self).validate()

        if (
            "disable_check_ref_format" in data
            and data["disable_check_ref_format"]
            and "reference" in errors
            and errors["reference"].startswith(
                "This reference does not match the expected format of"
            )
        ):
            del errors["reference"]

        return errors

    def urban_config_validate(self):
        keys = ["deadLineDelay", "alertDelay"]
        self._change_int_to_str_context(keys)
        errors = super(DeserializeFromJsonUrban, self).validate()
        self._change_int_to_str_context(keys)
        return errors

    def _change_int_to_str_context(self, keys=[]):
        for key in keys:
            getter = getattr(
                self.context, "getRaw{}{}".format(key[0].capitalize(), key[1:]), None
            )
            if getter is None:
                continue
            value = getter()
            if isinstance(value, int):
                value = str(value)
            elif isinstance(value, str):
                try:
                    value = int(value)
                except Exception:
                    continue
            setattr(self.context, key, value)
