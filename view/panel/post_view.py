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

from common.case_data import case_data

class PostView:

    def __init__(self, parent):

        self.parent = parent

        self.vtk_post = parent.vtk_post

        self.case_data = case_data

        self._results_loaded = False

        self._spray_actor: Optional[vtk.vtkActor] = None

        if self.vtk_post:

            self.vtk_post.case_loaded.connect(self._on_case_loaded)

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

    def _find_foam_file(self, case_path: Path) -> Optional[Path]:

        """케이스 폴더 안에서 *.foam 파일 탐색 (직접 경로 → 서브폴더 순)."""

        foams = list(case_path.glob("*.foam"))

        if foams:

            return foams[0]

        for sub in ["5.CHTFCase", "CHTFCase", "fluid", "run"]:

            sub_path = case_path / sub

            foams = list(sub_path.glob("*.foam")) if sub_path.is_dir() else []

            if foams:

                return foams[0]

        for child in case_path.iterdir():

            if child.is_dir():

                foams = list(child.glob("*.foam"))

                if foams:

                    return foams[0]

        return None

    def _on_case_loaded(self, case_path_str: str):

        """PostprocessWidget이 케이스 로드를 완료하면 호출."""

        self._configure_slice()

        self._select_default_field()

        self._add_spray_overlay()

        self._ensure_scalar_bar()

        self._set_camera_top_z()

        self._results_loaded = True

    def _configure_slice(self):

        vp = self.vtk_post

        if not vp:

            return

        vp.slice_check.setChecked(True)

        vp.axis_combo.setCurrentText("Z")

        vp.slice_pos = 0.0

        vp._update_slider_position()

        vp._on_slice_toggled(True)

    def _select_default_field(self):

        vp = self.vtk_post

        if not vp:

            return

        for preferred in ("T", "p"):

            idx = vp.field_combo.findText(preferred)

            if idx >= 0:

                vp.field_combo.setCurrentIndex(idx)

                return

        if vp.field_combo.count() > 0:

            vp.field_combo.setCurrentIndex(0)

    def _add_spray_overlay(self):
        """Lagrangian 파티클 추출 및 오버레이 추가 (동기, 메인 스레드).

        VTK는 스레드 안전하지 않으므로 모든 VTK 작업은 메인 스레드에서 실행.
        835개 파티클 extract는 수ms로 충분히 빠름.
        """
        vp = self.vtk_post
        if not vp or not vp.reader:
            return

        mb = vp.reader.GetOutput()
        if mb is None:
            return

        from vtkmodules.vtkFiltersCore import vtkAppendFilter
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
            return

        append.Update()
        ug = append.GetOutput()
        if ug is None or ug.GetNumberOfPoints() == 0:
            return

        arr = ug.GetPointData().GetArray('d')
        if arr is None:
            return

        self._on_spray_ready(ug, arr.GetRange())

    def _on_spray_ready(self, ug, d_range: tuple):

        """스프레이 데이터 추출 완료 → 메인 스레드에서 actor 생성 및 추가."""

        self._spray_worker = None

        self._spray_thread = None

        if ug is None or not d_range:

            return

        vp = self.vtk_post

        if not vp:

            return

        lut = vtk.vtkLookupTable()

        lut.SetNumberOfTableValues(256)

        lut.SetRange(d_range)

        lut.SetHueRange(0.667, 0.0)

        lut.SetSaturationRange(1.0, 1.0)

        lut.SetValueRange(1.0, 1.0)

        lut.Build()

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

            camera.SetPosition(fp[0], fp[1], fp[2] + dist)

            camera.SetViewUp(0.0, 1.0, 0.0)

            camera.SetFocalPoint(fp)

            renderer.ResetCameraClippingRange()

            vp.vtk_widget.GetRenderWindow().Render()

        except Exception:

            pass

