from pathlib import Path
from common.app_data import app_data
from common.case_data import case_data


class MeshGenerationView:
    def __init__(self, parent):
        self.parent = parent
        self.ui = self.parent.ui
        self.ctx = self.parent.ctx
        self.exec = self.ctx.get("exec")
        self.vtk1 = self.ctx.get("vtk1")

        self.app_data = app_data
        self.case_data = case_data

        self.foam_data = self.parent.foam_data

        self._init_connect()

    def _init_connect(self):
        self.ui.button_mesh_generate.clicked.connect(self.clicked_btn_mesh_generate)


    def clicked_btn_mesh_generate(self):
        x, y, z = (
            self.ui.lineEdit_basegrid_x.text(),
            self.ui.lineEdit_basegrid_y.text(),
            self.ui.lineEdit_basegrid_z.text()
        )

        filedata = self.foam_data.file('blockMeshDict')
        print(filedata)
        # result = filedata.get_value('blocks.hex')
        # print(result)


