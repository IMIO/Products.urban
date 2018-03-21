# -*- coding: utf-8 -*-

from Products.Archetypes.atapi import StringWidget
from Products.Archetypes.Registry import registerWidget
from plone import api


class UrbanReferenceWidget(StringWidget):
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro': 'urbanreference',
    })

    def get_reference_url(self, value):
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
