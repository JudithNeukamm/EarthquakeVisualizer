import vtk
from KeyboardInterface import KeyboardInterface
from MyReader import ReadPointsCSV
from EarthquakeOutlineActor import *
from EarthquakeBallGlyphActor import *


class EarthquakeVisualization:

    def __init__(self):
        self.data = vtk.vtkPolyData()
        self.data_dict = None
        self.mapper = None
        self.actors = []
        self.renderer = None

        # ... add color to each earthquake (point in dataset), depends on depth (z-value)
        self.colorTransferFunction = vtk.vtkColorTransferFunction()
        self.colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
        self.colorTransferFunction.AddRGBPoint(4.0, 0.0, 1.0, 0.0)
        self.colorTransferFunction.AddRGBPoint(6.0, 1.0, 0.0, 0.0)
        self.colorTransferFunction.AddRGBPoint(8.0, 0.58, 0.44, 0.86)

        self.visualize()

    def init_reader(self):
        # Read the dataset
        data_dict = ReadPointsCSV().readPoints("data/events3.csv")

        points = data_dict["2013"]["09"]['points']
        scalars = data_dict["2013"]["09"]['scalar']
        # tid = data_dict["2013"]["09"]["tid"]

        self.data.SetPoints(points)
        self.data.GetPointData().SetScalars(scalars)

    def init_mapper(self):
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInput(self.data)
        self.mapper.SetLookupTable(self.colorTransferFunction)

    def init_actors(self):

        # add visualization actor
        actor = vtk.vtkActor()
        actor.SetMapper(self.mapper)
        actor.GetProperty().SetPointSize(2)
        self.actors.append(actor)

        # add BallGlyphs with scalar bar
        ball_actor = EarthquakeBallGlyphActor(self.data)
        ball_actor.set_color_transfer_function(self.colorTransferFunction)
        self.actors.append(ball_actor)

        scalar_bar_actor = ball_actor.get_scalar_bar()
        self.actors.append(scalar_bar_actor)

        # add outline
        outline_actor = EarthquakeOutlineActor(self.data)
        self.actors.append(outline_actor)

    def init_renderer(self):
        # Create a renderer and add the actors to it
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.2, 0.2, 0.2)

        # add the actors to renderer
        for actor in self.actors:
            self.renderer.AddActor(actor)

    def get_renderer(self):
        return self.renderer

    def visualize(self):
        self.init_reader()
        self.init_mapper()
        self.init_actors()
        self.init_renderer()

        # Create a text property for both cube axes
        textProp = vtk.vtkTextProperty()
        textProp.SetColor(1, 1, 1)
        textProp.ShadowOn()

        # Create a vtkCubeAxesActor2D. Use the outer edges of the bounding box to
        # draw the axes. Add the actor to the renderer.
        axes = vtk.vtkCubeAxesActor2D()
        axes.SetInput(self.data)
        #axes.SetCamera(renderer.GetActiveCamera())
        axes.SetLabelFormat("%6.4g")
        axes.SetFlyModeToOuterEdges()
        axes.SetFontFactor(0.8)
        axes.SetAxisTitleTextProperty(textProp)
        axes.SetAxisLabelTextProperty(textProp)

        # create a text actor
        txt = vtk.vtkTextActor()
        txt.SetInput("Time: " + str(2.0))
        txtprop = txt.GetTextProperty()
        txtprop.SetFontFamilyToArial()
        txtprop.SetFontSize(18)
        txtprop.SetColor(1, 1, 1)
        txt.SetDisplayPosition(20, 20)
        self.renderer.AddActor(txt)

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
