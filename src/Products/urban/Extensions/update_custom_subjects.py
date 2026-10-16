# -*- coding: utf-8 -*-

from plone import api


def update_custom_subjects():
    """
    Update `licenceSubject` on existing Housing licences with the default
    text configured on the Housing LicenceConfig.

    To be run manually after the `licenceSubject`
    default text has been configured for Housing licences.
    """
    urban_tool = api.portal.get_tool("portal_urban")
    catalog = api.portal.get_tool("portal_catalog")
    brains = catalog(portal_type="Housing")
    for brain in brains:
        obj = brain.getObject()
        default_subject = urban_tool.getTextDefaultValue("licenceSubject", obj)
        if default_subject:
            obj.setLicenceSubject(default_subject)
            obj.updateTitle()
            obj.reindexObject(idxs=("SearchableText",))
