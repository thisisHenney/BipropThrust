
from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

a5CHTFCase_noHT_reHTfoam = GetActiveSource()

renderView1 = GetActiveViewOrCreate('RenderView')

a5CHTFCase_noHT_reHTfoamDisplay = Show(a5CHTFCase_noHT_reHTfoam, renderView1, 'GeometryRepresentation')

a5CHTFCase_noHT_reHTfoamDisplay.Representation = 'Surface'
a5CHTFCase_noHT_reHTfoamDisplay.ColorArrayName = [None, '']
a5CHTFCase_noHT_reHTfoamDisplay.SelectTCoordArray = 'None'
a5CHTFCase_noHT_reHTfoamDisplay.SelectNormalArray = 'None'
a5CHTFCase_noHT_reHTfoamDisplay.SelectTangentArray = 'None'
a5CHTFCase_noHT_reHTfoamDisplay.OSPRayScaleArray = 'AR'
a5CHTFCase_noHT_reHTfoamDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
a5CHTFCase_noHT_reHTfoamDisplay.SelectOrientationVectors = 'None'
a5CHTFCase_noHT_reHTfoamDisplay.ScaleFactor = 0.0035201175371184948
a5CHTFCase_noHT_reHTfoamDisplay.SelectScaleArray = 'AR'
a5CHTFCase_noHT_reHTfoamDisplay.GlyphType = 'Arrow'
a5CHTFCase_noHT_reHTfoamDisplay.GlyphTableIndexArray = 'AR'
a5CHTFCase_noHT_reHTfoamDisplay.GaussianRadius = 0.00017600587685592472
a5CHTFCase_noHT_reHTfoamDisplay.SetScaleArray = ['POINTS', 'AR']
a5CHTFCase_noHT_reHTfoamDisplay.ScaleTransferFunction = 'PiecewiseFunction'
a5CHTFCase_noHT_reHTfoamDisplay.OpacityArray = ['POINTS', 'AR']
a5CHTFCase_noHT_reHTfoamDisplay.OpacityTransferFunction = 'PiecewiseFunction'
a5CHTFCase_noHT_reHTfoamDisplay.DataAxesGrid = 'GridAxesRepresentation'
a5CHTFCase_noHT_reHTfoamDisplay.PolarAxes = 'PolarAxesRepresentation'
a5CHTFCase_noHT_reHTfoamDisplay.SelectInputVectors = ['POINTS', 'sprayMMHCloud:UTrans']
a5CHTFCase_noHT_reHTfoamDisplay.WriteLog = ''

a5CHTFCase_noHT_reHTfoamDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.0067337192595005035, 1.0, 0.5, 0.0]

a5CHTFCase_noHT_reHTfoamDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.0067337192595005035, 1.0, 0.5, 0.0]

renderView1.ResetCamera(False)

materialLibrary1 = GetMaterialLibrary()

renderView1.Update()

ColorBy(a5CHTFCase_noHT_reHTfoamDisplay, ('FIELD', 'vtkBlockColors'))

a5CHTFCase_noHT_reHTfoamDisplay.SetScalarBarVisibility(renderView1, True)

vtkBlockColorsTF2D = GetTransferFunction2D('vtkBlockColors')

vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')
vtkBlockColorsLUT.InterpretValuesAsCategories = 1
vtkBlockColorsLUT.AnnotationsInitialized = 1
vtkBlockColorsLUT.TransferFunction2D = vtkBlockColorsTF2D
vtkBlockColorsLUT.Annotations = ['0', '0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9', '10', '10', '11', '11']
vtkBlockColorsLUT.ActiveAnnotatedValues = ['0', '1', '6', '7']
vtkBlockColorsLUT.IndexedColors = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.63, 0.63, 1.0, 0.67, 0.5, 0.33, 1.0, 0.5, 0.75, 0.53, 0.35, 0.7, 1.0, 0.75, 0.5]

vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')

a5CHTFCase_noHT_reHTfoam.MeshRegions = ['/filmRegion/patch/outlet']

renderView1.Update()

extractSurface1 = ExtractSurface(registrationName='ExtractSurface1', Input=a5CHTFCase_noHT_reHTfoam)

extractSurface1Display = Show(extractSurface1, renderView1, 'GeometryRepresentation')

extractSurface1Display.Representation = 'Surface'
extractSurface1Display.ColorArrayName = [None, '']
extractSurface1Display.SelectTCoordArray = 'None'
extractSurface1Display.SelectNormalArray = 'None'
extractSurface1Display.SelectTangentArray = 'None'
extractSurface1Display.OSPRayScaleFunction = 'PiecewiseFunction'
extractSurface1Display.SelectOrientationVectors = 'None'
extractSurface1Display.ScaleFactor = 0.0015060695819556714
extractSurface1Display.SelectScaleArray = 'None'
extractSurface1Display.GlyphType = 'Arrow'
extractSurface1Display.GlyphTableIndexArray = 'None'
extractSurface1Display.GaussianRadius = 7.530347909778356e-05
extractSurface1Display.SetScaleArray = [None, '']
extractSurface1Display.ScaleTransferFunction = 'PiecewiseFunction'
extractSurface1Display.OpacityArray = [None, '']
extractSurface1Display.OpacityTransferFunction = 'PiecewiseFunction'
extractSurface1Display.DataAxesGrid = 'GridAxesRepresentation'
extractSurface1Display.PolarAxes = 'PolarAxesRepresentation'
extractSurface1Display.SelectInputVectors = [None, '']
extractSurface1Display.WriteLog = ''

Hide(a5CHTFCase_noHT_reHTfoam, renderView1)

renderView1.Update()

generateSurfaceNormals1 = GenerateSurfaceNormals(registrationName='GenerateSurfaceNormals1', Input=extractSurface1)

generateSurfaceNormals1.ComputeCellNormals = 1

generateSurfaceNormals1Display = Show(generateSurfaceNormals1, renderView1, 'GeometryRepresentation')

generateSurfaceNormals1Display.Representation = 'Surface'
generateSurfaceNormals1Display.ColorArrayName = [None, '']
generateSurfaceNormals1Display.SelectTCoordArray = 'None'
generateSurfaceNormals1Display.SelectNormalArray = 'Normals'
generateSurfaceNormals1Display.SelectTangentArray = 'None'
generateSurfaceNormals1Display.OSPRayScaleArray = 'Normals'
generateSurfaceNormals1Display.OSPRayScaleFunction = 'PiecewiseFunction'
generateSurfaceNormals1Display.SelectOrientationVectors = 'None'
generateSurfaceNormals1Display.ScaleFactor = 0.0015060695819556714
generateSurfaceNormals1Display.SelectScaleArray = 'None'
generateSurfaceNormals1Display.GlyphType = 'Arrow'
generateSurfaceNormals1Display.GlyphTableIndexArray = 'None'
generateSurfaceNormals1Display.GaussianRadius = 7.530347909778356e-05
generateSurfaceNormals1Display.SetScaleArray = ['POINTS', 'Normals']
generateSurfaceNormals1Display.ScaleTransferFunction = 'PiecewiseFunction'
generateSurfaceNormals1Display.OpacityArray = ['POINTS', 'Normals']
generateSurfaceNormals1Display.OpacityTransferFunction = 'PiecewiseFunction'
generateSurfaceNormals1Display.DataAxesGrid = 'GridAxesRepresentation'
generateSurfaceNormals1Display.PolarAxes = 'PolarAxesRepresentation'
generateSurfaceNormals1Display.SelectInputVectors = ['POINTS', 'Normals']
generateSurfaceNormals1Display.WriteLog = ''

generateSurfaceNormals1Display.ScaleTransferFunction.Points = [0.9045549035072327, 0.0, 0.5, 0.0, 0.9272884130477905, 1.0, 0.5, 0.0]

generateSurfaceNormals1Display.OpacityTransferFunction.Points = [0.9045549035072327, 0.0, 0.5, 0.0, 0.9272884130477905, 1.0, 0.5, 0.0]

Hide(extractSurface1, renderView1)

renderView1.Update()

calculator1 = Calculator(registrationName='Calculator1', Input=generateSurfaceNormals1)
calculator1.Function = ''

SetActiveSource(extractSurface1)

calculator1.Function = ''

calculator1Display = Show(calculator1, renderView1, 'GeometryRepresentation')

calculator1Display.Representation = 'Surface'
calculator1Display.ColorArrayName = [None, '']
calculator1Display.SelectTCoordArray = 'None'
calculator1Display.SelectNormalArray = 'Normals'
calculator1Display.SelectTangentArray = 'None'
calculator1Display.OSPRayScaleArray = 'Normals'
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.SelectOrientationVectors = 'None'
calculator1Display.ScaleFactor = 0.0015060695819556714
calculator1Display.SelectScaleArray = 'None'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.GlyphTableIndexArray = 'None'
calculator1Display.GaussianRadius = 7.530347909778356e-05
calculator1Display.SetScaleArray = ['POINTS', 'Normals']
calculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator1Display.OpacityArray = ['POINTS', 'Normals']
calculator1Display.OpacityTransferFunction = 'PiecewiseFunction'
calculator1Display.DataAxesGrid = 'GridAxesRepresentation'
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.SelectInputVectors = ['POINTS', 'Normals']
calculator1Display.WriteLog = ''

calculator1Display.ScaleTransferFunction.Points = [0.9045549035072327, 0.0, 0.5, 0.0, 0.9272884130477905, 1.0, 0.5, 0.0]

calculator1Display.OpacityTransferFunction.Points = [0.9045549035072327, 0.0, 0.5, 0.0, 0.9272884130477905, 1.0, 0.5, 0.0]

Hide(generateSurfaceNormals1, renderView1)

renderView1.Update()

SetActiveSource(a5CHTFCase_noHT_reHTfoam)

a5CHTFCase_noHT_reHTfoam.MeshRegions = ['/fluid/patch/outlet']

renderView1.Update()

SetActiveSource(calculator1)

SetActiveSource(a5CHTFCase_noHT_reHTfoam)

a5CHTFCase_noHT_reHTfoam.CellArrays = ['U', 'p', 'rho']

renderView1.Update()

SetActiveSource(calculator1)

SetActiveSource(a5CHTFCase_noHT_reHTfoam)

SetActiveSource(extractSurface1)

SetActiveSource(generateSurfaceNormals1)

SetActiveSource(calculator1)

SetActiveSource(generateSurfaceNormals1)

Hide(calculator1, renderView1)

generateSurfaceNormals1Display = Show(generateSurfaceNormals1, renderView1, 'GeometryRepresentation')

Delete(calculator1)
del calculator1

calculator1 = Calculator(registrationName='Calculator1', Input=generateSurfaceNormals1)
calculator1.Function = ''

SetActiveSource(a5CHTFCase_noHT_reHTfoam)

calculator1.Function = ''

calculator1Display = Show(calculator1, renderView1, 'GeometryRepresentation')

calculator1Display.Representation = 'Surface'
calculator1Display.ColorArrayName = [None, '']
calculator1Display.SelectTCoordArray = 'None'
calculator1Display.SelectNormalArray = 'Normals'
calculator1Display.SelectTangentArray = 'None'
calculator1Display.OSPRayScaleArray = 'Normals'
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.SelectOrientationVectors = 'None'
calculator1Display.ScaleFactor = 0.0014608359429985286
calculator1Display.SelectScaleArray = 'None'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.GlyphTableIndexArray = 'None'
calculator1Display.GaussianRadius = 7.304179714992643e-05
calculator1Display.SetScaleArray = ['POINTS', 'Normals']
calculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator1Display.OpacityArray = ['POINTS', 'Normals']
calculator1Display.OpacityTransferFunction = 'PiecewiseFunction'
calculator1Display.DataAxesGrid = 'GridAxesRepresentation'
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.SelectInputVectors = ['POINTS', 'Normals']
calculator1Display.WriteLog = ''

calculator1Display.ScaleTransferFunction.Points = [0.999902069568634, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]

calculator1Display.OpacityTransferFunction.Points = [0.999902069568634, 0.0, 0.5, 0.0, 1.0, 1.0, 0.5, 0.0]

Hide(generateSurfaceNormals1, renderView1)

renderView1.Update()

SetActiveSource(calculator1)

SetActiveSource(a5CHTFCase_noHT_reHTfoam)

a5CHTFCase_noHT_reHTfoam.CellArrays = ['AR', 'CH3', 'CH3NHNH2', 'CH3NN', 'CH3NNH', 'CH3NNH2', 'CH3O', 'CH4', 'CO', 'CO2', 'H', 'H2', 'H2CN', 'H2O', 'HCN', 'HNC', 'HNCO', 'HNO3', 'HONO', 'Mach', 'N', 'N2', 'N2O4', 'NH', 'NH2', 'NH3', 'NO', 'NO2', 'O', 'O2', 'OH', 'T', 'U', 'alphat', 'dQ', 'k', 'nut', 'omega', 'p', 'rho', 'sprayMMHCloud:UCoeff', 'sprayMMHCloud:UTrans', 'sprayMMHCloud:hsCoeff', 'sprayMMHCloud:hsTrans', 'sprayMMHCloud:rhoTrans_AR', 'sprayMMHCloud:rhoTrans_CH3', 'sprayMMHCloud:rhoTrans_CH3NHNH2', 'sprayMMHCloud:rhoTrans_CH3NN', 'sprayMMHCloud:rhoTrans_CH3NNH', 'sprayMMHCloud:rhoTrans_CH3NNH2', 'sprayMMHCloud:rhoTrans_CH3O', 'sprayMMHCloud:rhoTrans_CH4', 'sprayMMHCloud:rhoTrans_CO', 'sprayMMHCloud:rhoTrans_CO2', 'sprayMMHCloud:rhoTrans_H', 'sprayMMHCloud:rhoTrans_H2', 'sprayMMHCloud:rhoTrans_H2CN', 'sprayMMHCloud:rhoTrans_H2O', 'sprayMMHCloud:rhoTrans_HCN', 'sprayMMHCloud:rhoTrans_HNC', 'sprayMMHCloud:rhoTrans_HNCO', 'sprayMMHCloud:rhoTrans_HNO3', 'sprayMMHCloud:rhoTrans_HONO', 'sprayMMHCloud:rhoTrans_N', 'sprayMMHCloud:rhoTrans_N2', 'sprayMMHCloud:rhoTrans_N2O4', 'sprayMMHCloud:rhoTrans_NH', 'sprayMMHCloud:rhoTrans_NH2', 'sprayMMHCloud:rhoTrans_NH3', 'sprayMMHCloud:rhoTrans_NO', 'sprayMMHCloud:rhoTrans_NO2', 'sprayMMHCloud:rhoTrans_O', 'sprayMMHCloud:rhoTrans_O2', 'sprayMMHCloud:rhoTrans_OH', 'sprayNTOCloud:UCoeff', 'sprayNTOCloud:UTrans', 'sprayNTOCloud:hsCoeff', 'sprayNTOCloud:hsTrans', 'sprayNTOCloud:rhoTrans_AR', 'sprayNTOCloud:rhoTrans_CH3', 'sprayNTOCloud:rhoTrans_CH3NHNH2', 'sprayNTOCloud:rhoTrans_CH3NN', 'sprayNTOCloud:rhoTrans_CH3NNH', 'sprayNTOCloud:rhoTrans_CH3NNH2', 'sprayNTOCloud:rhoTrans_CH3O', 'sprayNTOCloud:rhoTrans_CH4', 'sprayNTOCloud:rhoTrans_CO', 'sprayNTOCloud:rhoTrans_CO2', 'sprayNTOCloud:rhoTrans_H', 'sprayNTOCloud:rhoTrans_H2', 'sprayNTOCloud:rhoTrans_H2CN', 'sprayNTOCloud:rhoTrans_H2O', 'sprayNTOCloud:rhoTrans_HCN', 'sprayNTOCloud:rhoTrans_HNC', 'sprayNTOCloud:rhoTrans_HNCO', 'sprayNTOCloud:rhoTrans_HNO3', 'sprayNTOCloud:rhoTrans_HONO', 'sprayNTOCloud:rhoTrans_N', 'sprayNTOCloud:rhoTrans_N2', 'sprayNTOCloud:rhoTrans_N2O4', 'sprayNTOCloud:rhoTrans_NH', 'sprayNTOCloud:rhoTrans_NH2', 'sprayNTOCloud:rhoTrans_NH3', 'sprayNTOCloud:rhoTrans_NO', 'sprayNTOCloud:rhoTrans_NO2', 'sprayNTOCloud:rhoTrans_O', 'sprayNTOCloud:rhoTrans_O2', 'sprayNTOCloud:rhoTrans_OH']

renderView1.Update()

SetActiveSource(calculator1)

SetActiveSource(a5CHTFCase_noHT_reHTfoam)

SetActiveSource(extractSurface1)

SetActiveSource(generateSurfaceNormals1)

SetActiveSource(calculator1)

animationScene1 = GetAnimationScene()

animationScene1.AnimationTime = 0.02

timeKeeper1 = GetTimeKeeper()

SetActiveSource(generateSurfaceNormals1)

SetActiveSource(calculator1)

SetActiveSource(a5CHTFCase_noHT_reHTfoam)

a5CHTFCase_noHT_reHTfoam.CellArrays = ['U', 'p', 'rho']

renderView1.Update()

SetActiveSource(calculator1)

calculator1.Function = 'rho*(U_X*U_X+U_Y*U_Y+U_Z*U_Z)'

renderView1.Update()

integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=calculator1)
print(integrateVariables1)

spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

integrateVariables1Display = Show(integrateVariables1, spreadSheetView1, 'SpreadSheetRepresentation')

layout1 = GetLayoutByName("Layout #1")

AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)

integrateVariables1Display.Assembly = ''

renderView1.Update()

spreadSheetView1.Update()

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

SetActiveSource(integrateVariables1)

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

SelectIDs(IDs=[-1, 0], FieldType=1, ContainingCells=0)

ExportView('/home/user1/OpenFOAM/user1-v2212/run/jskang/KARI/250214/CHTF/5.CHTFCase_noHT_reHT/performance_thrust.csv', view=spreadSheetView1, RealNumberNotation='Scientific')



layout1.SetSize(1280, 1157)


renderView1.CameraPosition = [-0.04490822510305423, 0.03471043690336882, 0.04260718620139332]
renderView1.CameraFocalPoint = [0.01640058762859553, 3.0035153031348547e-07, 0.0]
renderView1.CameraViewUp = [0.30397586969568235, 0.9044152502802929, -0.2993855803194079]
renderView1.CameraParallelScale = 0.021309684052540755

