from plone import api


def reindex_object_by_uid(uid):
    cat = api.portal.get_tool('portal_catalog')
    brains = cat(UID=uid)
    obj = brains[0].getObject()
    obj.reindexObject()
