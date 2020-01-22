# -*- coding: utf-8 -*-

from plone import api

from zope.annotation import IAnnotations


def setInspectionBoundLicence(licence, event):
    annotations = IAnnotations(licence)
    previous_bound_UID = list(annotations.get('urban.inspection_bound_licence') or set([]))
    new_bound_UID = licence.getField('bound_licence').getRaw(licence)
    if set(previous_bound_UID) == set(new_bound_UID):
        return

    catalog = api.portal.get_tool('portal_catalog')
    # unrefer previous licence
    if previous_bound_UID:
        previous_licence = catalog(UID=previous_bound_UID)
        previous_licence = previous_licence and previous_licence[0].getObject()
        if previous_licence:
            previous_licence_annotations = IAnnotations(previous_licence)
            values = previous_licence_annotations.get('urban.bound_inspections') or set([])
            if licence.UID() in values:
                values.remove(licence.UID())
                previous_licence_annotations['urban.bound_inspections'] = values

    # refer new licence
    if new_bound_UID:
        new_licence = catalog(UID=new_bound_UID)
        new_licence = new_licence and new_licence[0].getObject()
        if new_licence:
            new_licence_annotations = IAnnotations(new_licence)
            values = new_licence_annotations.get('urban.bound_inspections') or set([])
            if licence.UID() not in values:
                values.add(licence.UID())
                new_licence_annotations['urban.bound_inspections'] = values

    annotations['urban.inspection_bound_licence'] = new_bound_UID
