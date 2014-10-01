import vtk
import time
#from ReadPointsCSV import ReadPointsCSV
from MyReader import ReadPointsCSV


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




# Read the dataset 
filename = "events3.csv"
data_dict = ReadPointsCSV().readPoints(filename)
#points, scalars, tid = ReadPointsCSV().readPoints(filename) 

#zeit = tid.getValue(0)
points = data_dict["2014-points"]
scalars = data_dict["2014-scalar"]
tid = data_dict["2014-tid"]
data = vtk.vtkPolyData()
data.SetPoints(points)
data.GetPointData().SetScalars(scalars)


'''
# filter data after time
data_filtered_according_time_slot = vtk.vtkPolyData()
for i in range(0, points.GetNumberOfPoints()):
    date = time.asctime(time.localtime(tid[0][i]))
    date_splitted = date.split(' ')
    time = date_splitted[3]
    time_splitted = time.split(':')
    hour = int(time_splitted[0])
    if 12 <= hour <= 13:
        print time_splitted[0]
'''   
    

# ... add color to each earthquake (point in dataset), depends on depth (z-value)
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(4.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(6.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(8.0, 0.58, 0.44, 0.86)


mapper = vtk.vtkPolyDataMapper()
mapper.SetInput(data)
mapper.SetLookupTable(colorTransferFunction)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(2)


# put spheres at each point in the dataset
ball = vtk.vtkSphereSource()
ball.SetRadius(0.5)
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

# add outline
outline = vtk.vtkOutlineFilter()
outline.SetInput(data) 

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInput(outline.GetOutput())

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetDiffuseColor(0.8, 0.8, 0.8)
outlineActor.GetProperty().SetLineWidth(2.0)



# add scalar bar
scalarBar = vtk.vtkScalarBarActor()
scalarBar.SetLookupTable(ballMapper.GetLookupTable())
# set properties ...
scalarBar.SetTitle("Strength")
scalarBar.GetLabelTextProperty().SetColor(0,0,1)
scalarBar.GetTitleTextProperty().SetColor(0,0,1)
# ...and size
scalarBar.SetWidth(.12)
scalarBar.SetHeight(.95)
# ... and position
spc = scalarBar.GetPositionCoordinate()
spc.SetCoordinateSystemToNormalizedViewport()
spc.SetValue(0.05,0.05)


# Create a text property for both cube axes
tprop = vtk.vtkTextProperty()
tprop.SetColor(1, 1, 1)
tprop.ShadowOn()


# Create a vtkCubeAxesActor2D. Use the outer edges of the bounding box to
# draw the axes. Add the actor to the renderer.
axes = vtk.vtkCubeAxesActor2D()
axes.SetInput(data)
#axes.SetCamera(renderer.GetActiveCamera())
axes.SetLabelFormat("%6.4g")
axes.SetFlyModeToOuterEdges()
axes.SetFontFactor(0.8)
axes.SetAxisTitleTextProperty(tprop)
axes.SetAxisLabelTextProperty(tprop)


# create a text actor
txt = vtk.vtkTextActor()
txt.SetInput("Time: " + str(2.0)) 
txtprop=txt.GetTextProperty()
txtprop.SetFontFamilyToArial()
txtprop.SetFontSize(18)
txtprop.SetColor(1,1,1)
txt.SetDisplayPosition(20,20)


# Create a renderer and add the actors to it
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.2)



# add the actors to rederer
#renderer.AddViewProp(axes)
renderer.AddActor(actor)
renderer.AddActor(outlineActor)
renderer.AddActor(ballActor)
renderer.AddActor(scalarBar)
renderer.AddActor(txt)


# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Earthquakes")
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
