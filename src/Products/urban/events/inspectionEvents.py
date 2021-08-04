# -*- coding: utf-8 -*-

from plone import api

from zope.annotation import IAnnotations


def setInspectionBoundLicence(inspection, event):
    annotations = IAnnotations(inspection)
    previous_bound_UIDs = list(annotations.get('urban.inspection_bound_licence') or set([]))
    new_bound_UIDs = inspection.getField('bound_licences').getRaw(inspection) or []
    if set(previous_bound_UIDs) == set(new_bound_UIDs):
        return

    catalog = api.portal.get_tool('portal_catalog')
    # unrefer previous licence
    if previous_bound_UIDs:
        previous_licence = catalog(UID=previous_bound_UIDs)
        previous_licence = previous_licence and previous_licence[0].getObject()
        if previous_licence:
            previous_licence_annotations = IAnnotations(previous_licence)
            values = previous_licence_annotations.get('urban.bound_inspections') or set([])
            if inspection.UID() in values:
                values.remove(inspection.UID())
                previous_licence_annotations['urban.bound_inspections'] = values

    # refer new licence
    if new_bound_UIDs:
        new_licence = catalog(UID=new_bound_UIDs)
        new_licence = new_licence and new_licence[0].getObject()
        if new_licence:
            new_licence_annotations = IAnnotations(new_licence)
            values = new_licence_annotations.get('urban.bound_inspections') or set([])
            if inspection.UID() not in values:
                values.add(inspection.UID())
                new_licence_annotations['urban.bound_inspections'] = values

    annotations['urban.inspection_bound_licence'] = new_bound_UIDs


def clearBoundLicences(inspection, event):
    annotations = IAnnotations(inspection)
    previous_bound_UIDs = list(annotations.get('urban.inspection_bound_licence') or set([]))
    catalog = api.portal.get_tool('portal_catalog')
    # unrefer previous licence
    if previous_bound_UIDs:
        previous_licence = catalog(UID=previous_bound_UIDs)
        previous_licence = previous_licence and previous_licence[0].getObject()
        if previous_licence:
            previous_licence_annotations = IAnnotations(previous_licence)
            values = previous_licence_annotations.get('urban.bound_inspections') or set([])
            if inspection.UID() in values:
                values.remove(inspection.UID())
                previous_licence_annotations['urban.bound_inspections'] = values
