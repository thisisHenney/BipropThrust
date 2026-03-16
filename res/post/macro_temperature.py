
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

slice1 = Slice(registrationName='Slice1', Input=a5CHTFCase_noHT_reHTfoam)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

slice1.SliceType.Origin = [0.01640058762859553, 3.003515303134918e-07, 0.0]

slice1.HyperTreeGridSlicer.Origin = [0.01640058762859553, 3.003515303134918e-07, 0.0]

slice1.SliceType.Normal = [0.0, 0.0, 1.0]

slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = [None, '']
slice1Display.SelectTCoordArray = 'None'
slice1Display.SelectNormalArray = 'None'
slice1Display.SelectTangentArray = 'None'
slice1Display.OSPRayScaleArray = 'AR'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'None'
slice1Display.ScaleFactor = 0.0035200013080611825
slice1Display.SelectScaleArray = 'AR'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'AR'
slice1Display.GaussianRadius = 0.00017600006540305913
slice1Display.SetScaleArray = ['POINTS', 'AR']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'AR']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'
slice1Display.SelectInputVectors = ['POINTS', 'sprayMMHCloud:UTrans']
slice1Display.WriteLog = ''

slice1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.005190156400203705, 1.0, 0.5, 0.0]

slice1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.005190156400203705, 1.0, 0.5, 0.0]

Hide(a5CHTFCase_noHT_reHTfoam, renderView1)

renderView1.Update()

ColorBy(slice1Display, ('FIELD', 'vtkBlockColors'))

slice1Display.SetScalarBarVisibility(renderView1, True)

HideInteractiveWidgets(proxy=slice1.SliceType)

animationScene1 = GetAnimationScene()

animationScene1.AnimationTime = 0.02

timeKeeper1 = GetTimeKeeper()

ColorBy(slice1Display, ('CELLS', 'T'))

HideScalarBarIfNotNeeded(vtkBlockColorsLUT, renderView1)

slice1Display.RescaleTransferFunctionToDataRange(True, False)

slice1Display.SetScalarBarVisibility(renderView1, True)

tTF2D = GetTransferFunction2D('T')

tLUT = GetColorTransferFunction('T')
tLUT.TransferFunction2D = tTF2D
tLUT.RGBPoints = [371.2058410644531, 0.231373, 0.298039, 0.752941, 1836.989517211914, 0.865003, 0.865003, 0.865003, 3302.773193359375, 0.705882, 0.0156863, 0.14902]
tLUT.ScalarRangeInitialized = 1.0

tPWF = GetOpacityTransferFunction('T')
tPWF.Points = [371.2058410644531, 0.0, 0.5, 0.0, 3302.773193359375, 1.0, 0.5, 0.0]
tPWF.ScalarRangeInitialized = 1

ColorBy(slice1Display, ('POINTS', 'T'))

HideScalarBarIfNotNeeded(tLUT, renderView1)

slice1Display.RescaleTransferFunctionToDataRange(True, False)

slice1Display.SetScalarBarVisibility(renderView1, True)

a5CHTFCase_noHT_reHTfoam_1 = OpenFOAMReader(registrationName='5.CHTFCase_noHT_reHT.foam', FileName='/home/user1/OpenFOAM/user1-v2212/run/jskang/KARI/250214/CHTF/5.CHTFCase_noHT_reHT/5.CHTFCase_noHT_reHT.foam')
a5CHTFCase_noHT_reHTfoam_1.MeshRegions = ['/filmRegion/internalMesh', '/fluid/internalMesh', '/fluid/lagrangian/sprayMMHCloudTracks', '/fluid/lagrangian/sprayNTOCloudTracks', '/fluid/lagrangian/sprayMMHCloud', '/fluid/lagrangian/sprayNTOCloud', '/header/internalMesh', '/thruster/internalMesh']
a5CHTFCase_noHT_reHTfoam_1.CellArrays = ['AR', 'CH3', 'CH3NHNH2', 'CH3NN', 'CH3NNH', 'CH3NNH2', 'CH3O', 'CH4', 'CO', 'CO2', 'H', 'H2', 'H2CN', 'H2O', 'HCN', 'HNC', 'HNCO', 'HNO3', 'HONO', 'Mach', 'N', 'N2', 'N2O4', 'NH', 'NH2', 'NH3', 'NO', 'NO2', 'O', 'O2', 'OH', 'T', 'U', 'alphat', 'dQ', 'k', 'nut', 'omega', 'p', 'rho', 'sprayMMHCloud:UCoeff', 'sprayMMHCloud:UTrans', 'sprayMMHCloud:hsCoeff', 'sprayMMHCloud:hsTrans', 'sprayMMHCloud:rhoTrans_AR', 'sprayMMHCloud:rhoTrans_CH3', 'sprayMMHCloud:rhoTrans_CH3NHNH2', 'sprayMMHCloud:rhoTrans_CH3NN', 'sprayMMHCloud:rhoTrans_CH3NNH', 'sprayMMHCloud:rhoTrans_CH3NNH2', 'sprayMMHCloud:rhoTrans_CH3O', 'sprayMMHCloud:rhoTrans_CH4', 'sprayMMHCloud:rhoTrans_CO', 'sprayMMHCloud:rhoTrans_CO2', 'sprayMMHCloud:rhoTrans_H', 'sprayMMHCloud:rhoTrans_H2', 'sprayMMHCloud:rhoTrans_H2CN', 'sprayMMHCloud:rhoTrans_H2O', 'sprayMMHCloud:rhoTrans_HCN', 'sprayMMHCloud:rhoTrans_HNC', 'sprayMMHCloud:rhoTrans_HNCO', 'sprayMMHCloud:rhoTrans_HNO3', 'sprayMMHCloud:rhoTrans_HONO', 'sprayMMHCloud:rhoTrans_N', 'sprayMMHCloud:rhoTrans_N2', 'sprayMMHCloud:rhoTrans_N2O4', 'sprayMMHCloud:rhoTrans_NH', 'sprayMMHCloud:rhoTrans_NH2', 'sprayMMHCloud:rhoTrans_NH3', 'sprayMMHCloud:rhoTrans_NO', 'sprayMMHCloud:rhoTrans_NO2', 'sprayMMHCloud:rhoTrans_O', 'sprayMMHCloud:rhoTrans_O2', 'sprayMMHCloud:rhoTrans_OH', 'sprayNTOCloud:UCoeff', 'sprayNTOCloud:UTrans', 'sprayNTOCloud:hsCoeff', 'sprayNTOCloud:hsTrans', 'sprayNTOCloud:rhoTrans_AR', 'sprayNTOCloud:rhoTrans_CH3', 'sprayNTOCloud:rhoTrans_CH3NHNH2', 'sprayNTOCloud:rhoTrans_CH3NN', 'sprayNTOCloud:rhoTrans_CH3NNH', 'sprayNTOCloud:rhoTrans_CH3NNH2', 'sprayNTOCloud:rhoTrans_CH3O', 'sprayNTOCloud:rhoTrans_CH4', 'sprayNTOCloud:rhoTrans_CO', 'sprayNTOCloud:rhoTrans_CO2', 'sprayNTOCloud:rhoTrans_H', 'sprayNTOCloud:rhoTrans_H2', 'sprayNTOCloud:rhoTrans_H2CN', 'sprayNTOCloud:rhoTrans_H2O', 'sprayNTOCloud:rhoTrans_HCN', 'sprayNTOCloud:rhoTrans_HNC', 'sprayNTOCloud:rhoTrans_HNCO', 'sprayNTOCloud:rhoTrans_HNO3', 'sprayNTOCloud:rhoTrans_HONO', 'sprayNTOCloud:rhoTrans_N', 'sprayNTOCloud:rhoTrans_N2', 'sprayNTOCloud:rhoTrans_N2O4', 'sprayNTOCloud:rhoTrans_NH', 'sprayNTOCloud:rhoTrans_NH2', 'sprayNTOCloud:rhoTrans_NH3', 'sprayNTOCloud:rhoTrans_NO', 'sprayNTOCloud:rhoTrans_NO2', 'sprayNTOCloud:rhoTrans_O', 'sprayNTOCloud:rhoTrans_O2', 'sprayNTOCloud:rhoTrans_OH']
a5CHTFCase_noHT_reHTfoam_1.LagrangianArrays = ['Cp', 'KHindex', 'Nu', 'Re', 'T', 'Tfg', 'U', 'UCorrect', 'UTurb', 'We', 'YCH3NHNH2(l)', 'YN2O4(l)', 'active', 'age', 'd', 'd0', 'dTarget', 'htc', 'injector', 'liquidCore', 'mass0', 'ms', 'mu', 'nParticle', 'origId', 'origProcId', 'position0', 'rho', 'sigma', 'tMom', 'tTurb', 'tc', 'typeId', 'user', 'y', 'yDot']

a5CHTFCase_noHT_reHTfoam_1.MeshRegions = ['/fluid/lagrangian/sprayMMHCloud', '/fluid/lagrangian/sprayMMHCloudTracks', '/fluid/lagrangian/sprayNTOCloud', '/fluid/lagrangian/sprayNTOCloudTracks']

a5CHTFCase_noHT_reHTfoam_1Display = Show(a5CHTFCase_noHT_reHTfoam_1, renderView1, 'GeometryRepresentation')

a5CHTFCase_noHT_reHTfoam_1Display.Representation = 'Surface'
a5CHTFCase_noHT_reHTfoam_1Display.ColorArrayName = [None, '']
a5CHTFCase_noHT_reHTfoam_1Display.SelectTCoordArray = 'None'
a5CHTFCase_noHT_reHTfoam_1Display.SelectNormalArray = 'None'
a5CHTFCase_noHT_reHTfoam_1Display.SelectTangentArray = 'None'
a5CHTFCase_noHT_reHTfoam_1Display.OSPRayScaleArray = 'Cp'
a5CHTFCase_noHT_reHTfoam_1Display.OSPRayScaleFunction = 'PiecewiseFunction'
a5CHTFCase_noHT_reHTfoam_1Display.SelectOrientationVectors = 'U'
a5CHTFCase_noHT_reHTfoam_1Display.ScaleFactor = 0.0006851332494989038
a5CHTFCase_noHT_reHTfoam_1Display.SelectScaleArray = 'Cp'
a5CHTFCase_noHT_reHTfoam_1Display.GlyphType = 'Arrow'
a5CHTFCase_noHT_reHTfoam_1Display.GlyphTableIndexArray = 'Cp'
a5CHTFCase_noHT_reHTfoam_1Display.GaussianRadius = 3.4256662474945186e-05
a5CHTFCase_noHT_reHTfoam_1Display.SetScaleArray = ['POINTS', 'Cp']
a5CHTFCase_noHT_reHTfoam_1Display.ScaleTransferFunction = 'PiecewiseFunction'
a5CHTFCase_noHT_reHTfoam_1Display.OpacityArray = ['POINTS', 'Cp']
a5CHTFCase_noHT_reHTfoam_1Display.OpacityTransferFunction = 'PiecewiseFunction'
a5CHTFCase_noHT_reHTfoam_1Display.DataAxesGrid = 'GridAxesRepresentation'
a5CHTFCase_noHT_reHTfoam_1Display.PolarAxes = 'PolarAxesRepresentation'
a5CHTFCase_noHT_reHTfoam_1Display.SelectInputVectors = ['POINTS', 'U']
a5CHTFCase_noHT_reHTfoam_1Display.WriteLog = ''

a5CHTFCase_noHT_reHTfoam_1Display.ScaleTransferFunction.Points = [1588.0628662109375, 0.0, 0.5, 0.0, 3925.705322265625, 1.0, 0.5, 0.0]

a5CHTFCase_noHT_reHTfoam_1Display.OpacityTransferFunction.Points = [1588.0628662109375, 0.0, 0.5, 0.0, 3925.705322265625, 1.0, 0.5, 0.0]

renderView1.Update()

ColorBy(a5CHTFCase_noHT_reHTfoam_1Display, ('FIELD', 'vtkBlockColors'))

a5CHTFCase_noHT_reHTfoam_1Display.SetScalarBarVisibility(renderView1, True)

a5CHTFCase_noHT_reHTfoam_1Display.SetRepresentationType('Points')

ColorBy(a5CHTFCase_noHT_reHTfoam_1Display, ('POINTS', 'd'))

HideScalarBarIfNotNeeded(vtkBlockColorsLUT, renderView1)

a5CHTFCase_noHT_reHTfoam_1Display.RescaleTransferFunctionToDataRange(True, False)

a5CHTFCase_noHT_reHTfoam_1Display.SetScalarBarVisibility(renderView1, True)

dTF2D = GetTransferFunction2D('d')

dLUT = GetColorTransferFunction('d')
dLUT.TransferFunction2D = dTF2D
dLUT.RGBPoints = [5.082769121145247e-07, 0.231373, 0.298039, 0.752941, 1.6855778255830955e-05, 0.865003, 0.865003, 0.865003, 3.3203279599547386e-05, 0.705882, 0.0156863, 0.14902]
dLUT.ScalarRangeInitialized = 1.0

dPWF = GetOpacityTransferFunction('d')
dPWF.Points = [5.082769121145247e-07, 0.0, 0.5, 0.0, 3.3203279599547386e-05, 1.0, 0.5, 0.0]
dPWF.ScalarRangeInitialized = 1

tLUTColorBar = GetScalarBar(tLUT, renderView1)
tLUTColorBar.Title = 'T'
tLUTColorBar.ComponentTitle = ''

tLUTColorBar.Orientation = 'Horizontal'
tLUTColorBar.WindowLocation = 'Any Location'
tLUTColorBar.Position = [0.29294850028296543, 0.6037683664649957]
tLUTColorBar.ScalarBarLength = 0.3300000000000001

tLUTColorBar.Position = [0.2816298811544991, 0.7022990492653414]
tLUTColorBar.ScalarBarLength = 0.33000000000000024

dLUTColorBar = GetScalarBar(dLUT, renderView1)
dLUTColorBar.WindowLocation = 'Upper Right Corner'
dLUTColorBar.Title = 'd'
dLUTColorBar.ComponentTitle = ''

dLUTColorBar.Orientation = 'Horizontal'
dLUTColorBar.WindowLocation = 'Any Location'
dLUTColorBar.Position = [0.2703112620260327, 0.24200518582541056]
dLUTColorBar.ScalarBarLength = 0.33


layout1 = GetLayout()


layout1.SetSize(1767, 1157)


renderView1.CameraPosition = [0.01640058762859553, 3.003515303134918e-07, 0.0650990823289702]
renderView1.CameraFocalPoint = [0.01640058762859553, 3.003515303134918e-07, -0.01723521437666746]
renderView1.CameraParallelScale = 0.021309684052540755

