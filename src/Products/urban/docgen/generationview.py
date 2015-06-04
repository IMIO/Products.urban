# -*- coding: utf-8 -*-

from Products.urban.interfaces import IUrbanDoc

from collective.documentgenerator.browser.generation_view import PersistentDocumentGenerationView

from plone import api

from zope.interface import directlyProvides


class UrbanDocGenerationView(PersistentDocumentGenerationView):
    """
    """

    def __call__(self):
        persisted_doc = self.generate_persistent_doc()
        directlyProvides(persisted_doc, IUrbanDoc)
        self.redirects(persisted_doc)

    def get_base_generation_context(self):
        """
        Backward compatibility with code used in old urban templates.
        """
        portal_urban = api.portal.get_tool('portal_urban')
        licence = self.context.getParentNode()
        applicants = licence.getApplicants()
        applicantobj = applicants and applicants[0] or None

        generation_context = {
            'self': licence,
            'urbanEventObj': self.context,
            'applicantobj': applicantobj,
            'tool': portal_urban
        }

        return generation_context
