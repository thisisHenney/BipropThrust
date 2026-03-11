from pathlib import Path

from PySide6.QtWidgets import QWidget, QGroupBox, QTreeWidget
from PySide6.QtCore import Qt

from common.app_context import AppContext
from common.case_data import case_data
from view.main.center_form_ui import Ui_Center
from view.main.step_nav_widget import StepNavWidget
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

        self.exec_widget    = context.get("exec")           if context else None
        self.vtk_pre        = context.get("vtk_pre")        if context else None
        self.vtk_post       = context.get("vtk_post")       if context else None
        self.residual_graph = context.get("residual_graph") if context else None
        self.dock_manager   = context.get("dock")           if context else None

        self.panel_views = {}

        self._setup_panels()
        self._setup_step_nav()
        self._connect_signals()

    # ──────────────────────────────────────────────────────────────
    # Setup
    # ──────────────────────────────────────────────────────────────

    def _setup_panels(self) -> None:
        self.panel_views["geometry"] = GeometryView(self)
        self.panel_views["mesh"]     = MeshGenerationView(self)
        self.panel_views["run"]      = RunView(self)
        self.panel_views["post"]     = PostView(self)

    def _setup_step_nav(self) -> None:
        # 기존 treeWidget 숨기기
        self.ui.treeWidget.hide()

        # StepNavWidget 생성 후 horizontalLayout 맨 앞에 삽입
        self.step_nav = StepNavWidget(self)
        self.ui.horizontalLayout.insertWidget(0, self.step_nav)

        self.step_nav.set_current("geometry")

    def _clear_designer_styles(self) -> None:
        for tree in self.findChildren(QTreeWidget):
            tree.setStyleSheet("")
        for gb in self.findChildren(QGroupBox):
            gb.setStyleSheet("")

    def _connect_signals(self) -> None:
        self.step_nav.step_clicked.connect(self._on_step_clicked)

    def select_default_tab(self) -> None:
        self._on_step_clicked("geometry")

    # ──────────────────────────────────────────────────────────────
    # Step navigation
    # ──────────────────────────────────────────────────────────────

    def _on_step_clicked(self, step_key: str) -> None:
        self.step_nav.set_current(step_key)

        if step_key == "geometry":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_geometry)
            self._on_tab_geometry()

        elif step_key == "mesh":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_mesh_generation)
            self._on_tab_mesh()

        elif step_key == "run":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_run)
            self._on_tab_run()

        elif step_key == "post":
            self._on_tab_post()

    # ──────────────────────────────────────────────────────────────
    # Tab 활성화 로직
    # ──────────────────────────────────────────────────────────────

    def _on_tab_geometry(self):
        if self.vtk_pre:
            self._show_geometry_objects()
            self._show_slice_toolbar("geometry")
            self.vtk_pre.set_visibility_mode("geometry")
            geo_view = self.panel_views.get("geometry")
            if geo_view and hasattr(geo_view, '_probe_marker_actor') and geo_view._probe_marker_actor:
                geo_view._probe_marker_actor.SetVisibility(True)
                self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _on_tab_mesh(self):
        if self.vtk_pre:
            self._show_mesh_objects()
            self._show_slice_toolbar("mesh")
            self.vtk_pre.set_visibility_mode("mesh")
            self._hide_probe_marker()

    def _on_tab_run(self):
        if self.dock_manager:
            self.dock_manager.change_dock_tab(4)  # Residual 그래프 독
        self._load_residual_log()
        if self.vtk_pre:
            self._show_mesh_objects()
            self._show_slice_toolbar("mesh")
            self.vtk_pre.set_visibility_mode("mesh")
            self._hide_probe_marker()

    def _on_tab_post(self):
        if self.dock_manager:
            self.dock_manager.change_dock_tab(3)  # Post VTK 독
        post_view = self.panel_views.get("post")
        if post_view and not getattr(post_view, '_results_loaded', False):
            post_view.load_results()
        if self.vtk_pre:
            self._show_mesh_objects()
            self._show_slice_toolbar("mesh")
            self.vtk_pre.set_visibility_mode("mesh")
            self._hide_probe_marker()

    def _hide_probe_marker(self):
        geo_view = self.panel_views.get("geometry")
        if geo_view and hasattr(geo_view, '_probe_marker_actor') and geo_view._probe_marker_actor:
            geo_view._probe_marker_actor.SetVisibility(False)
            if self.vtk_pre:
                self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    # ──────────────────────────────────────────────────────────────
    # VTK 가시성 헬퍼
    # ──────────────────────────────────────────────────────────────

    def _show_geometry_objects(self):
        all_objs = self.vtk_pre.obj_manager.get_all()
        renderer = self.vtk_pre.vtk_widget.GetRenderWindow().GetRenderers().GetFirstRenderer()

        for obj in all_objs:
            if hasattr(obj, 'group'):
                if obj.group == "geometry":
                    renderer.AddActor(obj.actor)
                    obj.actor.SetVisibility(True)
                elif obj.group == "mesh":
                    obj.actor.SetVisibility(False)

        mesh_view = self.panel_views.get("mesh")
        if mesh_view:
            mesh_view._hide_slice_clip_actors()

        self.vtk_pre.show_clip_actors_for_group("geometry")
        self.vtk_pre.hide_clip_actors_for_group("mesh")
        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _show_mesh_objects(self):
        all_objs = self.vtk_pre.obj_manager.get_all()

        for obj in all_objs:
            if hasattr(obj, 'group'):
                if obj.group == "geometry":
                    obj.actor.SetVisibility(False)
                elif obj.group == "mesh":
                    obj.actor.SetVisibility(True)

        mesh_view = self.panel_views.get("mesh")
        if mesh_view:
            mesh_view._show_slice_clip_actors()

        self.vtk_pre.hide_clip_actors_for_group("geometry")
        self.vtk_pre.show_clip_actors_for_group("mesh")
        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _show_slice_toolbar(self, mode: str = "mesh"):
        geometry_view = self.panel_views.get("geometry")
        mesh_view     = self.panel_views.get("mesh")

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

    # ──────────────────────────────────────────────────────────────
    # Residual 로그
    # ──────────────────────────────────────────────────────────────

    def _load_residual_log(self):
        if not self.residual_graph or not case_data.path:
            return

        chtf_case = Path(case_data.path) / "5.CHTFCase"
        log_file  = chtf_case / "log.Solver"
        if not log_file.exists():
            log_file = chtf_case / "log.solver"

        if log_file.exists():
            self.residual_graph.load_file(str(log_file), target_vars=['h', 'p', 'rho'])

    def get_panel(self, panel_id: str):
        return self.panel_views.get(panel_id)
