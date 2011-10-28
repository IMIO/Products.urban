from Products.urban.exportimport import addUrbanEventTypes
from Products.urban.exportimport import addGlobalTemplates

def updateAllUrbanTemplates(context):
    if context.readDataFile('urban_testCommunes_marker.txt') is None:
        return
    addGlobalTemplates(context)
    addUrbanEventTypes(context)
