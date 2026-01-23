"""
Mesh Generation View - Handles mesh generation logic

This view connects to UI widgets defined in center_form_ui.py
and implements OpenFOAM mesh generation functionality.
"""

from pathlib import Path
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

        # Connect signals
        self._init_connect()

    def _init_connect(self):
        """Initialize signal connections."""
        self.ui.button_mesh_generate.clicked.connect(self._on_generate_clicked)

    def _on_generate_clicked(self):
        """Handle Generate button click - update blockMeshDict and run mesh generation."""
        # Disable button during execution
        self.ui.button_mesh_generate.setEnabled(False)

        # Get base grid values
        x = self.ui.lineEdit_basegrid_x.text() or "100"
        y = self.ui.lineEdit_basegrid_y.text() or "100"
        z = self.ui.lineEdit_basegrid_z.text() or "100"

        print(f"Generating mesh with base grid: ({x}, {y}, {z})")

        # Update blockMeshDict with geometry bounding box and base grid
        if not self._update_blockmesh_dict(x, y, z):
            print("Failed to update blockMeshDict")
            self.ui.button_mesh_generate.setEnabled(True)
            return

        # TODO: Update snappyHexMeshDict with boundary layer settings

        # Set working directory to case path
        if self.exec_widget:
            self.exec_widget.set_working_path(str(self.case_data.path))

            # Register callbacks
            self.exec_widget.register_func_after_finished(self._on_mesh_generated)
            self.exec_widget.register_func_on_error(self._restore_ui)
            self.exec_widget.register_func_restore_ui(self._restore_ui)

            # Define mesh generation commands
            commands = [
                "cd 2.meshing_MheadBL",
                "blockMesh",
                "snappyHexMesh -overwrite",
                "cd .."
            ]

            # Run mesh generation commands
            self.exec_widget.run(commands)
        else:
            print("ExecWidget not available")
            self.ui.button_mesh_generate.setEnabled(True)

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
        geom_objects = self.vtk_pre.obj_manager.get_all_in_group("geometry")
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

    def _on_mesh_generated(self):
        """Handle mesh generation completion - load and display generated mesh."""
        print("Mesh generation completed")

        # Load generated mesh to VTK
        if self.vtk_pre:
            mesh_path = Path(self.case_data.path) / "2.meshing_MheadBL" / "constant" / "triSurface" / "mesh.stl"
            if mesh_path.exists():
                print(f"Loading generated mesh: {mesh_path}")
                # TODO: Load mesh to VTK
                # actor = self.vtk_pre.mesh_loader.load_stl(mesh_path)
                # self.vtk_pre.obj_manager.add(actor, name="mesh", group="mesh")
            else:
                print(f"Generated mesh not found: {mesh_path}")

    def load_data(self):
        """Load mesh settings from blockMeshDict."""
        print("[DEBUG] MeshGenerationView.load_data() called")

        # Default values
        default_cells = ["100", "100", "100"]

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
