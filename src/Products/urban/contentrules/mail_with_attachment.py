# -*- coding: utf-8 -*-

import base64
import logging
import traceback
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPException

from Acquisition import aq_inner
from collective.exportimport.interfaces import IBase64BlobsMarker
from plone import api
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.actions.mail import (IMailAction, MailAction,
                                                 MailActionExecutor,
                                                 MailAddForm, MailEditForm)
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.restapi.interfaces import ISerializeToJson
from plone.stringinterp.interfaces import IStringInterpolator
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.MailHost.MailHost import MailHostError
from Products.statusmessages.interfaces import IStatusMessage
from Products.urban.contentrules.interface import IGetDocumentToAttach
from zope.component import adapter, adapts, getMultiAdapter
from zope.component.interfaces import ComponentLookupError
from zope.formlib import form
from zope.globalrequest import getRequest
from zope.interface import Interface, alsoProvides, implementer, implements

logger = logging.getLogger("plone.contentrules")


class IMailWithAttachmentAction(IMailAction):
    """Definition of the configuration available for a mail action
    """


class MailWithAttachmentAction(MailAction):
    """
    The implementation of the action defined before
    """
    implements(IMailWithAttachmentAction, IRuleElementData)

    element = 'plone.actions.MailWithAttachement'


class MailWithAttachmentActionExecutor(MailActionExecutor):
    """The executor for this action.
    """
    adapts(Interface, IMailWithAttachmentAction, Interface)

    def __call__(self):
        mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not mailhost:
            raise ComponentLookupError, "You must have a Mailhost utility to \
execute this action"

        urltool = getToolByName(aq_inner(self.context), "portal_url")
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')

        obj = self.event.object

        interpolator = IStringInterpolator(obj)

        source = self.element.source
        if source:
            source = interpolator(source).strip()

        if not source:
            # no source provided, looking for the site wide from email
            # address
            from_address = portal.getProperty('email_from_address')
            if not from_address:
                # the mail can't be sent. Try to inform the user
                request = getRequest()
                if request:
                    messages = IStatusMessage(request)
                    msg = _(u"Error sending email from content rule. You must "
                            "provide a source address for mail "
                            "actions or enter an email in the portal properties")
                    messages.add(msg, type=u"error")
                return False

            from_name = portal.getProperty('email_from_name').strip('"')
            source = '"%s" <%s>' % (from_name, from_address)

        recip_string = interpolator(self.element.recipients)
        if recip_string: # check recipient is not None or empty string
            recipients = set([str(mail.strip()) for mail in recip_string.split(',') \
                              if mail.strip()])
        else:
            recipients = set()

        if self.element.exclude_actor:
            mtool = getToolByName(aq_inner(self.context), "portal_membership")
            actor_email = mtool.getAuthenticatedMember().getProperty('email', '')
            if actor_email in recipients:
                recipients.remove(actor_email)

        message = MIMEMultipart()
        # prepend interpolated message with \n to avoid interpretation
        # of first line as header
        body = "\n%s" % interpolator(self.element.message)
        body_part = MIMEText(body.encode("utf-8"))
        message.attach(body_part)

        message = self.attach_document(message)

        subject = interpolator(self.element.subject)

        for email_recipient in recipients:
            try:
                # XXX: We're using "immediate=True" because otherwise we won't
                # be able to catch SMTPException as the smtp connection is made
                # as part of the transaction apparatus.
                # AlecM thinks this wouldn't be a problem if mail queuing was
                # always on -- but it isn't. (stevem)
                # so we test if queue is not on to set immediate
                mailhost.send(message, email_recipient, source,
                              subject=subject, charset=email_charset,
                              immediate=not mailhost.smtp_queue)
            except (MailHostError, SMTPException):
                logger.error(
                    """mailing error: Attempt to send mail in content rule failed.\n%s""" %
                    traceback.format_exc())

        return True

    def attach_document(self, message):
        request = getattr(self.context, "REQUEST", None)
        if request is None:
            portal = api.portal.get()
            request = portal.REQUEST

        alsoProvides(request, IBase64BlobsMarker)
        obj = self.event.object
        docs = getMultiAdapter((obj, request, self.event), IGetDocumentToAttach)
        for doc in docs():
            serializer = getMultiAdapter((doc, request), ISerializeToJson)
            item = serializer(include_items=False)
            data = item["file"]["data"].encode()
            content = base64.b64decode(data)
            if item["@type"] in ["ATFile", "File"]:
                part = MIMEApplication(content, name=item["file"]["filename"])
                part.add_header("Content-Disposition", 'attachment; filename="{}"'.format(item["file"]["filename"]))
                message.attach(part)
            if item["@type"] in ["ATImage", "Image"]:
                message.attach(MIMEImage(content, name=item["file"]["filename"]))


        return message


@implementer(IGetDocumentToAttach)
@adapter(Interface, Interface, Interface)
class GetDocumentToAttach(object):
    def __init__(self, context, request, event):
        self.context = context
        self.request = request
        self.event = event

    def __call__(self):
        return self.context.listFolderContents(
            contentFilter={"portal_type" : ["ATFile","ATImage","File", "Image"]}
        )


class MailWithAttachmentAddForm(MailAddForm):
    """
    An add form for the mail action
    """
    form_fields = form.FormFields(IMailWithAttachmentAction)

    # custom template will allow us to add help text
    template = ViewPageTemplateFile('templates/mail.pt')

    def create(self, data):
        a = MailWithAttachmentAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class MailWithAttachmentEditForm(MailEditForm):
    """
    An edit form for the mail action
    """
    form_fields = form.FormFields(IMailWithAttachmentAction)
 
    # custom template will allow us to add help text
    template = ViewPageTemplateFile('templates/mail.pt')
