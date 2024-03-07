from collective.documentgenerator.content import pod_template
from plone import api
from StringIO import StringIO

import lxml
import zipfile


def check_corrupted_templates(context):
    catalog = api.portal.get_tool("portal_catalog")
    out = open("../corrupted_models.txt", "a")
    for brain in catalog(object_provides=pod_template.IPODTemplate.__identifier__):
        template = brain.getObject()
        raw_content = zipfile.ZipFile(StringIO(template.odt_file.data)).read(
            "content.xml"
        )
        try:
            lxml.etree.fromstring(raw_content)
        except Exception:
            infos = repr(template) + " " + template.Title() + "\n"
            out.write(infos)
    out.close()
