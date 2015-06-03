# -*- coding: utf-8 -*-

from collective.documentgenerator.browser.generation_view import PersistentDocumentGenerationView

from plone import api


class UrbanDocGenerationView(PersistentDocumentGenerationView):
    """
    """

    def get_base_generation_context(self):
        """
        Override this method to be backward compatible with code used in old urban templates.
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
