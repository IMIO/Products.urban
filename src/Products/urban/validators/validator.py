from Products.validation.interfaces.IValidator import IValidator
from zope.interface import implements
from zope.i18n import translate
from Products.urban import UrbanMessage as _
from Products.CMFCore.utils import getToolByName

class isTextFieldConfiguredValidator:
    """
    Check if a text field has been already configured or not, so it cannot be configured twice
    and have several conflictual default values
    """
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
    """
     Check that theres no empty adress defined on the workLocation field
    """
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        for line in value:
            if line['orderindex_'] != 'template_row_marker' and not line['street']:
                return translate(_('error_streetname',
                                    default=u"Please select a valid street"))
        return 1



class isNotDuplicatedReferenceValidator:
    """
     Check that the reference of the licence is not already used on another licence
     (can happen when two licences are edited at the same time)
    """
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        licence = kwargs['instance']
        catalog = getToolByName(licence, 'portal_catalog')
        similar_licences = catalog(portal_type=licence.portal_type, getReference=value)
        if not similar_licences or (len(similar_licences) == 1 and licence.UID() == similar_licences[0].UID):
            return 1
        return translate(_('error_reference',
                            default=u"This reference has already been encoded"))


class procedureChoiceValidator:
    """
    """
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        licence = kwargs['instance']
        if 'ukn' in value and len(value) > 2:
            return translate(
                _('error_procedure_choice',
                default=u"Cannot select 'unknown' with another value")
            )
        return True


"""
Validators for parcel reference values, used in the case where the parcel is addded manually
"""
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
        if value == '' or (len(value) < 3 and ((value.isalpha() and value.isupper()) or value.isdigit())):
            return 1
        return translate(_('error_exposant', default=u"Exposant should be uppercase letters or digits"))


class isValidPuissanceValidator:
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if value == '' or (len(value) < 3 and value.isdigit()):
            return 1
        return translate(_('error_puissance', default=u"Puissance should be a number < 100"))
