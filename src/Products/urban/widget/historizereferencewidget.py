# -*- coding: utf-8 -*-

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.Archetypes.Registry import registerWidget


class HistorizeReferenceBrowserWidget(ReferenceBrowserWidget):
    _properties = ReferenceBrowserWidget._properties.copy()
    _properties.update({
        'macro': 'historizereferencebrowser',
    })


registerWidget(
    HistorizeReferenceBrowserWidget,
    title='Historize Reference Browser',
    description=('Reference widget that allows you to browse or '
                 'search the portal for objects to refer to and keep and '
                 'history of the changes.'),
    used_for=('Products.Archetypes.Field.ReferenceField',)
)
