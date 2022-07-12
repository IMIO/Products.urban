# -*- coding: utf-8 -*-
#
# File: UrbanEventAnnouncement.py
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
from Products.urban.content.UrbanEventInquiry import UrbanEventInquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from OFS.ObjectManager import BeforeDeleteException
from Products.CMFPlone import PloneMessageFactory as _
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
##/code-section module-header

schema = Schema((
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanEventAnnouncement_schema = BaseFolderSchema.copy() + \
    getattr(UrbanEventInquiry, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
UrbanEventAnnouncement_schema['eventDate'].widget.visible['edit'] = 'invisible'
UrbanEventAnnouncement_schema['eventDate'].widget.visible['view'] = 'invisible'
##/code-section after-schema


class UrbanEventAnnouncement(BaseFolder, UrbanEventInquiry, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanEventAnnouncement)

    meta_type = 'UrbanEventAnnouncement'
    _at_rename_after_creation = False

    schema = UrbanEventAnnouncement_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePrivate('manage_beforeDelete')

    def manage_beforeDelete(self, item, container):
        """
          We can only remove the last UrbanEventAnnouncement to avoid mismatch between
          existing announcements and UrbanEventAnnouncements
        """
        existingUrbanEventAnnouncements = self.getUrbanEventAnnouncements()
        lastUrbanEventAnnouncement = existingUrbanEventAnnouncements[-1]
        #if the user is not removing the last UrbanEventAnnouncement, we raise!
        if not lastUrbanEventAnnouncement.UID() == self.UID():
            raise BeforeDeleteException, _(
                'cannot_remove_urbaneventannouncement_notthelast',
                mapping={'lasturbaneventannouncementurl': lastUrbanEventAnnouncement.absolute_url()},
                default="You can not delete an UrbanEventAnnouncement if it is not the last!  Remove the last UrbanEventAnnouncements before being able to remove this one!"
            )
        BaseFolder.manage_beforeDelete(self, item, container)

    security.declarePublic('getClaimants')

    def getClaimants(self):
        """
          Return the claimants for this UrbanEventAnnouncement
        """
        return self.listFolderContents({'portal_type': 'Claimant'})

    security.declarePublic('getAbbreviatedArticles')

    def getAbbreviatedArticles(self):
        """
          As we have a short version of the article in the title, if we need just
          the list of articles (330 1°, 330 2°, ...) we will use the extraValue of the Vocabulary term
        """
        return self.displayValue(UrbanVocabulary('announcementarticles', value_to_use="extraValue").getDisplayList(self), self.getLinkedInquiry().getAnnouncementArticles())

    def getKeyDate(self):
        return self.getInvestigationStart()


registerType(UrbanEventAnnouncement, PROJECTNAME)
# end of class UrbanEventAnnouncement

##code-section module-footer #fill in your manual code here
##/code-section module-footer

