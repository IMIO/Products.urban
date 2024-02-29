import uno
import unohelper
from com.sun.star.style.BreakType import PAGE_BEFORE, PAGE_AFTER, PAGE_BOTH, NONE
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK


def Mailing(self):
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    sourceDoc = desktop.getCurrentComponent()
    sourceDocViewcursor = sourceDoc.getCurrentController().getViewCursor()
    sourceDocDispatcher = smgr.createInstanceWithContext(
        "com.sun.star.frame.DispatchHelper", ctx
    )
    sourceDocFrame = sourceDoc.getCurrentController().getFrame()
    destinationDoc = desktop.loadComponentFromURL(
        "private:factory/swriter", "_blank", 0, ()
    )
    destinationDocFrame = destinationDoc.getCurrentController().getFrame()
    destinationDocDispatcher = smgr.createInstanceWithContext(
        "com.sun.star.frame.DispatchHelper", ctx
    )
    replaceDesc = destinationDoc.createReplaceDescriptor()
    recipientscsv = ExtractionPlageTexteDelimite(sourceDoc)
    recipientslist = recipientscsv.split("%")
    firstItem = True
    for recipient in recipientslist:
        if firstItem:
            firstItem = False
            rfields = recipient.split("|")
        else:
            rvalues = recipient.split("|")
            sourceDocDispatcher.executeDispatch(
                sourceDocFrame, ".uno:SelectAll", "", 0, ()
            )
            sourceDocDispatcher.executeDispatch(sourceDocFrame, ".uno:Copy", "", 0, ())
            destinationDocDispatcher.executeDispatch(
                destinationDocFrame, ".uno:Paste", "", 0, ()
            )
            for i in range(len(rfields)):
                replaceDesc.SearchString = "<%" + rfields[i] + "%>"
                replaceDesc.ReplaceString = rvalues[i]
                destinationDoc.replaceAll(replaceDesc)
            oCurseur = destinationDoc.getCurrentController().getViewCursor()
            Cible = oCurseur.getText()
            Cible.insertControlCharacter(oCurseur, PARAGRAPH_BREAK, False)
            oCurseur.setPropertyValue("BreakType", PAGE_BEFORE)


def ExtractionPlageTexteDelimite(sourceDoc):
    sourceDocSD = sourceDoc.createSearchDescriptor()
    sourceDocSD.SearchString = "\[CSV\].*\[/CSV\]"
    sourceDocSD.SearchRegularExpression = True
    Plage = sourceDoc.findFirst(sourceDocSD)
    if Plage.String:
        toreturn = Plage.String
    else:
        toreturn = ""
    toreturn = toreturn.replace("[CSV]", "")
    toreturn = toreturn.replace("[/CSV]", "")
    return toreturn
