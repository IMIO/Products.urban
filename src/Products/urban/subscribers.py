# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api
import re
from DateTime import DateTime
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from .utils import convert_to_europe_brussels
from .interfaces import ICODT_ParcelOutLicence


def after_term_deactivate(obj, event):
    if (
        not event.transition
        or event.transition.id not in ["disable"]
        or obj != event.object
    ):
        return
    obj.setEndValidity(datetime(*datetime.now().date().timetuple()[0:3]))


def post_save_event_parceloutlicence(obj, event):    
    if not IObjectModifiedEvent.providedBy(event):
        return  
  
    if not ICODT_ParcelOutLicence.providedBy(obj.aq_parent):
        return
    urbaneventtypes = obj.getUrbaneventtypes()
    is_event_type_valid = (
        urbaneventtypes is not None and urbaneventtypes.id == "delivrance-du-permis-octroi-ou-refus-codt"
    )
    
    if not is_event_type_valid:
        return
    site_root = api.portal.get() 
    site_root_path = "/".join(site_root.getPhysicalPath())  
    parent_container = api.content.get(path=site_root_path+"/urban/parcellings")
    
    title = getattr(obj.aq_parent, "title", None)
    reference_dgatlp = getattr(obj.aq_parent, "referenceDGATLP", None)
    reference = getattr(obj.aq_parent, "reference", None)
    label = getattr(obj.aq_parent, "licenceSubject", None)
    match = re.search(r" - ([^-]+)$", title)
    if match is not None:
        subdivider_name = match.group(1)
    else:
        subdivider_name = ""

    is_favorable = obj.getDecision() == "favorable"

    if not is_favorable:
        return
    else:
        approbation_date = obj.getEventDate()
        authorization_date = obj.decisionDate

        # format dates
        if isinstance(approbation_date, DateTime):
            approbation_date = convert_to_europe_brussels(approbation_date)

        if isinstance(authorization_date, DateTime):
            authorization_date = convert_to_europe_brussels(authorization_date)
        found_parcelling = None
        for obj in parent_container.objectValues():
            if obj.portal_type == "Parcelling" and getattr(obj, "communalReference", None) == reference:
                found_parcelling = obj
                break
        
        if found_parcelling :
            # Update fields
            found_parcelling.title = title
            found_parcelling.label = label
            found_parcelling.subdividerName = subdivider_name
            found_parcelling.communalReference = reference
            found_parcelling.DGO4Reference = reference_dgatlp
            found_parcelling.approvalDate = approbation_date
            found_parcelling.authorizationDate = authorization_date

        else:
            api.content.create(
                container=parent_container,
                type="Parcelling",  # Type of content to create
                title=title,
                label=label,
                subdividerName=subdivider_name,
                communalReference=reference,
                DGO4Reference=reference_dgatlp,
                approvalDate=approbation_date,
                authorizationDate=authorization_date,
            )
