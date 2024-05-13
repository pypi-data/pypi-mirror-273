import os
import subprocess as subproc
from pyshared.python import default_repr as def_repr
from typing import Union as U, List, Dict, Optional as Opt, Tuple
from logfunc import logf

from .log import logger as log
from .shell import CmdExec, CmdResult


class GitCmds:
    def __init__(self, repo_path: str):
        os.chdir(repo_path)
        self.repo_path = repo_path

        self.branch = CmdExec('git rev-parse --abbrev-ref HEAD').result.output
        self.remote_name = CmdExec(
            'git config --get branch.{}.remote'.format(self.branch)
        ).result.output
        self.remote_branch = CmdExec(
            'git config --get branch.{}.merge'.format(self.branch)
        ).result.output.split('/')[-1]

        self.remote_ref = 'refs/remotes/{}/{}'.format(
            self.remote_name, self.remote_branch
        )
        self.remote = CmdExec(
            'git rev-parse {}'.format(self.remote_ref)
        ).result

        self.local = CmdExec('git rev-parse HEAD').result

        self.fetch = CmdExec('git fetch')
        self.success = (
            self.fetch.result.code == 0
            and self.remote.code == 0
            and self.local.code == 0
        )

        self.changed = self.local.output != self.remote.output

    def __repr__(self):
        return def_repr(self)

    def __str__(self):
        return self.__repr__()
