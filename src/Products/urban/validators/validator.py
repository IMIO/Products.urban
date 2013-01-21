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
                return translate(_('error_textcfg',
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
                return translate(_('error_streetname',
                                    default=u"Please select a valid street"))
        return 1


class isValidSectionValidator:
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if value == '' or (len(value) == 1 and value.isalpha() and value.isupper()):
            return 1
        return translate(_('error_section', default=u"Section should be a single uppercase letter"))


class isValidRadicalValidator:
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if value == '' or value.isdigit():
            return 1
        return translate(_('error_radical', default=u"Radical should be a number"))


class isValidBisValidator:
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if value == '' or (len(value) < 3 and value.isdigit()):
            return 1
        return translate(_('error_bis', default=u"Bis should be a number < 100"))


class isValidExposantValidator:
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if value == '' or (len(value) == 1 and value.isalpha() and value.isupper()):
            return 1
        return translate(_('error_exposant', default=u"Exposant should be a single uppercase letter"))


class isValidPuissanceValidator:
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if value == '' or (len(value) < 3 and value.isdigit()):
            return 1
        return translate(_('error_puissance', default=u"Puissance should be a number < 100"))
