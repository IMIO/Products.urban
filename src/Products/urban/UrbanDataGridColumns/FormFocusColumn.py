from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.DataGridField.FixedColumn import FixedColumn


class FormFocusColumn(FixedColumn):
    """
     On view mode, doesnt display anything.

     On edit mode, add a column wich can display a popup to edit fields located
     elsewhere on the form.
    """
    security = ClassSecurityInfo()

    def __init__(self, label, default=None, label_msgid=None, visible=True):
        """ Create a column

            @param hide Hide column from displaying
        """
        FixedColumn.__init__(self, label, default, label_msgid)
        self.visible = visible

    security.declarePublic('getMacro')
    def getMacro(self):
        """ Return macro used to render this column in view/edit """
        return "datagrid_formfocus_cell"


# Initializes class security
InitializeClass(FixedColumn)
