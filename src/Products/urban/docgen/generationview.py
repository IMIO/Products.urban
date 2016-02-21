# -*- coding: utf-8 -*-

from Products.urban.interfaces import IUrbanDoc

from collective.documentgenerator.browser.generation_view import PersistentDocumentGenerationView

from plone import api

from zope.interface import alsoProvides


class UrbanDocGenerationView(PersistentDocumentGenerationView):
    """
    """

    def __call__(self, template_uid='', output_format=''):
        """
        Override the call to:
         - mark the document with IUrbanDoc interface
         - return the url of the generated doc
        """
        pod_template, output_format = self._get_base_args(template_uid, output_format)

        persisted_doc = self.generate_persistent_doc(pod_template, output_format)
        alsoProvides(persisted_doc, IUrbanDoc)

        return persisted_doc.absolute_url()

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
