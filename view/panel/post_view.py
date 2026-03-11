"""
Post 결과 뷰 – ParaView 매크로(macro_temperature.py / macro_pressure.py)와 동일한 시각화

레이어 구성:
  1. fluid 내부 격자의 Z=0 슬라이스 → 선택 필드(T / p)로 채색
  2. Lagrangian 스프레이 입자(sprayMMHCloud + sprayNTOCloud) → 점 표현, 'd'(직경)로 채색
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import vtk
from PySide6.QtCore import QObject, QThread, Signal

from common.case_data import case_data


class _SprayWorker(QObject):
    """Lagrangian 입자 데이터 추출을 백그라운드에서 실행하는 Worker.

    append.Update()는 데이터 처리만 하므로 스레드 안전합니다.
    추출 결과(vtkUnstructuredGrid + d_range)를 시그널로 전달하면
    메인 스레드에서 mapper/actor를 생성해 렌더러에 추가합니다.
    """
    finished = Signal(object, tuple)  # (ug | None, d_range | ())

    def __init__(self, reader, parent=None):
        super().__init__(parent)
        self._reader = reader

    def run(self):
        try:
            from vtkmodules.vtkFiltersCore import vtkAppendFilter
            mb = self._reader.GetOutput()
            if mb is None:
                self.finished.emit(None, ())
                return

            append = vtkAppendFilter()
            append.MergePointsOff()
            count = 0

            def _block_name(parent_obj, idx):
                try:
                    meta = parent_obj.GetMetaData(idx)
                    key = vtk.vtkCompositeDataSet.NAME()
                    if meta and meta.Has(key):
                        return meta.Get(key)
                except Exception:
                    pass
                return ''

            def _collect(data_obj, parent_obj=None, idx=0):
                nonlocal count
                if data_obj is None:
                    return
                name = _block_name(parent_obj, idx) if parent_obj is not None else ''
                if 'Tracks' in name:
                    return
                if not hasattr(data_obj, 'GetNumberOfBlocks'):
                    if (hasattr(data_obj, 'GetPointData') and
                            hasattr(data_obj, 'GetNumberOfPoints') and
                            data_obj.GetNumberOfPoints() > 0):
                        try:
                            if data_obj.GetPointData().HasArray('d'):
                                append.AddInputData(data_obj)
                                count += 1
                        except Exception:
                            pass
                    return
                for i in range(data_obj.GetNumberOfBlocks()):
                    _collect(data_obj.GetBlock(i), data_obj, i)

            _collect(mb)

            if count == 0:
                self.finished.emit(None, ())
                return

            append.Update()
            ug = append.GetOutput()
            if ug is None or ug.GetNumberOfPoints() == 0:
                self.finished.emit(None, ())
                return

            arr = ug.GetPointData().GetArray('d')
            if arr is None:
                self.finished.emit(None, ())
                return

            self.finished.emit(ug, arr.GetRange())

        except Exception:
            self.finished.emit(None, ())


class PostView:

    def __init__(self, parent):
        self.parent = parent
        self.vtk_post = parent.vtk_post
        self.case_data = case_data
        self._results_loaded = False
        self._spray_actor: Optional[vtk.vtkActor] = None
        self._spray_thread = None
        self._spray_worker = None

        # 케이스 로드 완료 시그널 연결 (로드 후 오버레이·카메라 설정)
        if self.vtk_post:
            self.vtk_post.case_loaded.connect(self._on_case_loaded)

    # ------------------------------------------------------------------
    # 공개 API
    # ------------------------------------------------------------------

    def load_results(self) -> bool:
        if not self.vtk_post:
            return False
        if not self.case_data.path:
            return False

        foam_file = self._find_foam_file(Path(self.case_data.path))
        if foam_file is None:
            return False

        self.vtk_post.set_case_path(str(foam_file.parent))
        self.vtk_post.load_foam(str(foam_file))
        return True

    def is_loaded(self) -> bool:
        return self._results_loaded

    def reload_results(self) -> bool:
        self._results_loaded = False
        if self._spray_actor:
            self.vtk_post.clear_overlay_actors()
            self._spray_actor = None
        return self.load_results()

    # ------------------------------------------------------------------
    # 내부 메서드
    # ------------------------------------------------------------------

    def _find_foam_file(self, case_path: Path) -> Optional[Path]:
        """케이스 폴더 안에서 *.foam 파일 탐색 (직접 경로 → 서브폴더 순)."""
        # 1) 직접 경로에 .foam 파일
        foams = list(case_path.glob("*.foam"))
        if foams:
            return foams[0]

        # 2) 공통 서브폴더 이름들 시도
        for sub in ["5.CHTFCase", "CHTFCase", "fluid", "run"]:
            sub_path = case_path / sub
            foams = list(sub_path.glob("*.foam")) if sub_path.is_dir() else []
            if foams:
                return foams[0]

        # 3) 첫 번째 수준 서브폴더 전체 탐색
        for child in case_path.iterdir():
            if child.is_dir():
                foams = list(child.glob("*.foam"))
                if foams:
                    return foams[0]

        return None

    def _on_case_loaded(self, case_path_str: str):
        """PostprocessWidget이 케이스 로드를 완료하면 호출."""
        # 슬라이스 설정 (Z=0)
        self._configure_slice()

        # 기본 필드: T (없으면 첫 번째 필드)
        self._select_default_field()

        # Lagrangian 스프레이 입자 오버레이 추가
        self._add_spray_overlay()

        # 스칼라 바 활성화
        self._ensure_scalar_bar()

        # 카메라 – +Z 방향에서 내려다보기 (Z=0 슬라이스 정면)
        self._set_camera_top_z()

        self._results_loaded = True

    def _configure_slice(self):
        vp = self.vtk_post
        if not vp:
            return
        # 슬라이스 체크 ON
        vp.slice_check.setChecked(True)
        # 축 Z
        vp.axis_combo.setCurrentText("Z")
        # 위치 0 (Z=0 평면)
        vp.slice_pos = 0.0
        vp._update_slider_position()
        vp._on_slice_toggled(True)

    def _select_default_field(self):
        vp = self.vtk_post
        if not vp:
            return
        # T 우선, 없으면 p, 없으면 첫 번째
        for preferred in ("T", "p"):
            idx = vp.field_combo.findText(preferred)
            if idx >= 0:
                vp.field_combo.setCurrentIndex(idx)
                return
        if vp.field_combo.count() > 0:
            vp.field_combo.setCurrentIndex(0)

    def _add_spray_overlay(self):
        """Lagrangian 파티클 추출을 백그라운드 스레드에서 실행.

        append.Update()만 스레드에서 처리하고,
        mapper/actor 생성 및 renderer 추가는 _on_spray_ready() 콜백(메인 스레드)에서 수행.
        """
        vp = self.vtk_post
        if not vp or not vp.reader:
            return

        self._spray_worker = _SprayWorker(vp.reader)
        self._spray_thread = QThread()
        self._spray_worker.moveToThread(self._spray_thread)

        self._spray_thread.started.connect(self._spray_worker.run)
        self._spray_worker.finished.connect(self._on_spray_ready)
        self._spray_worker.finished.connect(self._spray_thread.quit)
        self._spray_thread.finished.connect(self._spray_thread.deleteLater)

        self._spray_thread.start()

    def _on_spray_ready(self, ug, d_range: tuple):
        """스프레이 데이터 추출 완료 → 메인 스레드에서 actor 생성 및 추가."""
        self._spray_worker = None
        self._spray_thread = None

        if ug is None or not d_range:
            return

        vp = self.vtk_post
        if not vp:
            return

        # Blue → Red LUT (파라뷰 Cool-to-Warm 방향)
        lut = vtk.vtkLookupTable()
        lut.SetNumberOfTableValues(256)
        lut.SetRange(d_range)
        lut.SetHueRange(0.667, 0.0)
        lut.SetSaturationRange(1.0, 1.0)
        lut.SetValueRange(1.0, 1.0)
        lut.Build()

        # vtkDataSetMapper: vtkPolyData/vtkUnstructuredGrid 무관하게 동작
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(ug)
        mapper.SetScalarVisibility(True)
        mapper.SelectColorArray('d')
        mapper.SetColorModeToMapScalars()
        mapper.SetScalarModeToUsePointFieldData()
        mapper.SetScalarRange(d_range)
        mapper.SetLookupTable(lut)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetRepresentationToPoints()
        actor.GetProperty().SetPointSize(3)

        self._spray_actor = actor
        vp.add_overlay_actor(actor)
        vp._render()

    def _ensure_scalar_bar(self):
        vp = self.vtk_post
        if not vp:
            return
        if not vp.scalar_bar_visible:
            vp._scalar_bar_action.setChecked(True)
            vp._on_scalar_bar_toggled(True)

    def _set_camera_top_z(self):
        """카메라를 +Z 방향에서 -Z를 바라보도록 설정 (Z=0 슬라이스 정면)."""
        vp = self.vtk_post
        if not vp:
            return
        try:
            renderer = vp.renderer
            renderer.ResetCamera()
            camera = renderer.GetActiveCamera()
            fp = camera.GetFocalPoint()
            dist = camera.GetDistance()
            # +Z 위치, focal point를 향해, Y가 위
            camera.SetPosition(fp[0], fp[1], fp[2] + dist)
            camera.SetViewUp(0.0, 1.0, 0.0)
            camera.SetFocalPoint(fp)
            renderer.ResetCameraClippingRange()
            vp.vtk_widget.GetRenderWindow().Render()
        except Exception:
            pass
