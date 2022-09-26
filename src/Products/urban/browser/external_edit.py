# -*- coding: utf-8 -*-

from collective.externaleditor.browser.views import ExternalEditView

from plone import api
from Products.statusmessages.interfaces import IStatusMessage
from Products.urban import UrbanMessage as _


class TemplatesExternalEditView(ExternalEditView):
    """
    """
    def __call__(self):
        """
        """
        try:
            enabled = api.portal.get_registry_record(
                'Products.urban.interfaces.ITemplatesExternalEdition.enabled'
            )
        except:
            enabled = True

        if not enabled:
            status = _(u"DISABLED")
            redirecturl = self.context.absolute_url()+'/view'
            self.request.response.redirect(redirecturl)
            IStatusMessage(self.request).addStatusMessage(status, type='error')
        else:
            return super(TemplatesExternalEditView, self).__call__()
