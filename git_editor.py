import sys
from PyQt4.QtGui import QApplication

from help_editor import HelpEditor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HelpEditor()
    window.show()
    sys.exit(app.exec_()) 


