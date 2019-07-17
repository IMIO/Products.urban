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
         - return the url of the generated doc (to open it in external edit)
        """
        self.pod_template, self.output_format = self._get_base_args(template_uid, output_format)

        persisted_doc = self.generate_persistent_doc(self.pod_template, self.output_format)
        alsoProvides(persisted_doc, IUrbanDoc)

        return persisted_doc.absolute_url()

    def get_generation_format(self):
        pod_template = self.get_pod_template(self.get_pod_template_uid())
        output_formats = pod_template.get_available_formats()
        if len(output_formats) != 1:
            portal_urban = api.portal.get_tool('portal_urban')
            output_format = portal_urban.getEditionOutputFormat()
        else:
            output_format = output_formats[0]
        return output_format

    def get_base_generation_context(self):
        """
        Backward compatibility with code used in old urban templates.
        """
        portal_urban = api.portal.get_tool('portal_urban')
        licence = self.context.getParentNode()
        applicants = licence.getApplicants()
        applicantobj = applicants and applicants[0] or None
        proprietaries = licence.getProprietaries()
        proprietaryobj = proprietaries and proprietaries[0] or None
        publicity = hasattr(licence, 'getLastInquiry') and licence.getLastInquiry() or hasattr(licence,
                'getLastAnnouncement') and licence.getLastAnnouncement() or None
        claimants = (publicity and hasattr(publicity, 'getClaimants')) and publicity.getClaimants() or None
        claimants_view = claimants and [claimant.restrictedTraverse('@@document_generation_helper_view') for claimant in
                claimants] or None
        claimants_view = claimants_view and [(view.context, view) for view in claimants_view]
        proprietaries = (publicity and hasattr(publicity, 'getRecipients')) and publicity.getRecipients() or None
        proprietaries_views = proprietaries and [proprietary.restrictedTraverse('@@document_generation_helper_view') for proprietary in
                proprietaries] or None
        proprietaries_views = proprietaries_views and [(view.context, view) for view in proprietaries_views]
        licence_helper_view = licence.restrictedTraverse('@@document_generation_helper_view')
        event_helper_view = self.context.restrictedTraverse('@@document_generation_helper_view')

        generation_context = {
            'this': licence,
            'self': licence_helper_view.context,
            'licence': licence_helper_view.context,
            'event': self.context,
            'urbanEventObj': self.context,
            'applicantobj': applicantobj,
            'proprietaryobj': proprietaryobj,
            'tool': portal_urban,
            'licence_view': licence_helper_view,
            'licence_helper': licence_helper_view.context,
            'event_view': event_helper_view,
            'event_helper': event_helper_view.context,
            'claimants': claimants_view,
            'inquiry_proprietaries': proprietaries_views,
        }

        return generation_context

    def get_views_for_appy_renderer(self, generation_context, helper_view):
        views = [
            helper_view,
            generation_context['licence_view'],
            generation_context['event_view'],
        ]
        if generation_context['claimants']:
            views.extend([view for proxy, view in generation_context['claimants']])
        if generation_context['inquiry_proprietaries']:
            views.extend([view for proxy, view in generation_context['inquiry_proprietaries']])
        return views
