from Products.validation.interfaces.IValidator import IValidator
from zope.interface import implements
from zope.i18n import translate
from Products.urban import UrbanMessage as _

class isTextFieldConfiguredValidator:
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        configured_fields = []
        for val in value[:-1]:
            if val['fieldname'] not in configured_fields:
                configured_fields.append(val['fieldname'])
            else:
                return translate(_('urban_textcfgerror',
                                    default=u"The field '${fieldname}' is configured twice",
                                    mapping={'fieldname':val['fieldname']}))
        return 1


class isValidStreetNameValidator:
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        for line in value:
            if line['orderindex_'] != 'template_row_marker' and not line['street']:
                return translate(_('urban_streetnameerror',
                                    default=u"Please select a valid street"))
        return 1
