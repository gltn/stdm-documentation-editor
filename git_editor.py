import sys
import os

from PyQt4.QtGui import (
        QApplication,
        QDialog
)

from PyQt4.QtCore import (
        QObject,
        pyqtSignal,
        QThread
)

import git
from git import (
        Repo,
        RemoteProgress
)

from help_editor import HelpEditor

from settings import (
        PLUGIN_DIR,
        DOC,              # docs
        DEFAULT_VERSION,  # 1_5
        LANGUAGE          # en
)

from ui.clone_editor import Ui_CloneEditor

# DOC_CLONE_DIR = 'STDMdocs'
DOC_CLONE_DIR = 'home\\QGISApp\\STDM\\dev\\SDE\\doctest2'
REMOTE_REPO='https://github.com/gltn/stdm-documentation.git'

class ProgressPrinter(RemoteProgress):
    def __init__(self, gw):
        self.gw = gw
    def update(self, op_code, cur_count, max_count=None, message=''):
        #self.gw.update_progress.emit()
        print op_code, cur_count, max_count, cur_count/(max_count or 100.0), message or "No Message!"

class GitWrapper(QObject):
    clone_started = pyqtSignal()
    update_progress = pyqtSignal()

    def __init__(self, repo, parent=None):
        QObject.__init__(self, parent)

        if not os.path.exists(repo):
            #raise Exception("Repo path does not exists!")
            self.repo = None
        else:
            try:
                self.repo = Repo(repo)
            except:
                self.repo = None
                #raise Exception("Not a valid git repo!")

    def git_add(self):
        self.repo.git.add(u=True) # add modified files
        self.repo.git.add(A=True) # add untracked files

    def commit_message(self):
        return "Added enemy files"

    def git_commit(self):
        self.repo.git.commit("-m", self.commit_message())

    def clone_dir(self):
        '''
        Formats a path string where to clone the repo
        :rtype: str
        '''
        drive, path = os.path.splitdrive(PLUGIN_DIR)
        docs_dir = '{}\\{}'.format(drive, DOC_CLONE_DIR)
        return docs_dir

    def make_symlink(self):
        doc_dir = '{}\{}'.format(DOC, DEFAULT_VERSION)
        slink_postfix = '{}\\'.format(doc_dir)
        dest_dir = '{}\{}'.format(self.clone_dir(), slink_postfix)
        cmd = "mkslink.sh {} {}".format(doc_dir, dest_dir)
        os.system(cmd)

    def clone(self):
        self.clone_started.emit() 
        Repo.clone_from(REMOTE_REPO, self.clone_dir(), progress=ProgressPrinter(self))
        #print "Done cloning."

    def git_push(self):
        '''
         Authentication:
         git remote set-url origin https://<name>:<password>@github.com/repo.git
        '''
        pass

    def modified_files(self):
        '''
        modified files
        :rtype: list
        '''
        mfiles = []
        mfiles = self.repo.git.diff(name_only=True).split('\n')
        return mfiles

    def untracked_files(self):
        '''
        new untracked files
        :rtype: list
        '''
        return self.repo.untracked_files


class CloneEditor(QDialog, Ui_CloneEditor):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        cdir = '\\{}'.format(DOC_CLONE_DIR)
        self.git_wrap = GitWrapper(cdir)
        self.init_gui()

    def __del__(self):
        QDialog.__del__(self)
        sys.stdout = sys.__stdout__

    def update(self, op_code, cur_count, max_count):
        print "CloneEditor::update()"
        self.edtOut.append(str(max_count))
        #op_code, cur_count, max_count, cur_count/(max_count or 100.0), message or "No Message!"
    def init_gui(self):
        self.btnClone.clicked.connect(self.clone_repo)

    def clone_repo(self):
        self.clone_update = QThread(self)
        self.git_wrap.moveToThread(self.clone_update)
        self.git_wrap.clone_started.connect(self.start_clone)
        self.git_wrap.update_progress.connect(self.clone_updates)

        self.clone_update.started.connect(self._clone_start)

        self.clone_update.start()

    def _clone_start(self):
        sys.stdout = self.clone_updates
        self.git_wrap.clone()

    def start_clone(self):
        self.edtOut.append("Cloning started ...")

    def clone_updates(self):
        self.edtOut.append("Cloning in progress ..")


if __name__ == '__main__':
    cdir = '\\{}'.format(DOC_CLONE_DIR)
    #gw = GitWrapper(cdir)
    #gw.repo = Repo(gw.clone())
    #gw.make_symlink()
    app = QApplication(sys.argv)
    window = HelpEditor()
    window.show()
    sys.exit(app.exec_()) 


