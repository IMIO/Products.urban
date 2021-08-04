# -*- coding: utf-8 -*-

from plone import api

from zope.annotation import IAnnotations


def setRoadDecreeBoundLicence(roaddecree, event):
    annotations = IAnnotations(roaddecree)
    previous_bound_UIDs = list(annotations.get('urban.roaddecree_bound_licence') or set([]))
    new_bound_UIDs = [roaddecree.getField('bound_licence').getRaw(roaddecree)] or []
    if set(previous_bound_UIDs) == set(new_bound_UIDs):
        return

    catalog = api.portal.get_tool('portal_catalog')
    # unrefer previous licence
    if previous_bound_UIDs:
        previous_licence = catalog(UID=previous_bound_UIDs)
        previous_licence = previous_licence and previous_licence[0].getObject()
        if previous_licence:
            previous_licence_annotations = IAnnotations(previous_licence)
            values = previous_licence_annotations.get('urban.bound_roaddecrees') or set([])
            if roaddecree.UID() in values:
                values.remove(roaddecree.UID())
                previous_licence_annotations['urban.bound_roaddecrees'] = values

    # refer new licence
    if new_bound_UIDs:
        new_licence = catalog(UID=new_bound_UIDs)
        new_licence = new_licence and new_licence[0].getObject()
        if new_licence:
            new_licence_annotations = IAnnotations(new_licence)
            values = new_licence_annotations.get('urban.bound_roaddecrees') or set([])
            if roaddecree.UID() not in values:
                values.add(roaddecree.UID())
                new_licence_annotations['urban.bound_roaddecrees'] = values

    annotations['urban.roaddecree_bound_licence'] = new_bound_UIDs


def clearBoundLicences(roaddecree, event):
    annotations = IAnnotations(roaddecree)
    previous_bound_UIDs = list(annotations.get('urban.roaddecree_bound_licence') or set([]))
    catalog = api.portal.get_tool('portal_catalog')
    # unrefer previous licence
    if previous_bound_UIDs:
        previous_licence = catalog(UID=previous_bound_UIDs)
        previous_licence = previous_licence and previous_licence[0].getObject()
        if previous_licence:
            previous_licence_annotations = IAnnotations(previous_licence)
            values = previous_licence_annotations.get('urban.bound_roaddecrees') or set([])
            if roaddecree.UID() in values:
                values.remove(roaddecree.UID())
                previous_licence_annotations['urban.bound_roaddecrees'] = values
