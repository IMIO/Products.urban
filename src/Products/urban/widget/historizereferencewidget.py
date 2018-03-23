# -*- coding: utf-8 -*-

import z3c.form
import zope.interface
from Products.Archetypes.Registry import registerWidget
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from z3c.form import button
from zope import schema
from zope.interface.interface import InterfaceClass
from Products.urban.events.envclassEvents import get_value_history_by_index
from plone.z3cform.layout import FormWrapper
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


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


class IHistorizeReference(zope.interface.Interface):
    comment = schema.Text(
        title=u'Comment',
        required=False
    )


class HistorizeReferenceForm(z3c.form.form.Form):
    zope.interface.implements(z3c.form.interfaces.IFieldsForm)
    ignoreContext = True

    historize_key = {
        'rubrics': 'rubrics_history',
        'additionalLegalConditions': 'alc_history'
    }

    def update(self):
        historize_field = self.request.form.get('fieldRealName')
        if historize_field is not None:
            last_history_value = get_value_history_by_index(self.context, self.historize_key.get(historize_field), -2)
            actual_values = get_value_history_by_index(self.context, self.historize_key.get(historize_field), -1)
            values = []
            values.extend(last_history_value)
            values.extend(actual_values)
            values = set(values)

            for idx, change in enumerate(values):
                self.fields += z3c.form.field.Fields(InterfaceClass('IHistorizeReference{0}'.format(idx), attrs={
                    'IHistorizeReference{0}'.format(idx): schema.Text(title=u'Commentaire {0} '.format(change))}))

        super(HistorizeReferenceForm, self).update()

    @button.buttonAndHandler((u'Enregistrer'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()
        pass


class HistorizeReferenceView(FormWrapper):
    form = HistorizeReferenceForm
    index = ViewPageTemplateFile('templates/historizereferenceformview.pt')
