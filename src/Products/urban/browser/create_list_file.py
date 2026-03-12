# -*- coding: utf-8 -*-

from Products.urban.migration.to_DX.migration_utils import GenerateCotentTypeList


class GeneratePortioOutList(GenerateCotentTypeList):
    src_portal_type = "PortionOut"


class GenerateParcelList(GenerateCotentTypeList):
    src_portal_type = "Parcel"
    sort_order="ascending"

    def condition(self, data):
        number = getattr(data, "street_number", None)
        if number is None:
            return False
        return isinstance(number ,int) or isinstance(number ,float)
