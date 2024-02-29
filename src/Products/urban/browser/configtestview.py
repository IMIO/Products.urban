# encoding: utf-8
from Products.Five import BrowserView
from Acquisition import aq_parent
from Acquisition import aq_inner
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.i18n import translate
from DateTime import DateTime
from Products.urban.browser.licence.licenceview import LicenceView


class ConfigTestView(BrowserView):
    def __init__(self, context, request):
        super(ConfigTestView, self).__init__(context, request)
        self.context = context
        self.request = request

    def get_events(self):
        licence = aq_parent(self.context)
        tool = api.portal.get_tool("portal_types")
        portal_type = tool[licence.licencePortalType]
        config_id = portal_type.id.lower()
        portal_urban = api.portal.get_tool("portal_urban")
        eventtypes = portal_urban.listEventTypes(licence, urbanConfigId=config_id)
        events_objects = [event.getObject() for event in eventtypes]
        return events_objects

    def get_generated_tests(self):
        licence = aq_parent(self.context)
        tool = api.portal.get_tool("portal_types")
        portal_type = tool[licence.licencePortalType]
        values = api.content.find(
            context=self.context,
            depth=1,
            portal_type=portal_type.id,
            sort_on="getObjPositionInParent",
        )
        lasts_generated = [item.id for item in reversed(values)]
        return lasts_generated


class ConfigTestProcessingView(BrowserView):
    def __init__(self, context, request):
        super(ConfigTestProcessingView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.events_checked = self.request.get("events_checked")

    def processing(self):
        licence_config = aq_parent(self.context)
        tool = api.portal.get_tool("portal_types")
        portal_type = tool[licence_config.licencePortalType]
        context = api.content.create(
            container=self.context,
            type=portal_type.id,
            title="footitle",
            reference="test",
        )
        mGenerateObject = GenerateObject(context=context, request=self.request)
        mGenerateObject.config_content()

        applicant = api.content.create(
            container=context, type="Applicant", title="ApplicantTitle"
        )

        # event manage
        mLicenceView = LicenceView(context, self.request)
        events = mLicenceView.getUrbanEventTypes()
        for event in events:
            if event.id in self.events_checked:
                event = event.getObject()
                event = mGenerateObject.context.createUrbanEvent(event)
                mGeneratEvent = GenerateObject(context=event, request=self.request)
                mGeneratEvent.config_event()

        mGenerateObjectApplicant = GenerateObject(
            context=applicant, request=self.request
        )
        mGenerateObjectApplicant.config_applicant()


class GenerateMixin(object):
    IGNORED_FIELD = [
        "id",
        "creation_date",
        "expirationDate",
        "effectiveDate",
        "modification_date",
        "allowDiscussion",
        "language",
        "reference",
    ]

    def __init__(self, context, request):
        self.schema = context.schema
        self.fields = context.schema._fields
        self.names = context.schema._names
        self.context = context
        self.request = request
        self.values = {}


class GenerateObject(GenerateMixin):
    def __init__(self, context, request):
        super(GenerateObject, self).__init__(context, request)

    def config_content(self):
        # TODO achieve Parcel and demandeur in content type
        for name in self.names:
            if name not in self.IGNORED_FIELD:
                me = getattr(self, "_{0}".format(name), process)
                me(
                    name=name,
                    fields=self.fields,
                    context=self.context,
                    request=self.request,
                )

    def config_event(self):
        # TODO error with interface, need to check
        self.IGNORED_FIELD.append("title")
        for name in self.names:
            if name not in self.IGNORED_FIELD:
                process(
                    name=name,
                    fields=self.fields,
                    context=self.context,
                    request=self.request,
                )

    def config_applicant(self):
        for name in self.names:
            if name not in self.IGNORED_FIELD:
                me = getattr(self, "_{0}".format(name), process)
                me(
                    name=name,
                    fields=self.fields,
                    context=self.context,
                    request=self.request,
                )

    # Custom method for process reference

    def _architects(self, name, fields, context, request=None):
        value = api.content.find(portal_type="Architect")[0].getObject()
        self.custum_setter(name, value, fields, context)

    def _foldermanagers(self, name, fields, context, request=None):
        value = api.content.find(portal_type="FolderManager")[0].getObject()
        self.custum_setter(name, value, fields, context)

    def _workLocations(self, name, fields, context, request=None):
        locality = api.content.find(portal_type="Locality")[0].getObject()
        value = {"number": "0", "street": locality.UID()}
        self.custum_setter(name, value, fields, context)

    def _roadEquipments(self, name, fields, context, request=None):
        value = {"road_equipment": "eau", "road_equipment_details": "eau"}
        self.custum_setter(name, value, fields, context)

    def _personTitle(self, name, fields, context, request=None):
        value = "master"
        setter = getattr(context, fields[name].mutator)
        setter(value)

    def custum_setter(self, name, value, fields, context):
        setter = getattr(context, fields[name].mutator)
        setter([value])


def process(name, fields, context, request):
    """
    filter field and set a value
    @return:
    """
    FIELDS_TYPE = {
        "boolean": True,
        "integer": 1,
        "double": 1.00,
        "datetime": DateTime(),
    }
    value = None
    # process vocabulary
    field = fields[name]
    if field.type in FIELDS_TYPE:
        value = FIELDS_TYPE[field.type]
    else:
        if field.vocabulary_factory:
            value = process_vocabulary_factory(field=field, context=context)
        elif field.vocabulary:
            value = process_vocabulary(field=field, context=context)
        elif (
            field.type == "text" or field.type == "string" or field.type == "lines"
        ) and not (field.vocabulary_factory or field.vocabulary):
            msgid = getattr(field.widget, "label_msgid", field.widget.label)
            domain = getattr(field.widget, "domain", "urban")
            value = translate(msgid, domain, context=request)
    setter = getattr(context, field.mutator)
    if value:
        setter(value)


def process_vocabulary(field, context):
    """
    Return value for vocabulary
    @param field: field from schema
    @param context: can be content type or event
    @return:
    """
    vocabulary = field.vocabulary
    if type(vocabulary) is str:
        return [get_custom_vocabulary(vocabulary, context)]
    else:
        if len(vocabulary.listAllVocTerms(context)) > 0:
            return tuple([vocabulary.listAllVocTerms(context)[0].id])
        else:
            return None


def process_vocabulary_factory(field, context):
    """
    Return value for vocabulary
    @param field: field from schema
    @param context: can be content type or event
    @return:
    """
    vocabulary_factory = field.vocabulary_factory
    factory = getUtility(IVocabularyFactory, vocabulary_factory)
    voc = factory(context)
    if len(voc._terms) > 0:
        return [voc._terms[0].value]
    else:
        return []


def get_custom_vocabulary(vocabulary_name, context):
    """

    @param vocabulary_name: name of vocabulary
    @param context:
    @return: value custom
    """
    if len(getattr(context, vocabulary_name)().keys()) > 0:
        value = getattr(context, vocabulary_name)().keys()[-1]
        if value is not None:
            return value
        else:
            # raise error if not key in vocabualary
            raise ValueError("Any key in custom vocabulary find!")
    else:
        return []
