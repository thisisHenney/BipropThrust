from PySide6.QtWidgets import QWidget
from nextlib.widgets.tree import TreeWidget
# from nextlib.vtk.tool.point_probe_tool import PointProbeTool
from view.main.center_form_ui import Ui_Center
from view.panel.geometry_view import GeometryView
from view.panel.mesh_generation_view import MeshGenerationView


class CenterWidget(QWidget):
    def __init__(self, parent=None, context=None):
        super().__init__(parent)
        self.ctx = context
        self.parent = parent
        self.foam_data = self.parent.foam_data

        self.exec = self.ctx.get("exec")
        self.vtk1 = self.ctx.get("vtk1")
        self.vtk2 = self.ctx.get("vtk2")
        self.dock = self.ctx.get("dock")

        self.ui = Ui_Center()
        self.ui.setupUi(self)

        self.tree = TreeWidget(self.parent, self.ui.treeWidget)

        self.geometry_view = GeometryView(self)
        self.mesh_generation_view = MeshGenerationView(self)

        # self.point_tool = PointProbeTool(self.parent, self.vtk1)
        # def on_box_center(x, y, z):
        #     print("box center:", x, y, z)
        # self.point_tool.center_moved.connect(self.on_box_center)
        # self.point_tool.show()

        # self.ui.buttonRun.clicked.connect(self._clicked_button_run)

    def init(self):
        self.tree.itemSelectedWithPos.connect(self._changed_selection_item)
        self.tree.widget.expandAll()

    def _changed_selection_item(self, pos, col):
        if pos[0] == 0:
            self.ui.stackedWidget.setCurrentIndex(0)
        elif pos[0] == 1:
            self.ui.stackedWidget.setCurrentIndex(1)
        elif pos[0] == 2 and len(pos) == 2:
            self.ui.stackedWidget.setCurrentIndex(2 + int(pos[1]))
        elif pos[0] == 3 and len(pos) == 2:
            self.ui.stackedWidget.setCurrentIndex(6 + int(pos[1]))
        elif pos[0] == 4:
            self.ui.stackedWidget.setCurrentIndex(8)
        elif pos[0] == 5 and len(pos) == 2:
            if pos[1] == 0:
                self.ctx.dock.change_dock_tab(0)
            elif pos[1] == 1:
                self.ctx.dock.change_dock_tab(3)

    def _clicked_button_run(self):
        cmd = './Allrun'
        self.exec.run(cmd)
