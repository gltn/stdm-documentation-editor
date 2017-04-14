import sys
import os

from PyQt4.QtGui import QApplication

import git
from git import Repo

from help_editor import HelpEditor

class GitWrapper(object):
    def __init__(self, repo):
        if not os.path.exists(repo):
            print "Repo path does not exists!"
            return
        else:
            try:
                self.repo = Repo(repo)
            except:
                print "Not a valid git repo!"
                return

    def git_add(self):
        pass
    def git_commit(self):
        pass
    def git_clone(self):
        pass
    def get_modified_files(self):
        mfiles = []
        mfiles = self.repo.git.diff(name_only=True).split('\n')
        return mfiles
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HelpEditor()
    window.show()
    sys.exit(app.exec_()) 


