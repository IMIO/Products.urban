from plone import api
from Products.Five import BrowserView

# !!! MUST INSTALL wildcard.fixpersistentutilities FOR THIS VIEW TO WORK !!!

interfaces_to_clean = [
    "Products.csvreplicata.interfaces.ICSVDefault",
    "Products.csvreplicata.interfaces.ICSVFile",
    "Products.csvreplicata.interfaces.ICSVReplicable",
    "Products.csvreplicata.interfaces.ICSVReplicataObjectsSearcher",
    "Products.csvreplicata.interfaces.ICSVReplicataExportImportPlugin",
    "Products.csvreplicata.interfaces.ICSVReplicataExportPlugin",
]


class CleanCSVReplicata(BrowserView):
    """ """

    def __call__(self):
        site = self.context
        # del csv replicata tool
        if "portal_csvreplicatatool" in site.objectIds():
            index = site.objectIds().index("portal_csvreplicatatool")
            delattr(site, "portal_csvreplicatatool")
            new_objects = site._objects[:index]
            if len(site._objects) > index + 1:
                new_objects += site._objects[index + 1 :]
            site._objects = new_objects

        cleaning_view = site.restrictedTraverse("@@fix-interfaces-fpu")
        self.request.set("submitted", True)
        for interface in interfaces_to_clean:
            self.request.set("dottedname", interface)
            print self.request.dottedname
            cleaning_view()
