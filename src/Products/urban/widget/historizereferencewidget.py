# -*- coding: utf-8 -*-

from Products.Archetypes.Registry import registerWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from archetypes.referencebrowserwidget.browser.view import ReferenceBrowserHelperView  # noqa
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from imio.history.utils import add_event_to_history
from plone.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form import interfaces
from z3c.form.field import Fields
from z3c.form.form import EditForm
from z3c.form.form import Form
from zope import schema
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implements
from zope.interface.interface import InterfaceClass

from Products.urban import UrbanMessage as _
from Products.urban.events.envclassEvents import get_value_history_by_index


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


class IHistorizeReference(Interface):
    field = schema.TextLine(
        title=u'field',
        required=True,
    )


class HistorizeReferenceForm(Form):
    implements(interfaces.IFieldsForm)
    fields = Fields(IHistorizeReference)
    ignoreContext = True
    # Avoid an issue with Products.PloneHotfix20160830
    allow_prefill_from_GET_request = True

    field_prefix = 'comment_'

    def update(self):
        historize_field = self.fieldname
        if historize_field is not None:
            last_history = get_value_history_by_index(
                self.context,
                '{0}_history'.format(historize_field),
                -2,
                action='update_{0}'.format(historize_field),
            )
            getter = 'get{0}{1}'.format(
                historize_field[0].upper(),
                historize_field[1:],
            )
            values = [e.id for e in getattr(self.context, getter)()]
            values.extend(last_history['{0}_history'.format(historize_field)])
            values = list(set(values))

            for idx, value in enumerate(values):
                key = 'IHistorizeReference{0}'.format(idx)
                field_title = self.get_title(historize_field, value)
                field = schema.Text(
                    title=self._formated_title(field_title),
                    required=False,
                )
                self.fields += Fields(
                    InterfaceClass(
                        key,
                        attrs={'{0}{1}'.format(self.field_prefix, value): field},
                    ),
                )

        super(HistorizeReferenceForm, self).update()

    def _formated_title(self, field_title):
        title = translate(_(u'Comment - {0}'), context=self.request)
        title = title.format(field_title)
        # Remove new lines
        return u''.join(title.splitlines())

    def updateWidgets(self, *args, **kwargs):
        super(HistorizeReferenceForm, self).updateWidgets(*args, **kwargs)
        self.widgets['field'].mode = interfaces.HIDDEN_MODE

    @property
    def fieldname(self):
        fieldname = self.request.form.get('form.widgets.field')
        if not fieldname:
            raise ValueError('missing field')
        return fieldname

    def get_title(self, fieldname, value):
        """Return the title of a reference"""
        view = ReferenceBrowserHelperView(self.context, self.request)
        field = self.context.getField(fieldname)
        values = [e for e in view.getFieldRelations(field) if e.id == value]
        if not values:
            return value
        return values[0].title and values[0].title or value

    @button.buttonAndHandler((u'Enregistrer'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = EditForm.formErrorsMessage
            return
        data = {k: v for k, v in data.items()
                if k.startswith(self.field_prefix) and v}
        if data:
            add_event_to_history(
                self.context,
                '{0}_history'.format(self.fieldname),
                '{0}_history'.format(self.fieldname),
                extra_infos=data,
            )
        self.status = _('History saved')


class HistorizeReferenceView(FormWrapper):
    form = HistorizeReferenceForm
    index = ViewPageTemplateFile('templates/historizereferenceformview.pt')
