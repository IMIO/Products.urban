# -*- coding: utf-8 -*-
"""
    Export folder contents as JSON.
    Can be run as a browser view or command line script.
"""

import os
import base64

try:
    import json
except ImportError:
    # Python 2.54 / Plone 3.3 use simplejson
    # version > 2.3 < 3.0
    import simplejson as json

from Products.Five.browser import BrowserView
from Products.CMFCore.interfaces import IFolderish
from DateTime import DateTime

#: Private attributes we add to the export list
EXPORT_ATTRIBUTES = ["portal_type", "id"]

#: Do we dump out binary data... default we do, but can be controlled with env var
EXPORT_BINARY = os.getenv("EXPORT_BINARY", None)
if EXPORT_BINARY:
    EXPORT_BINARY = EXPORT_BINARY == "true"
else:
    EXPORT_BINARY = True

class ExportFolderAsJSON(BrowserView):
    """
    Exports the current context folder Archetypes as JSON.
    Returns downloadable JSON from the data.
    """

    def convert(self, value):
        """
        Convert value to more JSON friendly format.
        """
        if isinstance(value, DateTime):
            # Zope DateTime
            # http://pypi.python.org/pypi/DateTime/3.0.2
            return value.ISO8601()
        elif hasattr(value, "isBinary") and value.isBinary():

            if not EXPORT_BINARY:
                return None

            # Archetypes FileField and ImageField payloads
            # are binary as OFS.Image.File object
            data = getattr(value.data, "data", None)
            if not data:
                return None
            return base64.b64encode(data)
        else:
            # Passthrough
            return value

    def grabArchetypesData(self, obj):
        """
        Export Archetypes schemad data as dictionary object.
        Binary fields are encoded as BASE64.
        """
        data = {'UID': obj.UID()}
        for field in obj.Schema().fields():
            name = field.getName()
            value = field.getRaw(obj)
            print "%s" % (value.__class__)

            data[name] = self.convert(value)
        return data

    def grabAttributes(self, obj):
        data = {}
        for key in EXPORT_ATTRIBUTES:
            data[key] = self.convert(getattr(obj, key, None))
        return data

    def export(self, folder, recursive=True):
        """
        Export content items.
        Possible to do recursively nesting into the children.
        :return: list of dictionaries
        """

        array = []
        for obj in folder.listFolderContents():
            data = self.grabArchetypesData(obj)
            data.update(self.grabAttributes(obj))

            if recursive:
                if IFolderish.providedBy(obj):
                    data["children"] = self.export(obj, True)

            array.append(data)

        return array

    def __call__(self):
        """
        """
        folder = self.context.aq_inner
        data = self.export(folder)
        pretty = json.dumps(data, sort_keys=True)
        self.request.response.setHeader("Content-type", "application/json")
        return pretty

def spoof_request(app):
    """
    http://developer.plone.org/misc/commandline.html
    """
    from AccessControl.SecurityManagement import newSecurityManager
    from AccessControl.SecurityManager import setSecurityPolicy
    from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser
    _policy = PermissiveSecurityPolicy()
    setSecurityPolicy(_policy)
    newSecurityManager(None, OmnipotentUser().__of__(app.acl_users))
    return app

def run_export_as_script(path):
    """ Command line helper function.
    Using from the command line::
        bin/instance script export.py yoursiteid/path/to/folder
    If you have a lot of binary data (images) you probably want
        bin/instance script export.py yoursiteid/path/to/folder > yourdata.json
    ... to prevent your terminal being flooded with base64.
    Or just pure data, no binary::
        EXPORT_BINARY=false bin/instance run export.py yoursiteid/path/to/folder
    :param path: Full ZODB path to the folder
    """
    global app

    secure_aware_app = spoof_request(app)
    folder = secure_aware_app.unrestrictedTraverse(path)
    view = ExportFolderAsJSON(folder, None)
    data = view.export(folder, recursive=True)
    # Pretty pony is prettttyyyyy
    pretty = json.dumps(data, sort_keys=True, indent='    ')
    print pretty

# Detect if run as a bin/instance run script
if "app" in globals():
    run_export_as_script(sys.argv[1])
