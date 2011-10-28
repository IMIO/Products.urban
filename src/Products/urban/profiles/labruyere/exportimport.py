from Products.urban.exportimport import addUrbanEventTypes
from Products.urban.exportimport import addGlobalTemplates

def updateAllLabruyereTemplates(context):
    if context.readDataFile('urban_labruyere_marker.txt') is None:
        return
    addGlobalTemplates(context)
    addUrbanEventTypes(context)
