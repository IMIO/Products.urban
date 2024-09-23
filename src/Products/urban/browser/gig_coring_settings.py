# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from z3c.form import button
from z3c.form import field

from Products.statusmessages.interfaces import IStatusMessage
from Products.urban import UrbanMessage as _

from zope.interface import Interface
from zope import schema


class IGigMapping(Interface):
    """ """

    user_id = schema.Choice(
        title=_(u"user_id"),
        required=False,
        vocabulary="urban.vocabularies.gig_coring_user_id",
    )

    mail_gig = schema.TextLine(
        title=_(u"mail_gig"),
        required=False,
    )


class IGigCoringLink(Interface):
    """ """

    gig_coring_activation = schema.Bool(
        title=_(u"gig_coring_activation"),
        default=False,
        required=False,
    )

    mail_mapping = schema.List(
        title=_("mail gig user id mapping"),
        description=_("map the plone user id to the gig mail address"),
        value_type=DictRow(title=_("mail mapping"), schema=IGigMapping, required=False),
        required=False,
    )


class GigCoringLinkEditForm(RegistryEditForm):
    """
    Define form logic
    """

    schema = IGigCoringLink
    label = _(u"gig coring link")
    description = _(u"""""")

    fields = field.Fields(IGigCoringLink)
    fields["mail_mapping"].widgetFactory = DataGridFieldFactory

    def updateWidgets(self):
        super(GigCoringLinkEditForm, self).updateWidgets()

    @button.buttonAndHandler(_("Save"), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"), "info")

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"), "info")
        self.request.response.redirect(
            "%s/%s" % (self.context.absolute_url(), self.control_panel_view)
        )


class GigCoringLinkControlPanel(ControlPanelFormWrapper):
    form = GigCoringLinkEditForm
