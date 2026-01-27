# trace generated using paraview version 5.11.2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
a5CHTFCase_noHT_reHTfoam = GetActiveSource()

# Properties modified on a5CHTFCase_noHT_reHTfoam
a5CHTFCase_noHT_reHTfoam.CaseType = 'Decomposed Case'

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
a5CHTFCase_noHT_reHTfoamDisplay = Show(a5CHTFCase_noHT_reHTfoam, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
a5CHTFCase_noHT_reHTfoamDisplay.Representation = 'Surface'
a5CHTFCase_noHT_reHTfoamDisplay.ColorArrayName = [None, '']
a5CHTFCase_noHT_reHTfoamDisplay.SelectTCoordArray = 'None'
a5CHTFCase_noHT_reHTfoamDisplay.SelectNormalArray = 'None'
a5CHTFCase_noHT_reHTfoamDisplay.SelectTangentArray = 'None'
a5CHTFCase_noHT_reHTfoamDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
a5CHTFCase_noHT_reHTfoamDisplay.SelectOrientationVectors = 'None'
a5CHTFCase_noHT_reHTfoamDisplay.ScaleFactor = -2.0000000000000002e+298
a5CHTFCase_noHT_reHTfoamDisplay.SelectScaleArray = 'None'
a5CHTFCase_noHT_reHTfoamDisplay.GlyphType = 'Arrow'
a5CHTFCase_noHT_reHTfoamDisplay.GlyphTableIndexArray = 'None'
a5CHTFCase_noHT_reHTfoamDisplay.GaussianRadius = -1e+297
a5CHTFCase_noHT_reHTfoamDisplay.SetScaleArray = [None, '']
a5CHTFCase_noHT_reHTfoamDisplay.ScaleTransferFunction = 'PiecewiseFunction'
a5CHTFCase_noHT_reHTfoamDisplay.OpacityArray = [None, '']
a5CHTFCase_noHT_reHTfoamDisplay.OpacityTransferFunction = 'PiecewiseFunction'
a5CHTFCase_noHT_reHTfoamDisplay.DataAxesGrid = 'GridAxesRepresentation'
a5CHTFCase_noHT_reHTfoamDisplay.PolarAxes = 'PolarAxesRepresentation'
a5CHTFCase_noHT_reHTfoamDisplay.SelectInputVectors = [None, '']
a5CHTFCase_noHT_reHTfoamDisplay.WriteLog = ''

# reset view to fit data
renderView1.ResetCamera(False)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# get animation scene
animationScene1 = GetAnimationScene()

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on a5CHTFCase_noHT_reHTfoam
a5CHTFCase_noHT_reHTfoam.CaseType = 'Reconstructed Case'

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# update the view to ensure updated data information
renderView1.Update()

renderView1.ResetActiveCameraToNegativeZ()

# reset view to fit data
renderView1.ResetCamera(False)

# Properties modified on animationScene1
animationScene1.AnimationTime = 0.02

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=a5CHTFCase_noHT_reHTfoam)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.01640058762859553, 3.003515303134918e-07, 0.0]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [0.01640058762859553, 3.003515303134918e-07, 0.0]

# Properties modified on slice1.SliceType
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# show data in view
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# get 2D transfer function for 'p'
pTF2D = GetTransferFunction2D('p')

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')
pLUT.TransferFunction2D = pTF2D
pLUT.RGBPoints = [2049.45263671875, 0.231373, 0.298039, 0.752941, 487197.7263183594, 0.865003, 0.865003, 0.865003, 972346.0, 0.705882, 0.0156863, 0.14902]
pLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'p']
slice1Display.LookupTable = pLUT
slice1Display.SelectTCoordArray = 'None'
slice1Display.SelectNormalArray = 'None'
slice1Display.SelectTangentArray = 'None'
slice1Display.OSPRayScaleArray = 'p'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'None'
slice1Display.ScaleFactor = 0.0035200013080611825
slice1Display.SelectScaleArray = 'p'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'p'
slice1Display.GaussianRadius = 0.00017600006540305913
slice1Display.SetScaleArray = ['POINTS', 'p']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'p']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'
slice1Display.SelectInputVectors = ['POINTS', 'U']
slice1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
slice1Display.ScaleTransferFunction.Points = [2049.45263671875, 0.0, 0.5, 0.0, 972346.0, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
slice1Display.OpacityTransferFunction.Points = [2049.45263671875, 0.0, 0.5, 0.0, 972346.0, 1.0, 0.5, 0.0]

# hide data in view
Hide(a5CHTFCase_noHT_reHTfoam, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')
pPWF.Points = [2049.45263671875, 0.0, 0.5, 0.0, 972346.0, 1.0, 0.5, 0.0]
pPWF.ScalarRangeInitialized = 1

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)

# create a new 'OpenFOAMReader'
a5CHTFCase_noHT_reHTfoam_1 = OpenFOAMReader(registrationName='5.CHTFCase_noHT_reHT.foam', FileName='/home/user1/OpenFOAM/user1-v2212/run/jskang/KARI/250214/CHTF/5.CHTFCase_noHT_reHT/5.CHTFCase_noHT_reHT.foam')
a5CHTFCase_noHT_reHTfoam_1.MeshRegions = ['/filmRegion/internalMesh', '/fluid/internalMesh', '/fluid/lagrangian/sprayMMHCloudTracks', '/fluid/lagrangian/sprayNTOCloudTracks', '/fluid/lagrangian/sprayMMHCloud', '/fluid/lagrangian/sprayNTOCloud', '/header/internalMesh', '/thruster/internalMesh']
a5CHTFCase_noHT_reHTfoam_1.CellArrays = ['AR', 'CH3', 'CH3NHNH2', 'CH3NN', 'CH3NNH', 'CH3NNH2', 'CH3O', 'CH4', 'CO', 'CO2', 'H', 'H2', 'H2CN', 'H2O', 'HCN', 'HNC', 'HNCO', 'HNO3', 'HONO', 'Mach', 'N', 'N2', 'N2O4', 'NH', 'NH2', 'NH3', 'NO', 'NO2', 'O', 'O2', 'OH', 'T', 'U', 'alphat', 'dQ', 'k', 'nut', 'omega', 'p', 'rho', 'sprayMMHCloud:UCoeff', 'sprayMMHCloud:UTrans', 'sprayMMHCloud:hsCoeff', 'sprayMMHCloud:hsTrans', 'sprayMMHCloud:rhoTrans_AR', 'sprayMMHCloud:rhoTrans_CH3', 'sprayMMHCloud:rhoTrans_CH3NHNH2', 'sprayMMHCloud:rhoTrans_CH3NN', 'sprayMMHCloud:rhoTrans_CH3NNH', 'sprayMMHCloud:rhoTrans_CH3NNH2', 'sprayMMHCloud:rhoTrans_CH3O', 'sprayMMHCloud:rhoTrans_CH4', 'sprayMMHCloud:rhoTrans_CO', 'sprayMMHCloud:rhoTrans_CO2', 'sprayMMHCloud:rhoTrans_H', 'sprayMMHCloud:rhoTrans_H2', 'sprayMMHCloud:rhoTrans_H2CN', 'sprayMMHCloud:rhoTrans_H2O', 'sprayMMHCloud:rhoTrans_HCN', 'sprayMMHCloud:rhoTrans_HNC', 'sprayMMHCloud:rhoTrans_HNCO', 'sprayMMHCloud:rhoTrans_HNO3', 'sprayMMHCloud:rhoTrans_HONO', 'sprayMMHCloud:rhoTrans_N', 'sprayMMHCloud:rhoTrans_N2', 'sprayMMHCloud:rhoTrans_N2O4', 'sprayMMHCloud:rhoTrans_NH', 'sprayMMHCloud:rhoTrans_NH2', 'sprayMMHCloud:rhoTrans_NH3', 'sprayMMHCloud:rhoTrans_NO', 'sprayMMHCloud:rhoTrans_NO2', 'sprayMMHCloud:rhoTrans_O', 'sprayMMHCloud:rhoTrans_O2', 'sprayMMHCloud:rhoTrans_OH', 'sprayNTOCloud:UCoeff', 'sprayNTOCloud:UTrans', 'sprayNTOCloud:hsCoeff', 'sprayNTOCloud:hsTrans', 'sprayNTOCloud:rhoTrans_AR', 'sprayNTOCloud:rhoTrans_CH3', 'sprayNTOCloud:rhoTrans_CH3NHNH2', 'sprayNTOCloud:rhoTrans_CH3NN', 'sprayNTOCloud:rhoTrans_CH3NNH', 'sprayNTOCloud:rhoTrans_CH3NNH2', 'sprayNTOCloud:rhoTrans_CH3O', 'sprayNTOCloud:rhoTrans_CH4', 'sprayNTOCloud:rhoTrans_CO', 'sprayNTOCloud:rhoTrans_CO2', 'sprayNTOCloud:rhoTrans_H', 'sprayNTOCloud:rhoTrans_H2', 'sprayNTOCloud:rhoTrans_H2CN', 'sprayNTOCloud:rhoTrans_H2O', 'sprayNTOCloud:rhoTrans_HCN', 'sprayNTOCloud:rhoTrans_HNC', 'sprayNTOCloud:rhoTrans_HNCO', 'sprayNTOCloud:rhoTrans_HNO3', 'sprayNTOCloud:rhoTrans_HONO', 'sprayNTOCloud:rhoTrans_N', 'sprayNTOCloud:rhoTrans_N2', 'sprayNTOCloud:rhoTrans_N2O4', 'sprayNTOCloud:rhoTrans_NH', 'sprayNTOCloud:rhoTrans_NH2', 'sprayNTOCloud:rhoTrans_NH3', 'sprayNTOCloud:rhoTrans_NO', 'sprayNTOCloud:rhoTrans_NO2', 'sprayNTOCloud:rhoTrans_O', 'sprayNTOCloud:rhoTrans_O2', 'sprayNTOCloud:rhoTrans_OH']
a5CHTFCase_noHT_reHTfoam_1.LagrangianArrays = ['Cp', 'KHindex', 'Nu', 'Re', 'T', 'Tfg', 'U', 'UCorrect', 'UTurb', 'We', 'YCH3NHNH2(l)', 'YN2O4(l)', 'active', 'age', 'd', 'd0', 'dTarget', 'htc', 'injector', 'liquidCore', 'mass0', 'ms', 'mu', 'nParticle', 'origId', 'origProcId', 'position0', 'rho', 'sigma', 'tMom', 'tTurb', 'tc', 'typeId', 'user', 'y', 'yDot']

# Properties modified on a5CHTFCase_noHT_reHTfoam_1
a5CHTFCase_noHT_reHTfoam_1.MeshRegions = ['/fluid/lagrangian/sprayMMHCloud', '/fluid/lagrangian/sprayMMHCloudTracks', '/fluid/lagrangian/sprayNTOCloud', '/fluid/lagrangian/sprayNTOCloudTracks']

# show data in view
a5CHTFCase_noHT_reHTfoam_1Display = Show(a5CHTFCase_noHT_reHTfoam_1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
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

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
a5CHTFCase_noHT_reHTfoam_1Display.ScaleTransferFunction.Points = [1588.0628662109375, 0.0, 0.5, 0.0, 3925.705322265625, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
a5CHTFCase_noHT_reHTfoam_1Display.OpacityTransferFunction.Points = [1588.0628662109375, 0.0, 0.5, 0.0, 3925.705322265625, 1.0, 0.5, 0.0]

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(a5CHTFCase_noHT_reHTfoam_1Display, ('FIELD', 'vtkBlockColors'))

# show color bar/color legend
a5CHTFCase_noHT_reHTfoam_1Display.SetScalarBarVisibility(renderView1, True)

# get 2D transfer function for 'vtkBlockColors'
vtkBlockColorsTF2D = GetTransferFunction2D('vtkBlockColors')

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')
vtkBlockColorsLUT.InterpretValuesAsCategories = 1
vtkBlockColorsLUT.AnnotationsInitialized = 1
vtkBlockColorsLUT.TransferFunction2D = vtkBlockColorsTF2D
vtkBlockColorsLUT.Annotations = ['0', '0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9', '10', '10', '11', '11']
vtkBlockColorsLUT.ActiveAnnotatedValues = ['0', '1', '2', '3']
vtkBlockColorsLUT.IndexedColors = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.63, 0.63, 1.0, 0.67, 0.5, 0.33, 1.0, 0.5, 0.75, 0.53, 0.35, 0.7, 1.0, 0.75, 0.5]

# get opacity transfer function/opacity map for 'vtkBlockColors'
vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')

# change representation type
a5CHTFCase_noHT_reHTfoam_1Display.SetRepresentationType('Points')

# set scalar coloring
ColorBy(a5CHTFCase_noHT_reHTfoam_1Display, ('CELLS', 'd'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(vtkBlockColorsLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
a5CHTFCase_noHT_reHTfoam_1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
a5CHTFCase_noHT_reHTfoam_1Display.SetScalarBarVisibility(renderView1, True)

# get 2D transfer function for 'd'
dTF2D = GetTransferFunction2D('d')

# get color transfer function/color map for 'd'
dLUT = GetColorTransferFunction('d')
dLUT.TransferFunction2D = dTF2D
dLUT.RGBPoints = [5.082769121145247e-07, 0.231373, 0.298039, 0.752941, 1.6855778255830955e-05, 0.865003, 0.865003, 0.865003, 3.3203279599547386e-05, 0.705882, 0.0156863, 0.14902]
dLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'd'
dPWF = GetOpacityTransferFunction('d')
dPWF.Points = [5.082769121145247e-07, 0.0, 0.5, 0.0, 3.3203279599547386e-05, 1.0, 0.5, 0.0]
dPWF.ScalarRangeInitialized = 1

# get color legend/bar for dLUT in view renderView1
dLUTColorBar = GetScalarBar(dLUT, renderView1)
dLUTColorBar.WindowLocation = 'Upper Right Corner'
dLUTColorBar.Title = 'd'
dLUTColorBar.ComponentTitle = ''

# change scalar bar placement
dLUTColorBar.Orientation = 'Horizontal'
dLUTColorBar.WindowLocation = 'Any Location'
dLUTColorBar.Position = [0.2754046406338425, 0.2658254105445118]
dLUTColorBar.ScalarBarLength = 0.33000000000000007

# get color legend/bar for pLUT in view renderView1
pLUTColorBar = GetScalarBar(pLUT, renderView1)
pLUTColorBar.Title = 'p'
pLUTColorBar.ComponentTitle = ''

# change scalar bar placement
pLUTColorBar.Orientation = 'Horizontal'
pLUTColorBar.WindowLocation = 'Any Location'
pLUTColorBar.Position = [0.2448443689869838, 0.6746413137424375]
pLUTColorBar.ScalarBarLength = 0.32999999999999974

# change scalar bar placement
pLUTColorBar.Position = [0.25842671194114336, 0.7022990492653416]
pLUTColorBar.ScalarBarLength = 0.32999999999999957

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

# get layout
layout1 = GetLayout()

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1767, 1157)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [0.01640058762859553, 3.003515303134918e-07, 0.0657670468215175]
renderView1.CameraFocalPoint = [0.01640058762859553, 3.003515303134918e-07, -0.01656724988412014]
renderView1.CameraParallelScale = 0.021309684052540755

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).