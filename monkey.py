from Products.DataGridField.Column import Column

"""
Monkey patch the call to the Column __init__: redturturtle use its own branch of DataGridField.Column which was modified
to include the 'required' parameter but the Plone DataGridField.Column does not handle this parameter and crash when called
with it.
"""

def patchedColumnInit(self, label, default=None, default_method=None,
             label_msgid=None, required=False, object_provides=[],
             surf_site=True, search_site=True):
    # removed the argument 'required'
    Column.__init__(self, label, default=default, default_method=default_method,
                    label_msgid=label_msgid)
    #original line:
    # Column.__init__(self, label, default=default, default_method=default_method, label_msgid=label_msgid, required=required)
    self.object_provides = object_provides
    self.surf_site = surf_site
    self.search_site = search_site
