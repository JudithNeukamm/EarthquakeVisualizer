import vtk
from ReadPointsCSV import ReadPointsCSV



# Define a class for the keyboard interface
class KeyboardInterface(object):
    """Keyboard interface.

    Provides a simple keyboard interface for interaction. You may
    extend this interface with keyboard shortcuts for, e.g., moving
    the slice plane(s) or manipulating the streamline seedpoints.

    """

    def __init__(self):
        self.screenshot_counter = 0
        self.render_window = None
        self.window2image_filter = None
        self.png_writer = None
        self.sliderUp = 0.3
        self.sliderDown = 0.3
        self.dNew = 0

    def keypress(self, obj, event):
        """This function captures keypress events and defines actions for
        keyboard shortcuts."""
        key = obj.GetKeySym()
        if key == "9":
            self.render_window.Render()
            self.window2image_filter.Modified()
            screenshot_filename = ("screenshot%02d.png" %
                                   (self.screenshot_counter))
            self.png_writer.SetFileName(screenshot_filename)
            self.png_writer.Write()
            print("Saved %s" % (screenshot_filename))
            self.screenshot_counter += 1
            
#         # decrease slice plane
#         elif key == "i" and self.dNew >= 0: 
#             self.dNew = self.dNew - self.sliderDown
#             slicePlane.SetExtent(0,W,0,H,self.dNew,self.dNew)
#             self.render_window.Render()
#             
#         # increase slice plane
#         elif key == "o" and self.dNew <= 15: 
#             self.dNew = self.dNew + self.sliderUp
#             slicePlane.SetExtent(0,W,0,H,self.dNew,self.dNew)
#             self.render_window.Render()
#             


# ... add color to each earthquake (point in dataset), depends on depth
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.37, 1.0, 1.0, 1.0)
colorTransferFunction.AddRGBPoint(0.68, 1.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(0.73, 1.0, 0.7, 0.0)
colorTransferFunction.AddRGBPoint(0.74, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(0.77, 0.0, 0, 1.0)
colorTransferFunction.AddRGBPoint(2.0, 0.0, 1.0, 0.0)



# Read the dataset
filename = "events2.csv"
points, scalars, tid = ReadPointsCSV().readPoints(filename) 

data = vtk.vtkPolyData()
data.SetPoints(points)
data.GetPointData().SetScalars(scalars)


mapper = vtk.vtkPolyDataMapper()
mapper.SetInput(data)
#mapper.SetColorModeToDefault()
mapper.SetLookupTable(colorTransferFunction)


actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(20)



# put spheres at each point in the dataset
ball = vtk.vtkSphereSource()
ball.SetRadius(1.0)
ball.SetThetaResolution(10)
ball.SetPhiResolution(10)

# filter that copies a geometric representation to every point in the dataset
ballGlyph = vtk.vtkGlyph3D()
ballGlyph.SetInput(data)
ballGlyph.SetSourceConnection(ball.GetOutputPort())
ballGlyph.SetScaleModeToScaleByScalar()
ballGlyph.SetColorModeToColorByScalar()
ballGlyph.SetScaleFactor(3.0)

ballMapper = vtk.vtkPolyDataMapper()
ballMapper.SetInputConnection(ballGlyph.GetOutputPort())
ballMapper.SetLookupTable(colorTransferFunction)

ballActor = vtk.vtkActor()
ballActor.SetMapper(ballMapper)



#reader = vtk.vtkStructuredPointsReader()
#reader.SetOutput(points)
#reader.SetFileName("wind.vtk")
#reader.Update()

# the range of the bounds of the data
#a,b = points.GetOutput().GetScalarRange()
#x_start, x_end, y_start, y_end, z_start, z_end = points.GetOutput().GetBounds()
#W,H,D = points.GetOutput().GetDimensions()



# # a plane for the seeds
# plane = vtk.vtkPlaneSource()
# plane.SetOrigin(x_start,math.ceil(y_start),z_start)
# plane.SetPoint1(x_end,math.ceil(y_start),z_start)
# plane.SetPoint2(x_start,math.ceil(y_start),z_end)
# plane.SetXResolution(4)
# plane.SetYResolution(6)
# 
# 
# # create the streamlines
# stream = vtk.vtkStreamLine()
# stream.SetSource(plane.GetOutput())
# stream.SetInput(reader.GetOutput())
# stream.SetIntegrationDirectionToForward()
# stream.SetIntegrator(vtk.vtkRungeKutta4())
# stream.SetStepLength(0.05)
# 
# 
# # connect streamline to mapper
# streamMapper = vtk.vtkPolyDataMapper()
# streamMapper.SetLookupTable(lut)
# streamMapper.SetInput(stream.GetOutput())
# streamMapper.SetScalarRange(a,b)
# streamActor = vtk.vtkActor()
# streamActor.SetMapper(streamMapper)
# streamActor.GetProperty().SetLineWidth(3.0)
# 
# # slice plane
# slicePlane = vtk.vtkImageDataGeometryFilter()
# slicePlane.SetInput( reader.GetOutput() )
# slicePlane.SetExtent(0,W,0,H,0,0)
# 
# slicePlaneMapper = vtk.vtkPolyDataMapper()
# slicePlaneMapper.SetLookupTable(lut)
# slicePlaneMapper.SetInput(slicePlane.GetOutput())
# slicePlaneMapper.SetScalarRange(a,b)
# 
# 
# slicePlaneActor = vtk.vtkActor()
# slicePlaneActor.SetMapper(slicePlaneMapper)
# 
# 
# 
# # add arrows to display the wind direction
# 
# arrow = vtk.vtkArrowSource()
# arrow.SetTipRadius(0.1)
# arrow.SetShaftRadius(0.02)
# 
# 
# arrowGlyph = vtk.vtkGlyph3D()
# arrowGlyph.SetInput(slicePlane.GetOutput())
# arrowGlyph.SetSourceConnection(arrow.GetOutputPort())
# 
# arrowGlyph.SetScaleModeToScaleByScalar()
# arrowGlyph.SetScaleFactor(0.1)
# 
# arrowMapper = vtk.vtkPolyDataMapper()
# arrowMapper.SetInputConnection(arrowGlyph.GetOutputPort())
# #arrowMapper.SetLookupTable(lut)
# 
# arrowActor = vtk.vtkActor()
# #arrowActor.GetProperty().SetColor(0.9,0.9,0.1)
# arrowActor.SetMapper(arrowMapper)
# 
# 
# 
# # create colorbar
# scalarBar = vtk.vtkScalarBarActor()
# scalarBar.SetLookupTable(streamMapper.GetLookupTable())
# # set properties ...
# scalarBar.SetTitle("Wind speed")
# scalarBar.GetLabelTextProperty().SetColor(0,0,1)
# scalarBar.GetTitleTextProperty().SetColor(0,0,1)
# scalarBar.SetOrientationToHorizontal()
# # ...and size
# scalarBar.SetWidth(.88)
# scalarBar.SetHeight(.12)
# # ... and position
# spc = scalarBar.GetPositionCoordinate()
# spc.SetCoordinateSystemToNormalizedViewport()
# spc.SetValue(0.05,0.05)

# add outline
outline = vtk.vtkOutlineFilter()
outline.SetInput(data) 

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInput(outline.GetOutput())
outlineActor = vtk.vtkActor()

outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetDiffuseColor(0.8, 0.8, 0.8)
outlineActor.GetProperty().SetLineWidth(2.0)


# Create a renderer and add the actors to it
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.2)
#renderer.AddActor(streamActor)
renderer.AddActor(actor)
renderer.AddActor(outlineActor)
renderer.AddActor(ballActor)
#renderer.AddActor(scalarBar)
#renderer.AddActor(slicePlaneActor)
#renderer.AddActor(arrowActor)


# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Air currents")
render_window.SetSize(800, 600)
render_window.AddRenderer(renderer)

# Create an interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Create a window-to-image filter and a PNG writer that can be used
# to take screenshots
window2image_filter = vtk.vtkWindowToImageFilter()
window2image_filter.SetInput(render_window)
png_writer = vtk.vtkPNGWriter()
png_writer.SetInput(window2image_filter.GetOutput())

# Set up the keyboard interface
keyboard_interface = KeyboardInterface()
keyboard_interface.render_window = render_window
keyboard_interface.window2image_filter = window2image_filter
keyboard_interface.png_writer = png_writer

# Connect the keyboard interface to the interactor
interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

# Initialize the interactor and start the rendering loop
interactor.Initialize()
render_window.Render()
interactor.Start()
