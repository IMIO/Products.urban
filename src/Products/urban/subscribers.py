# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api
from Products.CMFCore.utils import getToolByName
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
    parent_object = obj.aq_parent
    if not ICODT_ParcelOutLicence.providedBy(parent_object):
        return
    
    is_event_eligible = (obj.getUrbaneventtypes().id == "delivrance-du-permis-octroi-ou-refus-codt" and obj.getDecision() == "favorable")
    
    if not is_event_eligible:
        return

    site_root = api.portal.get() 
    parcellings_folder = site_root['urban']['parcellings']
    
    title = getattr(parent_object, "title", None)
    reference_dgatlp = getattr(parent_object, "referenceDGATLP", None)
    reference = getattr(parent_object, "reference", None)
    label = getattr(parent_object, "licenceSubject", None)
    match = re.search(r" - ([^-]+)$", title)
   
    if match is not None:
        subdivider_name = match.group(1)
    else:
        subdivider_name = ""
        
    approbation_date = obj.getEventDate()
    authorization_date = obj.decisionDate

    # format dates
    if isinstance(approbation_date, DateTime):
        approbation_date = convert_to_europe_brussels(approbation_date)

    if isinstance(authorization_date, DateTime):
        authorization_date = convert_to_europe_brussels(authorization_date)
        
    #found_parcelling = None
    found_parcelling = next((
        obj for obj in parcellings_folder.objectValues() 
        if obj.portal_type == "Parcelling" and getattr(obj, "communalReference", None) == reference
    ), None)
    """for obj in parcellings_folder.objectValues():
        if obj.portal_type == "Parcelling" and getattr(obj, "communalReference", None) == reference:
            found_parcelling = obj
            break"""
    
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
            container=parcellings_folder,
            type="Parcelling",  # Type of content to create
            title=title,
            label=label,
            subdividerName=subdivider_name,
            communalReference=reference,
            DGO4Reference=reference_dgatlp,
            approvalDate=approbation_date,
            authorizationDate=authorization_date,
        )
