from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.i18n import translate


class LongTextView(BrowserView):
    """
    This manage the view of long text
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.field = self.request.get("field", "")
        if not self.field:
            plone_utils = getToolByName(context, "plone_utils")
            plone_utils.addPortalMessage(_("Nothing to show !!!"), type="error")

    def getFieldText(self):
        """
        Returns the entire text
        """
        context = aq_inner(self.context)
        if hasattr(context, self.field):
            return getattr(
                context, "get" + self.field[0].capitalize() + self.field[1:]
            )()
        else:
            plone_utils = getToolByName(context, "plone_utils")
            plone_utils.addPortalMessage(
                _("The field does not exist !!!"),
                mapping={"field": self.field},
                type="error",
            )


class PmSummaryTextView(BrowserView):
    """ """

    def getPmFields(self):
        """
        Return all the activated fields of this UrbanEvent
        """
        context = aq_inner(self.context)
        linkedUrbanEventType = context.getUrbaneventtypes()
        fields = []
        for activatedField in linkedUrbanEventType.getActivatedFields():
            if not activatedField:
                continue  # in some case, there could be an empty value in activatedFields...
            field = context.getField(activatedField)
            if hasattr(field, "pm_text_field"):
                fields.append(field)
        return fields

    def getFieldText(self):
        """ """
        fields = self.getPmFields()
        summary_text = []
        summary = []

        for field in fields:
            text = field.get(self.context)
            summary_text.append(text)
            widget = field.widget
            field_name = translate(
                widget.label,
                context=self.request,
            )
            summary.append("<strong>{}:</strong>".format(field_name.encode("utf-8")))
            summary.append(text)

        if not any(summary_text):
            return ""

        summary = "<br /><br />".join(summary)

        return summary


class NoticeFormDataTextView(BrowserView):
    def __init__(self, context, request):
        super(NoticeFormDataTextView, self).__init__(context, request)
        self.action_code = self.request.get("action_code", "")
        if not self.action_code:
            plone_utils = getToolByName(self.context, "plone_utils")
            plone_utils.addPortalMessage(_("Nothing to show !!!"), type="error")

    def getFieldText(self):
        """
        Returns an HTML structure of the form data sent with a particular action code.
        This data comes from a dict stored as annotation on the event.
        """

        annotations = IAnnotations(self.context)
        transmits = annotations.get("notice_transmit_dates", {})
        action_data = transmits.get(self.action_code, {})
        field_values = action_data.get("field_values", {})

        if not field_values:
            return _("Nothing to show !!!")

        html_blocks = []
        for field_id, field_value in field_values.items():
            field_title = translate(
                field_id,
                context=self.request,
            )
            html_blocks.append(u"<h2>{}</h2>".format(field_title))
            if field_id in ("college_opinion", "college_decision"):
                html_blocks.append(u"<div>{}</div>".format(field_value))
            elif field_id == "documents":
                points = [
                    u"<li>{}</li>".format(document["title"]) for document in field_value
                ]
                html_blocks.append(u"<ul>{}</ul>".format("\n".join(points)))
                if not field_value:
                    html_blocks.append(u"<div>{}</div>".format(_("content_none")))

        return u"<br />\n".join(html_blocks)
