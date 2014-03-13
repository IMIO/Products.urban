# -*- coding: utf-8 -*-

from Products.urban.utils import getOsTempFolder

from StringIO import StringIO

from plone import api

from zope.component import queryAdapter
from zope.interface import Interface
from zope.interface import implements

import appy.pod.renderer
import os
import time


def generateUrbanDocFile(container, odt_template, appy_context=None):

    if not appy_context:
        appy_context = {}

    appy_context.update({'template': odt_template})
    more_appy_context = queryAdapter(container, IAppyContext)
    if more_appy_context:
        appy_context.update(more_appy_context.get())

    portal_urban = api.portal.get_tool('portal_urban')
    file_type = portal_urban.getEditionOutputFormat()

    temp_filename = '%s/%s_%f.%s' % (getOsTempFolder(), odt_template._at_uid, time.time(), file_type)
    temp_file_names = {}

    global_templates = getattr(portal_urban, 'globaltemplates')
    auto_imported_template_ids = ['header.odt', 'footer.odt', 'reference.odt', 'signatures.odt']
    for template_id in auto_imported_template_ids:
        #do only import necessary templates if exists...
        template = getattr(global_templates, template_id)
        if not template or not template.size:
            continue
        template = StringIO(template)
        temp_file_name = '%s/%s_%f.%s' % (getOsTempFolder(), odt_template._at_uid, time.time(), 'odt')
        #remove the '.odt' suffix so terms like "header" can be used in the templates instead of "header.odt"
        temp_file_names[os.path.splitext(template_id)[0]] = temp_file_name
        #we render the template so pod instructions into the generic sub-templates are rendered too
        renderer = appy.pod.renderer.Renderer(
            template,
            appy_context,
            temp_file_name,
            pythonWithUnoPath=portal_urban.getUnoEnabledPython()
        )
        renderer.run()

    #now that sub-templates are rendered, we can use them in the main pod template and render the entire document
    #we prepare the styles template
    styles_template = getattr(global_templates, 'styles.odt', None)
    if styles_template and styles_template.size:
        styles_template = StringIO(styles_template)
    appy_context.update(temp_file_names)
    renderer = appy.pod.renderer.Renderer(
        StringIO(odt_template),
        appy_context,
        temp_filename,
        pythonWithUnoPath=portal_urban.getUnoEnabledPython(),
    )
    renderer.run()

    # Returns the doc and removes the temp file
    f = open(temp_filename, 'rb')
    doc = f.read()
    f.close()
    os.remove(temp_filename)

    return doc


class IAppyContext(Interface):
    """ Adapts an object into an appy.pod generation context """

    def get():
        """ Return a dict use as context for appy.pod to generate odt document"""


class UrbanEventAppyContext:
    implements(IAppyContext)

    def __init__(self, urban_event):
        portal_urban = api.portal.get_tool('portal_urban')
        licence = urban_event.getParentNode()
        applicants = licence.getApplicants()
        applicantobj = applicants and applicants[0] or None

        self.appy_context = {
            'self': licence,
            'urbanEventObj': urban_event,
            'applicantobj': applicantobj,
            'tool': portal_urban
        }

    def get(self):
        return self.appy_context
