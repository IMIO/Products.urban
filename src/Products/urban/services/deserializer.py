# -*- coding: utf-8 -*-
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.atcontent import DeserializeFromJson
from plone.restapi.interfaces import IDeserializeFromJson
from Products.Archetypes.interfaces import IBaseObject
from Products.urban.interfaces import IProductUrbanLayer
from zope.component import adapter
from zope.interface import implementer


@implementer(IDeserializeFromJson)
@adapter(IBaseObject, IProductUrbanLayer)
class DeserializeFromJsonUrban(DeserializeFromJson):
    def validate(self):
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
