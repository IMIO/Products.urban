# -*- coding: utf-8 -*-

from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.Registry import registerWidget
from plone import api


class UrbanReferenceWidget(StringWidget):
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro': 'urbanreference',
    })
    portal_types = []

    def __init__(self, *args, **kwargs):
        if 'portal_types' in kwargs.keys():
            self.portal_types = kwargs.pop('portal_types')
        super(UrbanReferenceWidget, self).__init__(*args, **kwargs)

    def get_reference_url(self, value):
        if self.portal_types:
            brains = api.content.find(
                getReference=value,
                portal_type=self.portal_types)
        else:
            brains = api.content.find(getReference=value)
        if len(brains) > 0:
            return brains[0].getURL()


registerWidget(
    UrbanReferenceWidget,
    title='Urban Reference',
    description=('Urban reference widget that display a link to referenced '
                 'object.'),
    used_for=('Products.Archetypes.Field.StringField', ),
)


class UrbanBackReferenceWidget(UrbanReferenceWidget):
    _properties = UrbanReferenceWidget._properties.copy()
    _properties.update({
        'macro': 'urbanbackreference',
    })


registerWidget(
    UrbanBackReferenceWidget,
    title='Urban Back Reference',
    description=('Urban back reference widget that display a link to '
                 'referenced object.'),
    used_for=('Products.Archetypes.Field.StringField', ),
)
