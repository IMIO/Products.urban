# -*- coding: utf-8 -*-
from collective.fingerpointing.config import AUDIT_MESSAGE
from collective.fingerpointing.interfaces import IFingerPointingSettings
from collective.fingerpointing.logger import log_info
from collective.fingerpointing.utils import get_request_information
from plone import api


def log_map_access(context, request):
    """Log urban map access"""
    name = IFingerPointingSettings.__identifier__ + '.audit_urbanmap'
    audit_profile_imports = api.portal.get_registry_record(name, default=False)
    if not audit_profile_imports:
        return

    try:
        user, ip = get_request_information()
    except AttributeError:
        user, ip = '-', '-'

    action = request.physicalPathFromURL(request.URL)[-1]
    extras = 'context={}'.format(request.physicalPathFromURL(request.URL)[-2])
    log_info(AUDIT_MESSAGE.format(user, ip, action, extras))
