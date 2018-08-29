# -*- coding: utf-8 -*-
#
# File: CODT_IntegratedLicence.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban import UrbanMessage as _
from Products.urban.content.licence.CODT_UniqueLicence import CODT_UniqueLicence
from Products.urban.content.licence.CODT_UniqueLicence import finalizeSchema as firstBaseFinalizeSchema
from Products.urban.utils import setSchemataForCODT_UniqueLicenceInquiry
from Products.urban.widget.historizereferencewidget import HistorizeReferenceBrowserWidget
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.urban.widget.urbanreferencewidget import UrbanReferenceWidget
from Products.urban import UrbanMessage as _


from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    LinesField(
        name='regional_authority',
        widget=MultiSelectionWidget(
            format='checkbox',
            label=_('urban_label_regional_authority', default='Regional_authority'),
        ),
        schemata='urban_description',
        vocabulary='listRegionalAuthorities',
        default=['dgo6'],
    ),
    StringField(
            name='road_decree_reference',
            widget=UrbanReferenceWidget(
                    label=_('road_decree_reference', default='road_decree_reference'),
                    portal_types=['RoadDecree'],
            ),
            required=False,
            schemata='urban_description',
            default_method='getDefaultText',
            validators=('isRoadDecreeReference',),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CODT_IntegratedLicence_schema = BaseFolderSchema.copy() + \
    getattr(CODT_UniqueLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
setSchemataForCODT_UniqueLicenceInquiry(CODT_IntegratedLicence_schema)
##/code-section after-schema


class CODT_IntegratedLicence(BaseFolder, CODT_UniqueLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICODT_IntegratedLicence)

    meta_type = 'CODT_IntegratedLicence'
    _at_rename_after_creation = True

    schema = CODT_IntegratedLicence_schema

    # Methods

    def listProcedureChoices(self):
        vocab = (
            ('ukn', 'Non determiné'),
            ('internal_opinions', 'Sollicitation d\'avis internes'),
            ('external_opinions', 'Sollicitation d\'avis externes'),
            ('inquiry', 'Enquête publique'),
            ('class_1', 'Classe 1'),
            ('big', 'Superficie >= 2500m²'),
        )
        return DisplayList(vocab)

    def getProcedureDelays(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        unknown = 'ukn' in selection
        class_1 = 'class_1' in selection
        big = 'big' in selection
        delay = 30

        if unknown:
            return ''
        elif big or class_1:
            delay = 140
        else:
            delay = 90

        if self.prorogation:
            delay += 30

        return '{}j'.format(str(delay))

    security.declarePublic('listRegionalAuthorities')

    def listRegionalAuthorities(self):
        voc_terms = (
            ('dgo3', 'DGO3/DPE : Fonctionnaire technique'),
            ('dgo4', 'DGO4 : Fonctionnaire délégué'),
            ('dgo6', 'DGO6 : Fonctionnaire des implantations commerciales'),
        )
        vocabulary = DisplayList(voc_terms)
        return vocabulary

    security.declarePublic('getDefaultSPEReference')

    def getDefaultSPEReference(self):
        """
          Returns the reference for the new element
        """
        return ''


registerType(CODT_IntegratedLicence, PROJECTNAME)
# end of class CODT_IntegratedLicence

##code-section module-footer #fill in your manual code here

def finalizeSchema(schema):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('regional_authority', after='authority')

#finalizeSchema comes from BuildLicence to be sure to have the same changes reflected
firstBaseFinalizeSchema(CODT_IntegratedLicence_schema)
finalizeSchema(CODT_IntegratedLicence_schema)
##/code-section module-footer
