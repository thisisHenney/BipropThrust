from pathlib import Path
from common.app_data import app_data
from common.case_data import case_data


class RunView:
    def __init__(self, parent):
        self.parent = parent
        self.ui = self.parent.ui
        self.ctx = self.parent.ctx
        self.exec = self.ctx.get("exec")
        self.vtk1 = self.ctx.get("vtk1")

        self.app_data = app_data
        self.case_data = case_data

        self._init_connect()

    def _init_connect(self):
        ...