
from pathlib import Path

from PySide6.QtWidgets import QWidget, QGroupBox, QTreeWidget

from PySide6.QtCore import Qt

from common.app_context import AppContext

from common.case_data import case_data

from view.main.center_form_ui import Ui_Center

from view.panel.geometry_view import GeometryView

from view.panel.mesh_generation_view import MeshGenerationView

from view.panel.run_view import RunView

from view.panel.post_view import PostView

class CenterWidget(QWidget):

    def __init__(self, parent=None, context: AppContext = None):

        super().__init__(parent)

        self.main_window = parent

        self.context = context

        self.ui = Ui_Center()

        self.ui.setupUi(self)

        self._clear_designer_styles()

        self.exec_widget = context.get("exec") if context else None

        self.vtk_pre = context.get("vtk_pre") if context else None

        self.vtk_post = context.get("vtk_post") if context else None

        self.residual_graph = context.get("residual_graph") if context else None

        self.dock_manager = context.get("dock") if context else None

        self.panel_views = {}

        self._setup_panels()

        self._connect_signals()

    def _setup_panels(self) -> None:

        self.panel_views["geometry"] = GeometryView(self)

        self.panel_views["mesh"] = MeshGenerationView(self)

        self.panel_views["run"] = RunView(self)

        self.panel_views["post"] = PostView(self)

    def _clear_designer_styles(self) -> None:

        for tree in self.findChildren(QTreeWidget):

            tree.setStyleSheet("")

        for gb in self.findChildren(QGroupBox):

            gb.setStyleSheet("")

    def _connect_signals(self) -> None:

        self.ui.treeWidget.itemSelectionChanged.connect(self._on_tree_selection_changed)

        self.ui.treeWidget.itemClicked.connect(self._on_tree_item_clicked)

    def select_default_tab(self) -> None:

        geometry_item = self.ui.treeWidget.topLevelItem(0)

        if geometry_item:

            self.ui.treeWidget.setCurrentItem(geometry_item)

    def _on_tree_item_clicked(self, item, column) -> None:

        if item.childCount() > 0:

            self.ui.treeWidget.expandItem(item)

            first_child = item.child(0)

            self.ui.treeWidget.setCurrentItem(first_child)

    def _on_tree_selection_changed(self) -> None:

        selected_items = self.ui.treeWidget.selectedItems()

        if not selected_items:

            return

        item = selected_items[0]

        if item.childCount() > 0:

            self.ui.treeWidget.expandItem(item)

            return

        item_text = item.text(0)

        parent = item.parent()

        parent_text = parent.text(0) if parent else None

        page_map = {
            "Geometry": self.ui.page_geometry,
            "Mesh Generation": self.ui.page_mesh_generation,
            "Run": self.ui.page_run,
        }

        setup_pages = {
            "Models": self.ui.page_models,
            "Initial Conditions": self.ui.page_initial_conditions,
            "Spray - MMH": self.ui.page_mmh,
            "Spray - NTO": self.ui.page_nto,
        }

        solution_pages = {
            "Numerical Conditions": self.ui.page_numerical_conditions,
            "Run Conditions": self.ui.page_run_conditions,
        }

        page = None

        if parent_text:

            if parent_text == "Setup":

                page = setup_pages.get(item_text)

            elif parent_text == "Solution":

                page = solution_pages.get(item_text)

            elif parent_text == "Results":

                if item_text == "Residual":

                    if self.dock_manager:

                        self.dock_manager.change_dock_tab(4)

                    self._load_residual_log()

                elif item_text == "Post":

                    if self.dock_manager:

                        self.dock_manager.change_dock_tab(3)

                    post_view = self.panel_views.get("post")

                    if post_view and not getattr(post_view, '_results_loaded', False):

                        post_view.load_results()

                if self.vtk_pre:

                    self._show_mesh_objects()

                    self._show_slice_toolbar("mesh")

                    self.vtk_pre.set_visibility_mode("mesh")

                    geo_view = self.panel_views.get("geometry")

                    if geo_view and hasattr(geo_view, '_probe_marker_actors') and geo_view._probe_marker_actors:

                        for _m in geo_view._probe_marker_actors:

                            _m.SetVisibility(False)

                        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

                return

        else:

            page = page_map.get(item_text)

        if page:

            self.ui.stackedWidget.setCurrentWidget(page)

            from PySide6.QtWidgets import QApplication

            QApplication.processEvents()

            if self.vtk_pre:

                if item_text == "Geometry" and not parent_text:

                    self._show_geometry_objects()

                    self._show_slice_toolbar("geometry")

                    self.vtk_pre.set_visibility_mode("geometry")

                    geo_view = self.panel_views.get("geometry")

                    if geo_view and hasattr(geo_view, '_probe_marker_actors') and geo_view._probe_marker_actors:

                        for _m in geo_view._probe_marker_actors:

                            _m.SetVisibility(True)

                        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

                else:

                    self._show_mesh_objects()

                    self._show_slice_toolbar("mesh")

                    self.vtk_pre.set_visibility_mode("mesh")

                    geo_view = self.panel_views.get("geometry")

                    if geo_view and hasattr(geo_view, '_probe_marker_actors') and geo_view._probe_marker_actors:

                        for _m in geo_view._probe_marker_actors:

                            _m.SetVisibility(False)

                        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _show_geometry_objects(self):

        all_objs = self.vtk_pre.obj_manager.get_all()

        renderer = self.vtk_pre.vtk_widget.GetRenderWindow().GetRenderers().GetFirstRenderer()

        geom_count = 0

        mesh_count = 0

        for obj in all_objs:

            if hasattr(obj, 'group'):

                if obj.group == "geometry":

                    renderer.AddActor(obj.actor)

                    obj.actor.SetVisibility(True)

                    geom_count += 1

                elif obj.group == "mesh":

                    obj.actor.SetVisibility(False)

                    mesh_count += 1

        mesh_view = self.panel_views.get("mesh")

        if mesh_view:

            mesh_view._hide_slice_clip_actors()

        self.vtk_pre.show_clip_actors_for_group("geometry")

        self.vtk_pre.hide_clip_actors_for_group("mesh")

        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _show_mesh_objects(self):

        all_objs = self.vtk_pre.obj_manager.get_all()

        geom_count = 0

        mesh_count = 0

        for obj in all_objs:

            if hasattr(obj, 'group'):

                if obj.group == "geometry":

                    obj.actor.SetVisibility(False)

                    geom_count += 1

                elif obj.group == "mesh":

                    obj.actor.SetVisibility(True)

                    mesh_count += 1

        mesh_view = self.panel_views.get("mesh")

        if mesh_view:

            mesh_view._show_slice_clip_actors()

        self.vtk_pre.hide_clip_actors_for_group("geometry")

        self.vtk_pre.show_clip_actors_for_group("mesh")

        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _show_mesh_objects_only(self):

        all_objs = self.vtk_pre.obj_manager.get_all()

        geom_count = 0

        mesh_count = 0

        for obj in all_objs:

            if hasattr(obj, 'group'):

                if obj.group == "geometry":

                    obj.actor.SetVisibility(False)

                    geom_count += 1

                elif obj.group == "mesh":

                    obj.actor.SetVisibility(True)

                    mesh_count += 1

        mesh_view = self.panel_views.get("mesh")

        if mesh_view:

            mesh_view._hide_slice_clip_actors()

        self.vtk_pre.hide_clip_actors_for_group("geometry")

        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _show_slice_toolbar(self, mode: str = "mesh"):

        geometry_view = self.panel_views.get("geometry")

        mesh_view = self.panel_views.get("mesh")

        if mode == "geometry":

            if geometry_view and hasattr(geometry_view, "slice_widget") and geometry_view.slice_widget:

                geometry_view.slice_widget.show()

            if mesh_view and hasattr(mesh_view, "slice_widget") and mesh_view.slice_widget:

                mesh_view.slice_widget.hide()

        else:

            if mesh_view and hasattr(mesh_view, "slice_widget") and mesh_view.slice_widget:

                mesh_view.slice_widget.show()

            if geometry_view and hasattr(geometry_view, "slice_widget") and geometry_view.slice_widget:

                geometry_view.slice_widget.hide()

    def _hide_slice_toolbar(self):

        geometry_view = self.panel_views.get("geometry")

        mesh_view = self.panel_views.get("mesh")

        if geometry_view and hasattr(geometry_view, "slice_widget") and geometry_view.slice_widget:

            geometry_view.slice_widget.hide()

        if mesh_view and hasattr(mesh_view, "slice_widget") and mesh_view.slice_widget:

            mesh_view.slice_widget.hide()

    def _load_residual_log(self):

        if not self.residual_graph:

            return

        if not case_data.path:

            return

        chtf_case = Path(case_data.path) / "5.CHTFCase"

        log_file = chtf_case / "log.Solver"

        if not log_file.exists():

            log_file = chtf_case / "log.solver"

        if log_file.exists():

            self.residual_graph.load_file(str(log_file), target_vars=['h', 'p', 'rho'])

    def get_panel(self, panel_id: str):

        return self.panel_views.get(panel_id)

