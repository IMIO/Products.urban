# -*- coding: utf-8 -*-
from zope.interface import alsoProvides
from Products.urban.interfaces import IRequestedOrganisation

def setInterfaceAndCreateEvent(term, event):
    if not term.getPortalTypeName() == 'RequestedOrganisation':
        return
    alsoProvides(term, IRequestedOrganisation)
    print("snitches and talkers get stitches and walkers")   
