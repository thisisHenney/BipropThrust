from pathlib import Path

from nextlib.program.program import open_file_explorer
from nextlib.widgets.messagebox import messagebox
from nextlib.dialogbox.dialogbox import DirDialogBox

from common.case_data import case_data


class MainMenu():
    def __init__(self, parent):
        self.parent = parent
        self.ui = parent.ui

        self.case_data = case_data

    def init(self):
        ui = self.ui
        ui.actionNew.triggered.connect(self.on_menu_new)
        ui.actionOpen.triggered.connect(self.on_menu_open)
        ui.actionSave.triggered.connect(self.on_menu_save)
        ui.actionExit.triggered.connect(self.on_menu_exit)
        ui.actionRun.triggered.connect(self.on_menu_run)

        ui.actionMesh.triggered.connect(self.on_menu_mesh)
        ui.actionResidual.triggered.connect(self.on_menu_residual)

        ui.actionFileExplorer.triggered.connect(self.on_menu_file_explorer)
        ui.actionTerminal.triggered.connect(self.on_menu_terminal)

        ui.actionAbout.triggered.connect(self.on_menu_about)

    def on_menu_new(self):
        print('on_menu_new')

    def on_menu_open(self):
        open_path = DirDialogBox.open_folder(
            parent=self.parent,
            title="Open OpenFOAM folder"
        )
        if open_path:
            self.parent.open_case(open_path)

    def on_menu_save(self):
        print('on_menu_save')

    def on_menu_exit(self):
        print('on_menu_exit')

    def on_menu_run(self):
        print('on_menu_run')

    def on_menu_mesh(self):
        print('on_menu_mesh')

    def on_menu_residual(self):
        print('on_menu_residual')

    def on_menu_file_explorer(self):
        open_file_explorer(self.parent, f"{self.case_data.path}")

    def on_menu_terminal(self):
        print('on_menu_terminal')
        # open_terminal()

    def on_menu_about(self):
        print('on_menu_about')
