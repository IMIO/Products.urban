import os
import platform
import uno
import unohelper
import urllib
import urllib2
import xml.etree.ElementTree as ET

from com.sun.star.awt import XActionListener
from com.sun.star.awt import XTextListener
from com.sun.star.awt import XItemListener
from com.sun.star.awt import XWindowListener
from com.sun.star.awt import XMouseListener
from com.sun.star.awt import FontDescriptor

configurl = "http://svn.communesplone.org/svn/communesplone/Products.urban/trunk/src/Products/urban/scripts/config.xml"

com_sun_star_awt_WindowAttribute_SHOW = uno.getConstantByName(
    "com.sun.star.awt.WindowAttribute.SHOW"
)
com_sun_star_awt_WindowAttribute_FULLSIZE = uno.getConstantByName(
    "com.sun.star.awt.WindowAttribute.FULLSIZE"
)
com_sun_star_awt_WindowAttribute_OPTIMUMSIZE = uno.getConstantByName(
    "com.sun.star.awt.WindowAttribute.OPTIMUMSIZE"
)
com_sun_star_awt_WindowAttribute_MINSIZE = uno.getConstantByName(
    "com.sun.star.awt.WindowAttribute.MINSIZE"
)
com_sun_star_awt_WindowAttribute_BORDER = uno.getConstantByName(
    "com.sun.star.awt.WindowAttribute.BORDER"
)
com_sun_star_awt_WindowAttribute_SIZEABLE = uno.getConstantByName(
    "com.sun.star.awt.WindowAttribute.SIZEABLE"
)
com_sun_star_awt_WindowAttribute_MOVEABLE = uno.getConstantByName(
    "com.sun.star.awt.WindowAttribute.MOVEABLE"
)
com_sun_star_awt_WindowAttribute_CLOSEABLE = uno.getConstantByName(
    "com.sun.star.awt.WindowAttribute.CLOSEABLE"
)
com_sun_star_awt_WindowAttribute_SYSTEMDEPENDENT = uno.getConstantByName(
    "com.sun.star.awt.WindowAttribute.SYSTEMDEPENDENT"
)
com_sun_star_awt_possize = uno.getConstantByName("com.sun.star.awt.PosSize.POSSIZE")
com_sun_star_awt_InvalidateStyle_Update = uno.getConstantByName(
    "com.sun.star.awt.InvalidateStyle.UPDATE"
)


class ListItemListener(unohelper.Base, XItemListener):
    def __init__(self, window, combobox1, combobox2, label1, objects):
        self.combobox1 = combobox1
        self.combobox2 = combobox2
        self.window = window
        self.label1 = label1
        self.objects = objects

    def itemStateChanged(self, itemEvent):
        refreshcombo(self.combobox1.getText(), self.combobox2, self.objects)
        self.window.invalidate(com_sun_star_awt_InvalidateStyle_Update)


class InsertButtonListener(unohelper.Base, XActionListener):
    def __init__(self, smgr, combobox1, combobox2, desktop, objects):
        self.combobox1 = combobox1
        self.combobox2 = combobox2
        self.objects = objects
        self.desktop = desktop
        self.smgr = smgr

    def actionPerformed(self, actionEvent):
        document = self.desktop.getCurrentComponent()
        viewcursor = document.getCurrentController().getViewCursor()
        ocurs = document.getText().createTextCursorByRange(viewcursor.getStart())
        i = 0
        for obj in self.objects:
            if self.combobox1.getText() == obj.attrib["name"]:
                for item in obj:
                    if self.combobox2.getText() == item.attrib["name"]:
                        for action in item:
                            if action.tag == "FieldCode":
                                txtfield = document.createInstance(
                                    "com.sun.star.text.TextField.Input"
                                )
                                txtfield.Content = action.text.strip()
                                txtfield.Hint = (
                                    self.combobox1.getText()
                                    + "-"
                                    + self.combobox2.getText()
                                )
                                document.Text.insertTextContent(ocurs, txtfield, False)
                            if action.tag == "AnnotationCode":
                                annotation = document.createInstance(
                                    "com.sun.star.text.TextField.Annotation"
                                )
                                annotation.Author = "urban"
                                annotation.Content = action.text.strip()
                                document.Text.insertTextContent(
                                    ocurs, annotation, False
                                )


class WindowListener(unohelper.Base, XWindowListener):
    def __init__(self, window, combobox1):
        self.window = window
        self.combobox1 = combobox1

    def windowResized(self, actionEvent):
        rect = self.window.getPosSize()
        self.window.invalidate(com_sun_star_awt_InvalidateStyle_Update)


def refreshcombo(valcombobox1, combobox2, objects):
    i = 0
    nCount = combobox2.getItemCount()
    combobox2.removeItems(0, nCount)
    for obj in objects:
        if valcombobox1 == obj.attrib["name"]:
            for item in obj:
                combobox2.addItem(item.attrib["name"], i)
                i = i + 1


def appyTE(self):
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    oAwtToolkit = smgr.createInstance("com.sun.star.awt.Toolkit")
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    oWindow = createTopWindow(
        "Insertion de champs urban", ctx, smgr, oAwtToolkit, 100, 80, 400, 100
    )
    label1 = addLabel(
        oWindow,
        smgr,
        ctx,
        "FixedText",
        5,
        15,
        70,
        28,
        ("Name", "Label"),
        ("label", u"Objet:"),
    )
    label2 = addLabel(
        oWindow,
        smgr,
        ctx,
        "FixedText",
        5,
        40,
        70,
        28,
        ("Name", "Label"),
        ("label", u"Elément:"),
    )
    combobox1 = addComboBox(oWindow, smgr, ctx, "Combobox", 75, 15, 300, 20)
    combobox2 = addComboBox(oWindow, smgr, ctx, "Combobox", 75, 40, 300, 20)
    button1 = addButton(
        oWindow, smgr, ctx, "Button", 10, 75, 100, 20, ("Label",), (u"Insérer",)
    )
    filepath = os.path.split(__file__)[0].split("file:")[1]
    if platform.system() == "Windows":
        filepath = filepath[3:]
    else:
        filepath = filepath[2:]
    filepath = "/".join([filepath, "config.xml"])
    filepath = filepath.replace("%20", " ")
    handle = open(filepath, "r")
    config = handle.read()
    objects = ET.XML(config).findall("Object")
    oWindow.addWindowListener(WindowListener(oWindow, combobox1))
    combobox1.addItemListener(
        ListItemListener(oWindow, combobox1, combobox2, label1, objects)
    )
    button1.addActionListener(
        InsertButtonListener(smgr, combobox1, combobox2, desktop, objects)
    )
    i = 0
    for obj in objects:
        combobox1.addItem(obj.attrib["name"], i)
        i = i + 1


def addButton(window, smgr, self, cCtrlName, x, y, width, height, names, values):
    oControlModel = smgr.createInstance("com.sun.star.awt.UnoControlButtonModel")
    oControlModel.setPropertyValues(names, values)
    oControl = smgr.createInstance(oControlModel.DefaultControl)
    oControl.setModel(oControlModel)
    AwtToolkit = smgr.createInstance("com.sun.star.awt.Toolkit")
    oControl.createPeer(AwtToolkit, window)
    oControl.setPosSize(x, y, width, height, com_sun_star_awt_possize)
    return oControl


def addLabel(window, smgr, self, cCtrlName, x, y, width, height, names, values):
    oControlModel = smgr.createInstance("com.sun.star.awt.UnoControlFixedTextModel")
    oControlModel.setPropertyValues(names, values)
    oControl = smgr.createInstance(oControlModel.DefaultControl)
    oControl.setModel(oControlModel)
    AwtToolkit = smgr.createInstance("com.sun.star.awt.Toolkit")
    oControl.createPeer(AwtToolkit, window)
    oControl.setPosSize(x, y, width, height, com_sun_star_awt_possize)
    return oControl


def addComboBox(window, smgr, self, cCtrlName, x, y, width, height):
    oControlModel = smgr.createInstance("com.sun.star.awt.UnoControlComboBoxModel")
    oControlModel.Dropdown = True
    oControl = smgr.createInstance(oControlModel.DefaultControl)
    oControl.setModel(oControlModel)
    AwtToolkit = smgr.createInstance("com.sun.star.awt.Toolkit")
    oControl.createPeer(AwtToolkit, window)
    oControl.setEditable(True)
    oControl.setPosSize(x, y, width, height, com_sun_star_awt_possize)
    return oControl


def createTopWindow(sTitle, ctx, smgr, oAwtToolkit, x, y, width, height):
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    oCoreReflection = smgr.createInstanceWithContext(
        "com.sun.star.reflection.CoreReflection", ctx
    )
    oXIdlClass = oCoreReflection.forName("com.sun.star.awt.WindowDescriptor")
    oReturnValue, oWindowDesc = oXIdlClass.createObject(None)
    oWindowDesc.Type = uno.getConstantByName("com.sun.star.awt.WindowClass.TOP")
    oWindowDesc.WindowServiceName = ""
    oWindowDesc.Parent = (
        desktop.getCurrentComponent().CurrentController.Frame.ContainerWindow
    )
    gnDefaultWindowAttributes = (
        com_sun_star_awt_WindowAttribute_SHOW
        + com_sun_star_awt_WindowAttribute_BORDER
        + com_sun_star_awt_WindowAttribute_MOVEABLE
        + com_sun_star_awt_WindowAttribute_CLOSEABLE
    )
    oXIdlClass = oCoreReflection.forName("com.sun.star.awt.Rectangle")
    oReturnValue, oRect = oXIdlClass.createObject(None)
    oRect.X = x
    oRect.Y = y
    oRect.Width = width
    oRect.Height = height
    oWindowDesc.Bounds = oRect
    oWindowDesc.WindowAttributes = gnDefaultWindowAttributes
    oWindow = oAwtToolkit.createWindow(oWindowDesc)
    oWindow.setBackground(10081175)
    oFrame = smgr.createInstanceWithContext("com.sun.star.frame.Frame", ctx)
    oFrame.initialize(oWindow)
    oFrame.setCreator(desktop)
    oFrame.Title = sTitle
    oFrame.activate()
    return oWindow
