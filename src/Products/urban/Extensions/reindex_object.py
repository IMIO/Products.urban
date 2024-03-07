from plone import api

from Products.urban.interfaces import IOpinionRequestEventType


def reindex_object_by_uid(uid):
    cat = api.portal.get_tool("portal_catalog")
    brains = cat(UID=uid)
    obj = brains[0].getObject()
    obj.reindexObject()


def disable_opinion_field():
    cat = api.portal.get_tool("portal_catalog")
    event_types_brains = cat(object_provides=IOpinionRequestEventType.__identifier__)
    for brain in event_types_brains:
        event_type = brain.getObject()
        active_fields = event_type.getActivatedFields()
        if "adviceAgreementLevel" in active_fields:
            index = active_fields.index("adviceAgreementLevel")
            new_active_fields = active_fields[:index] + active_fields[index + 1 :]
            event_type.activatedFields = new_active_fields
