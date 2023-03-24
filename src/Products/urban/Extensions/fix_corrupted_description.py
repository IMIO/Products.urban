# -*- coding: utf-8 -*-

from plone import api
import transaction

def fix_corrupted_description():
    """
    To be used in case of error "maximum recursion depth exceeded"
    the probleme come from a "corrupted" description on the object cause by a browser extension (fenetremailto) at edit time
    """
    portal = api.portal.get()
    request = portal.REQUEST
    context = request['PARENTS'][0]
    if not getattr(context, "description", False):
        return

    context.description.raw = ""
    context.description.original_encoding = "ascii"
    transaction.commit()


def show_description():
    """
    """
    portal = api.portal.get()
    request = portal.REQUEST
    context = request['PARENTS'][0]
    return context.description.raw
