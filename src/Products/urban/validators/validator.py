# -*- coding: utf-8 -*-

from DateTime import DateTime

from plone import api

from Products.urban import UrbanMessage as _
from Products.urban.config import URBAN_TYPES

from Products.validation.interfaces.IValidator import IValidator

from zope.interface import implements
from zope.i18n import translate

import re


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
                return translate(
                    _('error_textcfg',
                      default=u"The field '${fieldname}' is configured twice",
                      mapping={'fieldname': val['fieldname']})
                )
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
            if 'orderindex_' in line and line['orderindex_'] != 'template_row_marker' and not line['street']:
                return translate(
                    _('error_streetname', default=u"Please select a valid street")
                )
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
        catalog = api.portal.get_tool('portal_catalog')
        portal_urban = api.portal.get_tool('portal_urban')

        licence_config = licence.getLicenceConfig()
        source = licence_config.getNumerotationSource()
        regex = licence_config.getReference_regex()
        types_to_check = [t for t in URBAN_TYPES if getattr(portal_urban, t.lower()).getNumerotationSource() == source]
        match = re.match(regex, value)
        if not match:
            return translate(
                _('error_reference_format', default=u"This reference does not match the expected format of {}".format(regex))
            )

        ref_num = match.group() or match.groups()
        if not ref_num:
            return 1

        similar_licences = catalog(getReference=ref_num, portal_type=types_to_check)
        if not similar_licences or (len(similar_licences) == 1 and licence.UID() == similar_licences[0].UID):
            return 1
        return translate(
            _('error_reference', default=u"This reference has already been encoded")
        )


class procedureChoiceValidator:
    """
    """
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if type(value) is str:
            return True

        if 'ukn' in value and len(value) > 2:
            return translate(
                _('error_procedure_choice_unknown',
                  default=u"Cannot select 'unknown' with another value")
            )
        if 'simple' in value and len(value) > 2:
            return translate(
                _('error_procedure_choice_simple',
                  default=u"Cannot select 'simple' with another value")
            )
        if ('light_inquiry' in value) + ('inquiry' in value) + ('initiative_light_inquiry' in value) > 1:
            return translate(
                _('error_multiple_inquiry_type',
                  default=u"Please select only ONE of the inquiry types")
            )
        if 'class_1' in value and 'class_2' in value:
            return translate(
                _('error_multiple_class_type',
                  default=u"Cannot select class 1 and class 2 toghether")
            )
        return True


class isValidSectionValidator:
    """
    Validators for parcel reference values, used in the case where the parcel is addded manually
    """
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
        if value == '' or (len(value) < 4 and value.isdigit()):
            return 1
        return translate(_('error_puissance', default=u"Puissance should be a number < 100"))


class isReferenceValidator(object):
    """
    Check that the reference is used by a licence
    """
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        catalog = api.portal.get_tool('portal_catalog')
        if not value:
            return 1
        if len(catalog(getReference=value)) > 0:
            return 1
        return translate(_('error_reference_does_not_exist', default=u"The reference does not exist"))


class isInteger:
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if value == '' or value.isdigit():
            return 1
        return translate(_('error_integer', default=u"Delay should be an integer"))
