# -*- coding: utf-8 -*-
#
# File: Contact.py
#
# Copyright (c) 2010 by CommunesPlone
# Generator: ArchGenXML Version 2.4.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>,
Stephan GEULETTE <stephan.geulette@uvcw.be>,
Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from plone.indexer import indexer
from Products.Archetypes.interfaces import IBaseObject


class UrbanIndexes:
    """
      This class manage indexes methods for urban objects
    """
    security = ClassSecurityInfo()

    security.declarePublic('applicantInfosIndex')

    def applicantInfosIndex(self):
        """
          Return the informations to index about the applicants
        """
        res = []
        for applicant in self.getApplicants():
            res.append(applicant.getName1())
            res.append(applicant.getName2())
            res.append(applicant.getNationalRegister())
        return res

    security.declarePublic('parcelInfosIndex')

    def parcelInfosIndex(self):
        """
          Indexes some informations about the parcels of 'self'
          It builds a list of parcels infos.  Parcels infos are :
          - code divison
          - division
          - section
          - radical
          - bis
          - exposant
          - puissance
          Separated by a ','
          What we need to do is to do an 'exact' search on it
          This index is a ZCTextIndex based on the plone_lexicon so we
          are sure that indexed values are lowercase
        """
        parcelsInfos = []
        try:
            for parcel in self.getParcels():
                res = []
                res.append(parcel.getDivisionCode())
                res.append(parcel.getSection())
                res.append(parcel.getRadical())
                res.append(parcel.getBis())
                res.append(parcel.getExposant())
                res.append(parcel.getPuissance())
                if parcel.getPartie():
                    res.append('1')
                else:
                    res.append('0')
                parcelInfos = ",".join(res)
                parcelsInfos.append(parcelInfos)
        except:
            pass
        return parcelsInfos


@indexer(IBaseObject)
def baseobject_title(object):
    title = object.Title()
    if isinstance(title, unicode):
        title = title.encode('utf8')
    return title
