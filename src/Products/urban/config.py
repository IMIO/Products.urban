# -*- coding: utf-8 -*-
#
# File: urban.py
#
# Copyright (c) 2011 by CommunesPlone
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
##code-section config-head #fill in your manual code here
##/code-section config-head


PROJECTNAME = "urban"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))
ADD_CONTENT_PERMISSIONS = {
    'GenericLicence': 'urban: Add GenericLicence',
    'Contact': 'urban: Add Contact',
    'Street': 'urban: Add Street',
    'UrbanEvent': 'urban: Add UrbanEvent',
    'UrbanEventType': 'urban: Add UrbanEventType',
    'Recipient': 'urban: Add Recipient',
    'BuildLicence': 'urban: Add BuildLicence',
    'ParcelOutLicence': 'urban: Add ParcelOutLicence',
    'Geometrician': 'urban: Add Geometrician',
    'FolderManager': 'urban: Add FolderManager',
    'UrbanVocabularyTerm': 'urban: Add UrbanVocabularyTerm',
    'PortionOut': 'urban: Add PortionOut',
    'RecipientCadastre': 'urban: Add RecipientCadastre',
    'Layer': 'urban: Add Layer',
    'Declaration': 'urban: Add Declaration',
    'ParcellingTerm': 'urban: Add ParcellingTerm',
    'PcaTerm': 'urban: Add PcaTerm',
    'City': 'urban: Add City',
    'UrbanCertificateBase': 'urban: Add UrbanCertificateBase',
    'UrbanCertificateTwo': 'urban: Add UrbanCertificateTwo',
    'EnvironmentalDeclaration': 'urban: Add EnvironmentalDeclaration',
    'Equipment': 'urban: Add Equipment',
    'Lot': 'urban: Add Lot',
    'Division': 'urban: Add Division',
    'WorkLocation': 'urban: Add WorkLocation',
    'UrbanDelay': 'urban: Add UrbanDelay',
    'Locality': 'urban: Add Locality',
    'LicenceConfig': 'urban: Add LicenceConfig',
    'PersonTitleTerm': 'urban: Add PersonTitleTerm',
    'Inquiry': 'urban: Add Inquiry',
    'UrbanEventInquiry': 'urban: Add UrbanEventInquiry',
}

setDefaultRoles('urban: Add GenericLicence',  ('Manager', ))
setDefaultRoles('urban: Add Contact',  ('Manager', ))
setDefaultRoles('urban: Add Street',  ('Manager', ))
setDefaultRoles('urban: Add UrbanEvent',  ('Manager', ))
setDefaultRoles('urban: Add UrbanEventType',  ('Manager', ))
setDefaultRoles('urban: Add Recipient',  ('Manager', ))
setDefaultRoles('urban: Add BuildLicence',  ('Manager', ))
setDefaultRoles('urban: Add ParcelOutLicence',  ('Manager', ))
setDefaultRoles('urban: Add Geometrician',  ('Manager', ))
setDefaultRoles('urban: Add FolderManager',  ('Manager', ))
setDefaultRoles('urban: Add UrbanVocabularyTerm',  ('Manager', ))
setDefaultRoles('urban: Add PortionOut',  ('Manager', ))
setDefaultRoles('urban: Add RecipientCadastre',  ('Manager', ))
setDefaultRoles('urban: Add Layer',  ('Manager', ))
setDefaultRoles('urban: Add Declaration',  ('Manager', ))
setDefaultRoles('urban: Add ParcellingTerm',  ('Manager', ))
setDefaultRoles('urban: Add PcaTerm',  ('Manager', ))
setDefaultRoles('urban: Add City',  ('Manager', ))
setDefaultRoles('urban: Add UrbanCertificateBase',  ('Manager', ))
setDefaultRoles('urban: Add UrbanCertificateTwo',  ('Manager', ))
setDefaultRoles('urban: Add EnvironmentalDeclaration',  ('Manager', ))
setDefaultRoles('urban: Add Equipment',  ('Manager', ))
setDefaultRoles('urban: Add Lot',  ('Manager', ))
setDefaultRoles('urban: Add Division',  ('Manager', ))
setDefaultRoles('urban: Add WorkLocation',  ('Manager', ))
setDefaultRoles('urban: Add UrbanDelay',  ('Manager', ))
setDefaultRoles('urban: Add Locality',  ('Manager', ))
setDefaultRoles('urban: Add LicenceConfig',  ('Manager', ))
setDefaultRoles('urban: Add PersonTitleTerm',  ('Manager', ))
setDefaultRoles('urban: Add Inquiry',  ('Manager', ))
setDefaultRoles('urban: Add UrbanEventInquiry',  ('Manager', ))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
STYLESHEETS = []
JAVASCRIPTS = []

#Add an empty value in vocabulary display proposing to choose a value and returning an error if not changed
ADD_EMPTY_VOCAB_VALUE = True
#topics
TOPIC_TYPE = "urban_topic_type"
#dependencies
DEPENDENCIES = ["ReferenceDataGridField",]
#name of the folder created in a licence that will contain additional
#layers linked to the licence and used in the mapfile generation
ADDITIONAL_LAYERS_FOLDER="additional_layers"

#a list where first element is the meetingConfigId and the second, the meta_type name
URBAN_TYPES = ['BuildLicence','ParcelOutLicence','Declaration', 'Division', 'UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter', 'EnvironmentalDeclaration', ]
#empty value used for listboxes
EMPTY_VOCAB_VALUE = 'choose_a_value'

HAS_PLONETASK = False
try:
    from Products.PloneTask.Task import Task
    HAS_PLONETASK = True
except ImportError:
    HAS_PLONETASK = False

PPNC_LAYERS = {
    'ppnc1' : {'xmin':40824, 'ymin':113446, 'xmax':139390, 'ymax':168195},
    'ppnc2' : {'xmin':122374, 'ymin':116510, 'xmax':218186, 'ymax':169730},
    'ppnc3' : {'xmin':202155, 'ymin':115165, 'xmax':302832, 'ymax':171088},
    'ppnc4' : {'xmin':95175, 'ymin':64858, 'xmax':196930, 'ymax':121379},
    'ppnc5' : {'xmin':191082, 'ymin':62858, 'xmax':300067, 'ymax':123394},
    'ppnc6' : {'xmin':176533, 'ymin':18317, 'xmax':270345, 'ymax':70426},
        }
#From Qgis
#PPNC : 27303,15803 : 311226,173511
#ppnc1: 40824,113446 : 139390,168195
#ppnc2: 122374,116510 : 218186,169730
#ppnc3: 202155,115165 : 302832,171088
#ppnc4: 95175,64858 : 196930,121379
#ppnc5: 191082,62858 : 300067,123394
#ppnc6: 176533,18317 : 270345,70426

##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from Products.urban.AppConfig import *
except ImportError:
    pass
