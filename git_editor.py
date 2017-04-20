import sys
import os

from PyQt4.QtGui import QApplication

import git
from git import Repo

from help_editor import HelpEditor
from settings import (
        PLUGIN_DIR,
        DOC,              # docs
        DEFAULT_VERSION,  # 1_5
        LANGUAGE          # en
)

# DOC_CLONE_DIR = 'STDMdocs'
DOC_CLONE_DIR = 'home\\QGISApp\\STDM\\dev\\SDE\\doctest'
REMOTE_REPO='https://github.com/gltn/stdm-documentation.git'

class GitWrapper(object):
    def __init__(self, repo):
        if not os.path.exists(repo):
            raise Exception("Repo path does not exists!")
        else:
            try:
                self.repo = Repo(repo)
            except:
                raise Exception("Not a valid git repo!")

    def git_add(self):
        self.repo.git.add(u=True) # add modified files
        self.repo.git.add(A=True) # add untracked files

    def commit_message(self):
        return "Added enemy files"

    def git_commit(self):
        self.repo.git.commit("-m", self.commit_message())

    def clone_dir(self):
        drive, path = os.path.splitdrive(PLUGIN_DIR)
        docs_dir = '{}\\{}'.format(drive, DOC_CLONE_DIR)
        return docs_dir

    def make_symlink(self):
        doc_dir = '{}\{}'.format(DOC, DEFAULT_VERSION)
        slink_postfix = '{}\\'.format(doc_dir)
        dest_dir = '{}\{}'.format(self.clone_dir(), slink_postfix)
        cmd = "mkslink.sh {} {}".format(doc_dir, dest_dir)
        os.system(cmd)

    def git_clone(self):
        print "Cloning started ..."
        Repo.clone_from(REMOTE_REPO, self.clone_dir())
        print "Done cloning."

    def git_push(self):
        '''
         Authentication:
         git remote set-url origin https://<name>:<password>@github.com/repo.git
        '''
        pass

    def modified_files(self):
        '''
        modified files
        '''
        mfiles = []
        mfiles = self.repo.git.diff(name_only=True).split('\n')
        return mfiles

    def untracked_files(self):
        '''
        new files
        '''
        return self.repo.untracked_files

if __name__ == '__main__':
    cdir = '\\{}'.format(DOC_CLONE_DIR)
    gw = GitWrapper(cdir)
    #gw.git_clone()
    gw.make_symlink()
    #app = QApplication(sys.argv)
    #window = HelpEditor()
    #window.show()
    #sys.exit(app.exec_()) 


