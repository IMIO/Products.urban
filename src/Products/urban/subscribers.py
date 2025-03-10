# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api
import re
from DateTime import DateTime
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectModifiedEvent
from .utils import convert_to_europe_brussels

def after_term_deactivate(obj, event):
    if (
        not event.transition
        or event.transition.id not in ["disable"]
        or obj != event.object
    ):
        return
    obj.setEndValidity(datetime(*datetime.now().date().timetuple()[0:3]))

def post_save_parceloutlicence(obj,event):
     
        #object_state = obj.get_state()
        parent_container = api.content.get(path='/Urban/urban/parcellings')
        title = getattr(obj,  'title', None)
        reference_dgatlp = getattr(obj,  'referenceDGATLP', None)
        reference = getattr(obj,  'reference', None)
        label = getattr(obj,  'licenceSubject', None)
        
        notification = obj.getLastLicenceNotification()
        
        if notification is not None:
            is_favorable = notification.getDecision().lower() == "favorable"
            
            approbation_date = notification.getEventDate()
            autorisation_date = notification.decisionDate
            
            # format dates
            if isinstance(approbation_date, DateTime):
                approbation_date = convert_to_europe_brussels(approbation_date)
                
            if isinstance(autorisation_date, DateTime):
                autorisation_date = convert_to_europe_brussels(autorisation_date)
        else:
            approbation_date = autorisation_date = None
    
        # to update 
        match = re.search(r' - ([^-]+)$', title)
        
        if match is not None:
            
            subdivider_name = match.group(1)
            
        else: 
            
            subdivider_name = ""
            
        found_parcelling = api.content.find(context=parent_container, communalReference=reference, portal_type="Parcelling")
        if found_parcelling and len(found_parcelling) > 0:
            found_parcelling = found_parcelling[0].getObject()
            
            #  Update fields
            found_parcelling.title = title
            found_parcelling.label = label
            found_parcelling.subdividerName = subdivider_name
            found_parcelling.communalReference = reference
            found_parcelling.DGO4Reference = reference_dgatlp
            found_parcelling.approvalDate = approbation_date
            found_parcelling.authorizationDate = autorisation_date
            
        else:
            # If the object doesn't exist, create a new one
            api.content.create(
                container=parent_container,
                type="Parcelling",  # Type of content to create
                title=title,
                label=label,
                subdividerName=subdivider_name,
                communalReference=reference,
                DGO4Reference=reference_dgatlp,
                approvalDate = approbation_date,
                authorizationDate = autorisation_date
            )
        
    
   


