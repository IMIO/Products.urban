# -*- coding: utf-8 -*-

from plone import api


def fix_profile_version(version=None):
    portal_setup = api.portal.get_tool("portal_setup")
    if version is None:
        version = "1122"
    profile_id = "Products.urban:default"
    portal_setup.setLastVersionForProfile(profile_id, version)
    return "Profile '{0}' is now version '{1}'".format(profile_id, version)
