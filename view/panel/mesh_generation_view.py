"""
Mesh Generation View - Handles mesh generation logic

This view connects to UI widgets defined in center_form_ui.py
and implements OpenFOAM mesh generation functionality.
"""

import sys
import subprocess
import math
import re
from pathlib import Path

import vtk
from PySide6.QtCore import QThread, Qt
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSlider,
    QCheckBox,
    QDoubleSpinBox,
)

from nextlib.openfoam.PyFoamCase.foamfile import FoamFile

from common.app_data import app_data
from common.case_data import case_data


class MeshGenerationView:
    """
    Mesh generation view.

    Manages blockMeshDict and mesh generation process.
    """

    def __init__(self, parent):
        """
        Initialize mesh generation view.

        Args:
            parent: CenterWidget instance (contains ui and context)
        """
        self.parent = parent
        self.ui = self.parent.ui
        self.ctx = self.parent.context

        # Get services from context
        self.exec_widget = self.ctx.get("exec")
        self.vtk_pre = self.ctx.get("vtk_pre")

        # Get data instances
        self.app_data = app_data
        self.case_data = case_data

        # VTK pipeline objects for OpenFOAM mesh and slice
        self.foam_reader = None
        self.geom_output = None  # Full surface polydata
        self.bounds = None  # (xmin, xmax, ymin, ymax, zmin, zmax)
        self.center = None  # (cx, cy, cz)
        self.diagonal_length = None
        self.surface_actor = None

        # Slice pipeline objects
        self.slice_plane = None
        self.slice_actor = None
        self.clip_actor = None
        self.clip_filter = None

        # Create slice controls widget (will be shown/hidden by center_widget)
        self.slice_widget = self._create_slice_widget()

        # Connect signals
        self._init_connect()

    def _init_connect(self):
        """Initialize signal connections."""
        self.ui.button_mesh_generate.clicked.connect(self._on_generate_clicked)
        self.ui.button_edit_hostfile_mesh.clicked.connect(self._on_edit_hostfile_clicked)

        # Slice toolbar signals
        self.combo_dir.currentIndexChanged.connect(self.update_slice)
        self.slider_pos.valueChanged.connect(self._on_slider_changed)
        self.chk_clip.toggled.connect(self.update_slice)
        self.spin_nx.valueChanged.connect(self.update_slice)
        self.spin_ny.valueChanged.connect(self.update_slice)
        self.spin_nz.valueChanged.connect(self.update_slice)

    def _create_slice_widget(self):
        """
        Create slice controls as a separate widget to be added below VTK viewer.

        Returns:
            QWidget containing slice controls
        """
        if not self.vtk_pre:
            return None

        # Create container widget
        slice_widget = QWidget()
        layout = QHBoxLayout(slice_widget)
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(6)

        # Direction selection
        lbl_dir = QLabel("Slice:")
        layout.addWidget(lbl_dir)

        self.combo_dir = QComboBox()
        self.combo_dir.addItems(["X", "Y", "Z", "Custom"])
        layout.addWidget(self.combo_dir)

        # Custom normal controls
        lbl_n = QLabel(" n=(")
        layout.addWidget(lbl_n)

        self.spin_nx = QDoubleSpinBox()
        self.spin_nx.setRange(-1.0, 1.0)
        self.spin_nx.setSingleStep(0.1)
        self.spin_nx.setValue(0.0)
        self.spin_nx.setMaximumWidth(60)
        layout.addWidget(self.spin_nx)

        lbl_comma1 = QLabel(",")
        layout.addWidget(lbl_comma1)

        self.spin_ny = QDoubleSpinBox()
        self.spin_ny.setRange(-1.0, 1.0)
        self.spin_ny.setSingleStep(0.1)
        self.spin_ny.setValue(0.0)
        self.spin_ny.setMaximumWidth(60)
        layout.addWidget(self.spin_ny)

        lbl_comma2 = QLabel(",")
        layout.addWidget(lbl_comma2)

        self.spin_nz = QDoubleSpinBox()
        self.spin_nz.setRange(-1.0, 1.0)
        self.spin_nz.setSingleStep(0.1)
        self.spin_nz.setValue(1.0)
        self.spin_nz.setMaximumWidth(60)
        layout.addWidget(self.spin_nz)

        lbl_close = QLabel(")")
        layout.addWidget(lbl_close)

        # Position slider
        lbl_pos = QLabel(" Pos:")
        layout.addWidget(lbl_pos)

        self.slider_pos = QSlider(Qt.Horizontal)
        self.slider_pos.setRange(0, 100)
        self.slider_pos.setValue(50)
        self.slider_pos.setMinimumWidth(200)
        layout.addWidget(self.slider_pos)

        self.lbl_pos_value = QLabel("50%")
        self.lbl_pos_value.setMinimumWidth(40)
        layout.addWidget(self.lbl_pos_value)

        # Clip checkbox
        self.chk_clip = QCheckBox("Clip")
        self.chk_clip.setChecked(False)
        layout.addWidget(self.chk_clip)

        # Add spacer to push controls to the left
        layout.addStretch()

        # Hide widget initially
        slice_widget.hide()

        # Add to VTK widget layout (below vtk_widget, above status bar if exists)
        vtk_layout = self.vtk_pre.layout()
        # vtk_layout has: toolbar (index 0), vtk_widget (index 1)
        # Insert slice widget after vtk_widget
        vtk_layout.addWidget(slice_widget)

        return slice_widget

    def _on_edit_hostfile_clicked(self):
        """Handle Edit host file button click - open hosts file in text editor."""
        # Path to hosts file in 2.meshing_MheadBL/system/
        hosts_path = Path(self.case_data.path) / "2.meshing_MheadBL" / "system" / "hosts"

        if not hosts_path.exists():
            print(f"Hosts file not found: {hosts_path}")
            # Create empty hosts file if it doesn't exist
            hosts_path.parent.mkdir(parents=True, exist_ok=True)
            hosts_path.touch()
            print(f"Created hosts file: {hosts_path}")

        # Open with appropriate text editor based on platform
        try:
            if sys.platform == "win32":
                # Windows - use notepad
                subprocess.Popen(["notepad", str(hosts_path)])
                print(f"Opening hosts file with notepad: {hosts_path}")
            else:
                # Linux - use gedit
                subprocess.Popen(["gedit", str(hosts_path)])
                print(f"Opening hosts file with gedit: {hosts_path}")
        except Exception as e:
            print(f"Error opening hosts file: {e}")
            import traceback
            traceback.print_exc()

    def _on_generate_clicked(self):
        """Handle Generate button click - update blockMeshDict and load existing mesh."""
        # Disable button during execution
        self.ui.button_mesh_generate.setEnabled(False)

        # Get base grid values
        x = self.ui.lineEdit_basegrid_x.text() or "100"
        y = self.ui.lineEdit_basegrid_y.text() or "100"
        z = self.ui.lineEdit_basegrid_z.text() or "100"

        print(f"Loading mesh with base grid: ({x}, {y}, {z})")

        # Update blockMeshDict with geometry bounding box and base grid
        if not self._update_blockmesh_dict(x, y, z):
            print("Failed to update blockMeshDict")
            self.ui.button_mesh_generate.setEnabled(True)
            return

        # Update snappyHexMeshDict with locationsInMesh from geometry probe positions
        if not self._update_snappyhex_dict():
            print("Failed to update snappyHexMeshDict")
            self.ui.button_mesh_generate.setEnabled(True)
            return

        # Load existing mesh directly (skip Allrun execution for now)
        print("Loading existing mesh from VTK folder...")
        self._on_mesh_generated()
        self._restore_ui()

        # # TODO: Uncomment below to run actual mesh generation
        # # Set working directory to case path
        # if self.exec_widget:
        #     self.exec_widget.set_working_path(str(self.case_data.path))
        #
        #     # Register callbacks
        #     self.exec_widget.set_function_after_finished(self._on_mesh_generated)
        #     self.exec_widget.set_function_restore_ui(self._restore_ui)
        #
        #     # Define mesh generation commands - run Allrun script
        #     if sys.platform == "win32":
        #         # Windows - use bash to run Allrun
        #         commands = [
        #             "cd 2.meshing_MheadBL",
        #             "bash Allrun",
        #             "foamToVTK",
        #             "cd .."
        #         ]
        #     else:
        #         # Linux - run Allrun directly
        #         commands = [
        #             "cd 2.meshing_MheadBL",
        #             "./Allrun",
        #             "foamToVTK",
        #             "cd .."
        #         ]
        #
        #     # Run mesh generation commands
        #     self.exec_widget.run(commands)
        # else:
        #     print("ExecWidget not available")
        #     self.ui.button_mesh_generate.setEnabled(True)

    def _restore_ui(self):
        """Restore UI state after command execution (success, error, or cancel)."""
        self.ui.button_mesh_generate.setEnabled(True)

    def _update_blockmesh_dict(self, cells_x: str, cells_y: str, cells_z: str) -> bool:
        """
        Update blockMeshDict with geometry bounding box vertices and base grid cells.

        Args:
            cells_x: Number of cells in x direction
            cells_y: Number of cells in y direction
            cells_z: Number of cells in z direction

        Returns:
            True if successful, False otherwise
        """
        if not self.vtk_pre:
            print("VTK widget not available")
            return False

        # Get all geometry objects
        all_objs = self.vtk_pre.obj_manager.get_all()
        geom_objects = [obj for obj in all_objs if hasattr(obj, 'group') and obj.group == "geometry"]

        if not geom_objects:
            print("No geometry objects found")
            return False

        # Calculate overall bounding box
        bounds = [float('inf'), float('-inf'),
                  float('inf'), float('-inf'),
                  float('inf'), float('-inf')]

        for obj in geom_objects:
            obj_bounds = obj.actor.GetBounds()
            bounds[0] = min(bounds[0], obj_bounds[0])  # xmin
            bounds[1] = max(bounds[1], obj_bounds[1])  # xmax
            bounds[2] = min(bounds[2], obj_bounds[2])  # ymin
            bounds[3] = max(bounds[3], obj_bounds[3])  # ymax
            bounds[4] = min(bounds[4], obj_bounds[4])  # zmin
            bounds[5] = max(bounds[5], obj_bounds[5])  # zmax

        xmin, xmax, ymin, ymax, zmin, zmax = bounds
        print(f"Geometry bounding box: ({xmin:.4f}, {ymin:.4f}, {zmin:.4f}) to ({xmax:.4f}, {ymax:.4f}, {zmax:.4f})")

        # Update blockMeshDict
        try:
            # Path to blockMeshDict (always in 2.meshing_MheadBL subfolder)
            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"
            blockmesh_path = case_path / "system" / "blockMeshDict"

            if not blockmesh_path.exists():
                print(f"blockMeshDict not found: {blockmesh_path}")
                return False

            # Load blockMeshDict using FoamFile
            foam_file = FoamFile(str(blockmesh_path))
            if not foam_file.load():
                print(f"Failed to load blockMeshDict from {blockmesh_path}")
                return False

            # Create vertices list (8 corners of bounding box)
            # Round to 2 decimal places
            vertices = [
                [round(xmin, 2), round(ymin, 2), round(zmin, 2)],  # 0
                [round(xmax, 2), round(ymin, 2), round(zmin, 2)],  # 1
                [round(xmax, 2), round(ymax, 2), round(zmin, 2)],  # 2
                [round(xmin, 2), round(ymax, 2), round(zmin, 2)],  # 3
                [round(xmin, 2), round(ymin, 2), round(zmax, 2)],  # 4
                [round(xmax, 2), round(ymin, 2), round(zmax, 2)],  # 5
                [round(xmax, 2), round(ymax, 2), round(zmax, 2)],  # 6
                [round(xmin, 2), round(ymax, 2), round(zmax, 2)],  # 7
            ]

            # Update vertices in blockMeshDict
            if not foam_file.has_key("vertices"):
                print("vertices key not found in blockMeshDict")
                return False

            foam_file.set_value("vertices", vertices, show_type="list")

            # Update blocks section with base grid cells
            # Use map_key='cells' to access the cells parameter in blocks[0]
            new_cells = [int(cells_x), int(cells_y), int(cells_z)]
            foam_file.set_value('blocks[0]', new_cells, map_key='cells')

            # Verify the update
            verify_cells = foam_file.get_value('blocks[0]', map_key='cells')
            print(f"Updated blockMeshDict cells: {verify_cells}")

            # Save the updated blockMeshDict
            foam_file.save()
            print(f"Updated blockMeshDict: {blockmesh_path}")
            return True

        except Exception as e:
            print(f"Error updating blockMeshDict: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _update_snappyhex_dict(self) -> bool:
        """
        Update snappyHexMeshDict with locationsInMesh from geometry probe positions.
        Uses direct text manipulation with regex since FoamFile doesn't parse this correctly.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Path to snappyHexMeshDict
            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"
            snappy_path = case_path / "system" / "snappyHexMeshDict"

            if not snappy_path.exists():
                print(f"snappyHexMeshDict not found: {snappy_path}")
                return False

            # Get all geometry objects from tree
            geometries = self.case_data.list_geometries()

            if not geometries:
                print("No geometries found in case_data")
                return False

            # Create locationsInMesh entries from ALL geometry objects
            location_lines = []
            for geom_name in geometries:
                probe_pos = self.case_data.get_geometry_probe_position(geom_name)

                # Use (0, 0, 0) if no probe position is set
                if probe_pos is None:
                    probe_pos = (0.0, 0.0, 0.0)
                    print(f"Warning: No probe position set for '{geom_name}', using (0, 0, 0)")

                # Format: (( x  y  z) region_name)
                x, y, z = probe_pos
                location_line = f"        (( {x:<9.4f} {y:<9.4f} {z:<9.4f}) {geom_name})"
                location_lines.append(location_line)
                print(f"Added location for '{geom_name}': ({x:.4f} {y:.4f} {z:.4f})")

            if not location_lines:
                print("Warning: No geometries found for locationsInMesh")
                return False

            # Read the entire file
            with open(snappy_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Build the new locationsInMesh block
            new_locations_block = "    locationsInMesh\n    (\n"
            new_locations_block += "\n".join(location_lines)
            new_locations_block += "\n    );"

            # Find and replace the locationsInMesh block using regex
            # Pattern matches: locationsInMesh\n    (\n        ...content...\n    );
            pattern = r'locationsInMesh\s*\(\s*(?:.*?)\s*\);'

            if not re.search(pattern, content, re.DOTALL):
                print("Error: locationsInMesh block not found in snappyHexMeshDict")
                return False

            # Replace the block
            new_content = re.sub(pattern, new_locations_block, content, flags=re.DOTALL)

            # Write back to file
            with open(snappy_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"Successfully updated snappyHexMeshDict: {snappy_path}")
            print(f"Updated {len(location_lines)} location(s) in locationsInMesh")
            return True

        except Exception as e:
            print(f"Error updating snappyHexMeshDict: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _on_mesh_generated(self):
        """Handle mesh generation completion - load and display generated mesh."""
        print("Mesh generation completed")

        if not self.vtk_pre:
            return

        # Hide geometry STL objects
        all_objs = self.vtk_pre.obj_manager.get_all()
        geom_count = 0
        for obj in all_objs:
            if hasattr(obj, 'group') and obj.group == "geometry":
                obj.actor.SetVisibility(False)
                geom_count += 1
        print(f"Hidden {geom_count} geometry objects")

        # Load mesh using OpenFOAM reader
        self.load_mesh_async()

    def load_mesh_async(self):
        """Load existing mesh asynchronously from OpenFOAM case folder."""
        print("[DEBUG] MeshGenerationView.load_mesh_async() called")

        mesh_case_path = Path(self.case_data.path) / "2.meshing_MheadBL"

        # Check for polyMesh folder (native OpenFOAM format)
        polymesh_folder = mesh_case_path / "constant" / "polyMesh"

        if not polymesh_folder.exists() or not (polymesh_folder / "points").exists():
            print("No mesh found - polyMesh folder missing")
            return

        print(f"Found polyMesh folder: {polymesh_folder}")
        print(f"Loading OpenFOAM case asynchronously: {mesh_case_path}")

        # Load mesh in background thread
        class MeshLoadThread(QThread):
            def __init__(self, view, case_path):
                super().__init__()
                self.view = view
                self.case_path = case_path
                self.reader = None
                self.success = False

            def run(self):
                """Load OpenFOAM case in background thread."""
                try:
                    # Create case.foam file if it doesn't exist
                    foam_file = self.case_path / "case.foam"
                    if not foam_file.exists():
                        foam_file.write_text("", encoding="utf-8")
                        print(f"[Thread] Created case.foam: {foam_file}")

                    # Create vtkOpenFOAMReader
                    reader = vtk.vtkOpenFOAMReader()
                    reader.SetFileName(str(foam_file))

                    # Enable cell-to-point interpolation (ParaView style)
                    if hasattr(reader, "SetCreateCellToPointOn"):
                        reader.SetCreateCellToPointOn()
                    elif hasattr(reader, "SetCreateCellToPoint"):
                        reader.SetCreateCellToPoint(1)

                    # Decompose polyhedra
                    if hasattr(reader, "DecomposePolyhedraOn"):
                        reader.DecomposePolyhedraOn()
                    elif hasattr(reader, "SetDecomposePolyhedra"):
                        reader.SetDecomposePolyhedra(1)

                    # Read the data
                    reader.Update()

                    self.reader = reader
                    self.success = True
                    print(f"[Thread] OpenFOAM case loaded successfully")

                except Exception as e:
                    print(f"[Thread] Error loading OpenFOAM case: {e}")
                    import traceback
                    traceback.print_exc()
                    self.success = False

        # Create and start thread
        self.mesh_thread = MeshLoadThread(self, mesh_case_path)
        self.mesh_thread.finished.connect(
            lambda: self._on_openfoam_case_loaded(
                self.mesh_thread.reader if self.mesh_thread.success else None
            )
        )
        self.mesh_thread.start()

    def _on_openfoam_case_loaded(self, reader):
        """Handle OpenFOAM case loaded in background thread."""
        if not reader or not self.vtk_pre:
            print("Failed to load OpenFOAM case")
            return

        try:
            # Store reader
            self.foam_reader = reader

            # Clear existing slice/clip pipeline
            self._clear_slice_clip()

            # Extract surface geometry (MultiBlock → PolyData)
            geom = vtk.vtkCompositeDataGeometryFilter()
            geom.SetInputConnection(reader.GetOutputPort())
            geom.Update()

            polydata = geom.GetOutput()
            self.geom_output = polydata

            # Calculate bounds, center, diagonal length
            b = polydata.GetBounds()
            self.bounds = b
            cx = 0.5 * (b[0] + b[1])
            cy = 0.5 * (b[2] + b[3])
            cz = 0.5 * (b[4] + b[5])
            self.center = (cx, cy, cz)
            dx = b[1] - b[0]
            dy = b[3] - b[2]
            dz = b[5] - b[4]
            self.diagonal_length = math.sqrt(dx * dx + dy * dy + dz * dz)

            print(f"Surface points: {polydata.GetNumberOfPoints()}")
            print(f"Bounds: {b}")
            print(f"Center: {self.center}")

            # Create surface actor
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(polydata)
            mapper.ScalarVisibilityOff()

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            prop = actor.GetProperty()
            prop.SetRepresentationToSurface()
            prop.EdgeVisibilityOn()
            prop.SetColor(0.85, 0.85, 0.90)
            prop.SetEdgeColor(0.10, 0.10, 0.40)
            prop.SetLineWidth(1.0)

            # Remove existing mesh if present
            existing_mesh = self.vtk_pre.obj_manager.find_by_name("mesh")
            if existing_mesh:
                self.vtk_pre.obj_manager.remove(existing_mesh.id)

            # Add mesh to VTK viewer with group="mesh"
            self.vtk_pre.obj_manager.add(actor, name="mesh", group="mesh")
            self.surface_actor = actor

            # Check if we're on Mesh Generation tab to determine initial visibility
            # Default is hidden (Geometry tab is usually active)
            current_page = self.parent.ui.stackedWidget.currentWidget()
            page_name = None
            if current_page == self.parent.ui.page_mesh_generation:
                page_name = "Mesh Generation"
                actor.SetVisibility(True)
            else:
                # Hide mesh if we're not on Mesh Generation tab
                actor.SetVisibility(False)

            # Fit camera only if mesh is visible
            if actor.GetVisibility():
                self.vtk_pre.camera.fit()

            # Refresh view
            self.vtk_pre.vtk_widget.GetRenderWindow().Render()

            print(f"OpenFOAM mesh loaded (visible: {actor.GetVisibility()})")

            # Initialize slice with current settings (only if visible)
            if actor.GetVisibility():
                self.update_slice()

        except Exception as e:
            print(f"Error displaying OpenFOAM mesh: {e}")
            import traceback
            traceback.print_exc()

    def _clear_slice_clip(self):
        """Clear slice/clip pipeline actors from renderer."""
        if not self.vtk_pre:
            return

        # Get renderer
        renderer = self.vtk_pre.vtk_widget.GetRenderWindow().GetRenderers().GetFirstRenderer()

        # Remove slice actor
        if self.slice_actor is not None:
            renderer.RemoveActor(self.slice_actor)
            self.slice_actor = None

        # Remove clip actor
        if self.clip_actor is not None:
            renderer.RemoveActor(self.clip_actor)
            self.clip_actor = None

        # Reset pipeline objects
        self.slice_plane = None
        self.clip_filter = None

    def _hide_slice_clip_actors(self):
        """Hide slice/clip actors without removing them (for tab switching)."""
        if not self.vtk_pre:
            return

        # Hide slice actor
        if self.slice_actor is not None:
            self.slice_actor.SetVisibility(False)

        # Hide clip actor
        if self.clip_actor is not None:
            self.clip_actor.SetVisibility(False)

    def _show_slice_clip_actors(self):
        """Show slice/clip actors (for tab switching back to Mesh Generation)."""
        if not self.vtk_pre:
            return

        # Show slice actor
        if self.slice_actor is not None:
            self.slice_actor.SetVisibility(True)

        # Show clip actor only if clip is enabled
        if self.clip_actor is not None and self.chk_clip.isChecked():
            self.clip_actor.SetVisibility(True)

    def _get_plane_params(self):
        """
        Calculate slice plane origin and normal based on current UI settings.

        Returns:
            Tuple of (origin, normal) or (None, None) if bounds not available
        """
        if self.bounds is None or self.center is None:
            return None, None

        xmin, xmax, ymin, ymax, zmin, zmax = self.bounds
        cx, cy, cz = self.center

        t = self.slider_pos.value() / 100.0  # 0.0 ~ 1.0

        dir_text = self.combo_dir.currentText()

        # Calculate normal and origin based on direction
        if dir_text == "X":
            normal = (1.0, 0.0, 0.0)
            x = xmin + t * (xmax - xmin)
            origin = (x, cy, cz)

        elif dir_text == "Y":
            normal = (0.0, 1.0, 0.0)
            y = ymin + t * (ymax - ymin)
            origin = (cx, y, cz)

        elif dir_text == "Z":
            normal = (0.0, 0.0, 1.0)
            z = zmin + t * (zmax - zmin)
            origin = (cx, cy, z)

        else:  # Custom
            nx = self.spin_nx.value()
            ny = self.spin_ny.value()
            nz = self.spin_nz.value()
            length = math.sqrt(nx * nx + ny * ny + nz * nz)
            if length < 1e-6:
                # Too small - use default Z-normal
                nx, ny, nz = 0.0, 0.0, 1.0
                length = 1.0
            normal = (nx / length, ny / length, nz / length)

            # Move along normal direction based on slider
            d = self.diagonal_length if self.diagonal_length else 1.0
            s = (t - 0.5) * d
            ox = cx + s * normal[0]
            oy = cy + s * normal[1]
            oz = cz + s * normal[2]
            origin = (ox, oy, oz)

        return origin, normal

    def _on_slider_changed(self, value: int):
        """Handle slider value change."""
        self.lbl_pos_value.setText(f"{value}%")
        self.update_slice()

    def update_slice(self):
        """Update slice/clip visualization based on current settings."""
        if self.foam_reader is None or self.geom_output is None or not self.vtk_pre:
            return

        origin, normal = self._get_plane_params()
        if origin is None or normal is None:
            return

        # Get renderer
        renderer = self.vtk_pre.vtk_widget.GetRenderWindow().GetRenderers().GetFirstRenderer()

        # Create or update slice plane
        if self.slice_plane is None:
            self.slice_plane = vtk.vtkPlane()

        self.slice_plane.SetOrigin(*origin)
        self.slice_plane.SetNormal(*normal)

        # ==================================================================
        # 1) ParaView-style Slice pipeline
        # ==================================================================

        # Remove previous slice actor
        if self.slice_actor is not None:
            renderer.RemoveActor(self.slice_actor)
            self.slice_actor = None

        # 1. MultiBlock → PolyData flatten
        geom_all = vtk.vtkCompositeDataGeometryFilter()
        geom_all.SetInputConnection(self.foam_reader.GetOutputPort())
        geom_all.Update()

        # 2. Cell → Point interpolation (ParaView style)
        cd2pd = vtk.vtkCellDataToPointData()
        cd2pd.SetInputConnection(geom_all.GetOutputPort())
        cd2pd.Update()

        # 3. Clean polydata
        clean1 = vtk.vtkCleanPolyData()
        clean1.SetInputConnection(cd2pd.GetOutputPort())

        # 4. Slice
        cutter = vtk.vtkCutter()
        cutter.SetCutFunction(self.slice_plane)
        cutter.SetInputConnection(clean1.GetOutputPort())
        cutter.Update()

        # 5. Clean slice result
        clean2 = vtk.vtkCleanPolyData()
        clean2.SetInputConnection(cutter.GetOutputPort())

        # 6. Triangulate slice
        tri = vtk.vtkTriangleFilter()
        tri.SetInputConnection(clean2.GetOutputPort())

        # 7. Mapper & Actor
        slice_mapper = vtk.vtkPolyDataMapper()
        slice_mapper.SetInputConnection(tri.GetOutputPort())

        slice_actor = vtk.vtkActor()
        slice_actor.SetMapper(slice_mapper)
        slice_actor.GetProperty().SetColor(1.0, 0.1, 0.1)
        slice_actor.GetProperty().SetLineWidth(2)

        # Store and add to renderer
        self.slice_actor = slice_actor
        renderer.AddActor(slice_actor)

        # ==================================================================
        # 2) Clip (optional) - ParaView-style Slice + Clip
        # ==================================================================
        if self.chk_clip.isChecked():
            # Hide surface actor, show clipped volume
            if self.surface_actor is not None:
                self.surface_actor.SetVisibility(False)

            # Remove previous clip actor
            if self.clip_actor is not None:
                renderer.RemoveActor(self.clip_actor)

            # Create clip pipeline
            clip_filter = vtk.vtkClipDataSet()
            clip_filter.SetInputConnection(self.foam_reader.GetOutputPort())
            clip_filter.SetClipFunction(self.slice_plane)
            clip_filter.InsideOutOn()

            clip_geom = vtk.vtkCompositeDataGeometryFilter()
            clip_geom.SetInputConnection(clip_filter.GetOutputPort())

            clip_mapper = vtk.vtkPolyDataMapper()
            clip_mapper.SetInputConnection(clip_geom.GetOutputPort())

            clip_actor = vtk.vtkActor()
            clip_actor.SetMapper(clip_mapper)

            prop = clip_actor.GetProperty()
            prop.SetRepresentationToSurface()
            prop.EdgeVisibilityOn()
            prop.SetColor(0.80, 0.80, 0.90)
            prop.SetEdgeColor(0.0, 0.0, 0.0)
            prop.SetLineWidth(1.0)

            # Store and add to renderer
            self.clip_filter = clip_filter
            self.clip_actor = clip_actor
            renderer.AddActor(clip_actor)

        else:
            # No clip - remove clip actor and show surface
            if self.clip_actor is not None:
                renderer.RemoveActor(self.clip_actor)
                self.clip_actor = None
                self.clip_filter = None

            if self.surface_actor is not None:
                self.surface_actor.SetVisibility(True)

        # Render
        self.vtk_pre.vtk_widget.GetRenderWindow().Render()

    def _load_locations_from_snappyhex(self):
        """
        Load probe positions from snappyHexMeshDict locationsInMesh and update case_data.
        """
        try:
            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"
            snappy_path = case_path / "system" / "snappyHexMeshDict"

            if not snappy_path.exists():
                print(f"snappyHexMeshDict not found: {snappy_path}")
                return

            # Read file
            with open(snappy_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find locationsInMesh block using regex
            pattern = r'locationsInMesh\s*\(\s*(.*?)\s*\);'
            match = re.search(pattern, content, re.DOTALL)

            if not match:
                print("locationsInMesh not found in snappyHexMeshDict")
                return

            locations_block = match.group(1)

            # Parse each line: (( x y z) region_name)
            line_pattern = r'\(\s*\(\s*([\d\.\-e]+)\s+([\d\.\-e]+)\s+([\d\.\-e]+)\s*\)\s+(\w+)\s*\)'

            loaded_count = 0
            for line_match in re.finditer(line_pattern, locations_block):
                x = float(line_match.group(1))
                y = float(line_match.group(2))
                z = float(line_match.group(3))
                region_name = line_match.group(4)

                # Update case_data with probe position
                if self.case_data.set_geometry_probe_position(region_name, x, y, z):
                    loaded_count += 1
                    print(f"Loaded probe position for '{region_name}': ({x:.4f}, {y:.4f}, {z:.4f})")

            if loaded_count > 0:
                self.case_data.save()
                print(f"Successfully loaded {loaded_count} probe positions from snappyHexMeshDict")

        except Exception as e:
            print(f"Error loading locations from snappyHexMeshDict: {e}")
            import traceback
            traceback.print_exc()

    def load_data(self):
        """Load mesh settings from blockMeshDict."""
        print("[DEBUG] MeshGenerationView.load_data() called")

        # Default values
        default_cells = ["100", "100", "100"]

        # Load probe positions from snappyHexMeshDict
        self._load_locations_from_snappyhex()

        # Load existing mesh asynchronously
        self.load_mesh_async()

        try:
            # Path to blockMeshDict
            case_path = Path(self.case_data.path) / "2.meshing_MheadBL"
            blockmesh_path = case_path / "system" / "blockMeshDict"
            print(f"[DEBUG] blockMeshDict path: {blockmesh_path}")
            print(f"[DEBUG] blockMeshDict exists: {blockmesh_path.exists()}")

            if not blockmesh_path.exists():
                print(f"blockMeshDict not found, using default values")
                self.ui.lineEdit_basegrid_x.setText(default_cells[0])
                self.ui.lineEdit_basegrid_y.setText(default_cells[1])
                self.ui.lineEdit_basegrid_z.setText(default_cells[2])
                return

            # Load blockMeshDict
            foam_file = FoamFile(str(blockmesh_path))
            load_result = foam_file.load()
            print(f"[DEBUG] FoamFile.load() result: {load_result}")

            if not load_result:
                print(f"Failed to load blockMeshDict, using default values")
                self.ui.lineEdit_basegrid_x.setText(default_cells[0])
                self.ui.lineEdit_basegrid_y.setText(default_cells[1])
                self.ui.lineEdit_basegrid_z.setText(default_cells[2])
                return

            # Read cells from blocks[0]
            cells = foam_file.get_value('blocks[0]', map_key='cells')
            print(f"[DEBUG] Read cells from blockMeshDict: {cells}")
            print(f"[DEBUG] cells type: {type(cells)}")

            # cells is a list of lists: [[161, 81, 81]]
            # Extract the first element which contains the actual cells
            if cells and isinstance(cells, list) and len(cells) > 0:
                actual_cells = cells[0] if isinstance(cells[0], list) else cells
                print(f"[DEBUG] actual_cells: {actual_cells}")

                if isinstance(actual_cells, list) and len(actual_cells) >= 3:
                    self.ui.lineEdit_basegrid_x.setText(str(actual_cells[0]))
                    self.ui.lineEdit_basegrid_y.setText(str(actual_cells[1]))
                    self.ui.lineEdit_basegrid_z.setText(str(actual_cells[2]))
                    print(f"Loaded blockMeshDict cells: ({actual_cells[0]}, {actual_cells[1]}, {actual_cells[2]})")
                else:
                    print(f"Invalid cells format: {actual_cells}, using default values")
                    self.ui.lineEdit_basegrid_x.setText(default_cells[0])
                    self.ui.lineEdit_basegrid_y.setText(default_cells[1])
                    self.ui.lineEdit_basegrid_z.setText(default_cells[2])
            else:
                print(f"Invalid cells format: {cells}, using default values")
                self.ui.lineEdit_basegrid_x.setText(default_cells[0])
                self.ui.lineEdit_basegrid_y.setText(default_cells[1])
                self.ui.lineEdit_basegrid_z.setText(default_cells[2])

        except Exception as e:
            print(f"Error loading blockMeshDict: {e}")
            import traceback
            traceback.print_exc()
            self.ui.lineEdit_basegrid_x.setText(default_cells[0])
            self.ui.lineEdit_basegrid_y.setText(default_cells[1])
            self.ui.lineEdit_basegrid_z.setText(default_cells[2])
