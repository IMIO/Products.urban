# -*- coding: utf-8 -*-

from Products.urban.interfaces import IUrbanDoc

from collective.documentgenerator.browser.generation_view import PersistentDocumentGenerationView

from plone import api

from zope.interface import alsoProvides


class UrbanDocGenerationView(PersistentDocumentGenerationView):
    """
    """

    def generate_persistent_doc(self, pod_template, output_format):
        persisted_doc = super(UrbanDocGenerationView, self).generate_persistent_doc(
            pod_template,
            output_format
        )
        alsoProvides(persisted_doc, IUrbanDoc)
        return persisted_doc

    def get_generation_format(self):
        portal_urban = api.portal.get_tool('portal_urban')
        output_format = portal_urban.getEditionOutputFormat()
        return output_format

    def get_base_generation_context(self):
        """
        Backward compatibility with code used in old urban templates.
        """
        portal_urban = api.portal.get_tool('portal_urban')
        licence = self.context.getParentNode()
        applicants = licence.getApplicants()
        proprietaries = licence.getProprietaries()
        applicantobj = applicants and applicants[0] or None
        proprietaryobj = proprietaries and proprietaries[0] or None

        generation_context = {
            'self': licence,
            'urbanEventObj': self.context,
            'applicantobj': applicantobj,
            'proprietaryobj': proprietaryobj,
            'tool': portal_urban
        }

        return generation_context
