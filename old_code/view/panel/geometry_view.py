from pathlib import Path
from PySide6.QtWidgets import QFileDialog
from nextlib.dialogbox.dialogbox import FileDialogBox
from nextlib.widgets.tree import TreeWidget
from common.app_data import app_data
from common.case_data import case_data


class GeometryView:
    def __init__(self, parent):
        self.parent = parent
        self.ui = self.parent.ui
        self.ctx = self.parent.ctx
        self.exec = self.ctx.get("exec")
        self.vtk1 = self.ctx.get("vtk1")

        self.app_data = app_data
        self.case_data = case_data

        self.tree = TreeWidget(self.parent, self.ui.tree_geometry)

        self._init_connect()

    def _init_connect(self):
        self.ui.button_geometry_add.clicked.connect(self.clicked_btn_add)
        self.ui.button_geometry_remove.clicked.connect(self.clicked_btn_remove)

        self.tree.widget.header().setVisible(False)
        self.tree.itemSelectedWithPos.connect(self._changed_selection_item)

    def _changed_selection_item(self, pos):
        self.tree.get_item(pos)

    def clicked_btn_add(self):
        add_files = FileDialogBox.open_files(
            self.parent, "Select STL files",
            "STL Files (*.stl);;All Files (*)", self.case_data.path)
        if not add_files:
            return

        for f in add_files:
            file = Path(f)
            self.case_data.add_geometry(file)
            name = file.stem
            self.tree.insert([], name)

            actor = self.vtk1.mesh_loader.load_stl(file)
            self.vtk1.obj_manager.add(actor, 0, name)

        self.case_data.save()

    def clicked_btn_remove(self):
        pos = self.tree.get_current_pos()
        obj_name = self.tree.get_text(pos)

        self.tree.remove_item(pos)

        obj_id = self.vtk1.obj_manager.get_id_by_name(obj_name)
        self.vtk1.obj_manager.remove(obj_id)
        self.case_data.remove_geometry(obj_name)

        self.case_data.save()
