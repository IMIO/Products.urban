# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api
import re
from DateTime import DateTime
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectModifiedEvent
from .utils import formated_date

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
        
        if obj.getLastLicenceNotification() is not None:
            is_favorable = obj.getLastLicenceNotification().getDecision()=="favorable"
            
            # get date decision and date notification
            approbation_date = obj.getLastLicenceNotification().getEventDate()
            autorisation_date = obj.getLastLicenceNotification().decisionDate
            # forlmat dates
            if isinstance(approbation_date, DateTime):
                approbation_date = formated_date(approbation_date)
            if isinstance(autorisation_date, DateTime):
                autorisation_date = formated_date(autorisation_date)
        else:
            approbation_date = autorisation_date = None
    
        # to update 
        match = re.search(r' - ([^-]+)$', title)
        if match :
            subdivider_name = match.group(1)
        else: 
            subdivider_name = ""
        existing_object = api.content.find(
            context=parent_container,
            communalReference = reference
    
        )
        
        if existing_object:
            existing_object = existing_object[0].getObject()
            # If the object exists, update its fields
            existing_object.title = title
            existing_object.label = label
            existing_object.subdividerName = subdivider_name
            existing_object.communalReference = reference
            existing_object.DGO4Reference = reference_dgatlp
            existing_object.approvalDate = approbation_date
            existing_object.authorizationDate = autorisation_date
            
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
        
    
   


