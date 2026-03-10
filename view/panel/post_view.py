
from pathlib import Path

from common.case_data import case_data


class PostView:

    def __init__(self, parent):
        self.parent = parent

        # Get VTK post widget from parent (CenterWidget has vtk_post from context)
        self.vtk_post = parent.vtk_post

        # Get case data
        self.case_data = case_data

        # Track if results are loaded
        self._results_loaded = False

        # 케이스 경로 등록 (Refresh 버튼용)
        self._register_case_path()

    def _register_case_path(self):
        if not self.vtk_post or not self.case_data.path:
            return
        chtf_case = Path(self.case_data.path) / "5.CHTFCase"
        self.vtk_post.set_case_path(str(chtf_case))

    def load_results(self) -> bool:
        if not self.vtk_post:
            return False

        if not self.case_data.path:
            return False

        # Check if 5.CHTFCase folder exists
        chtf_case = Path(self.case_data.path) / "5.CHTFCase"

        if not chtf_case.exists():
            return False

        # Check for result time folders (numeric folders like 0.001, 0.002, etc.)
        has_results = False
        time_folders = []
        for item in chtf_case.iterdir():
            if item.is_dir():
                try:
                    float(item.name)
                    time_folders.append(item.name)
                    has_results = True
                except ValueError:
                    continue

        if not has_results:
            return False

        # 케이스 경로 등록 (Refresh 버튼에서 이 경로로 새로고침)
        self.vtk_post.set_case_path(str(chtf_case))

        # Load OpenFOAM case into vtk_post (직접 케이스 폴더 경로 전달)
        self.vtk_post.load_foam_file(str(chtf_case))

        # Configure slice view (Z=0 plane)
        self._configure_slice()

        # Field selection - commented out, let user select from combo box
        # self._select_temperature_field()
        # self._select_pressure_field()

        # Show scalar bar
        self._show_scalar_bar()

        # 카메라 뷰: Y축 위, X축 오른쪽, +Z가 화면 앞방향 (-Z가 모니터 뒷방향)
        # fit_to_scene()이 ResetCamera를 호출하므로, 그 이후에 카메라를 직접 재설정
        try:
            renderer = self.vtk_post.renderer
            camera = renderer.GetActiveCamera()
            fp = camera.GetFocalPoint()
            dist = camera.GetDistance()
            # +Z 방향에서 바라보기: Y가 위, X가 오른쪽
            camera.SetPosition(fp[0], fp[1], fp[2] + dist)
            camera.SetViewUp(0.0, 1.0, 0.0)
            camera.SetFocalPoint(fp)
            renderer.ResetCameraClippingRange()
            self.vtk_post.vtk_widget.GetRenderWindow().Render()
        except Exception:
            pass

        self._results_loaded = True
        return True

    def _configure_slice(self) -> None:
        if not self.vtk_post:
            return

        # Enable slice mode
        self.vtk_post.slice_check.setChecked(True)

        # Set axis to Z
        self.vtk_post.axis_combo.setCurrentText("Z")

        # Set position to 0
        self.vtk_post.slice_pos = 0.0
        self.vtk_post._update_slider_position()

    def _select_temperature_field(self) -> None:
        if not self.vtk_post:
            return

        # Find and select T field
        idx = self.vtk_post.field_combo.findText("T")
        if idx >= 0:
            self.vtk_post.field_combo.setCurrentIndex(idx)

    def _select_pressure_field(self) -> None:
        if not self.vtk_post:
            return

        # Find and select p field
        idx = self.vtk_post.field_combo.findText("p")
        if idx >= 0:
            self.vtk_post.field_combo.setCurrentIndex(idx)

    def _show_scalar_bar(self) -> None:
        if not self.vtk_post:
            return

        # Enable scalar bar
        if not self.vtk_post.scalar_bar_visible:
            self.vtk_post._scalar_bar_action.setChecked(True)
            self.vtk_post._on_scalar_bar_toggled(True)

    def is_loaded(self) -> bool:
        return self._results_loaded

    def reload_results(self) -> bool:
        self._results_loaded = False
        return self.load_results()
