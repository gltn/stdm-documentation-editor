
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QIcon

from help_editor import HelpEditor
from . import PLUGIN_DIR


class StdmDocumentationEditor(object):
    """
    StdmDocumentationEditor initializes the whole plugin and adds the plugin
    on toolbar of GGIS.
    """
    def __init__(self, iface):
        """
        Initializes iface and importer object.
        :param iface:
        :type iface:
        """
        self.iface = iface
        self.editor = None

    def initGui(self):
        """
        Initializes the plugin GUI.
        """
        self.action = QAction(
            QIcon('{}/images/icon.png'.format(PLUGIN_DIR)),
            'STDM Documentation Editor', self.iface.mainWindow()
        )
        self.action.setObjectName('stdm_documentation_editor')
        self.action.setWhatsThis('STDM Documentation Editor')
        self.action.setStatusTip('Edit STDM Documentation')
        self.action.triggered.connect(self.run)

        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        """
        Removes the plugin properly.
        """
        # remove the plugin menu item and icon
        self.iface.removePluginMenu('&STDM Documentation Editor', self.action)
        self.iface.removeToolBarIcon(self.action)
        # disconnect form signal of the canvas
        self.action.triggered.disconnect(self.run)

    def run(self):
        """
        Starts the plugin GUI.
        """
        if self.editor is None:
            self.editor = HelpEditor()
            self.editor.show()
        else:
            self.editor.show()
            self.editor.activateWindow()
