import vtk
from KeyboardInterface import KeyboardInterface
from MyReader import ReadPointsCSV
from EarthquakeOutlineActor import *
from EarthquakeBallGlyphActor import *


class EarthquakeVisualization:

    def __init__(self):
        self.data = vtk.vtkPolyData()
        self.data_dict = {}
        self.data_segments = []
        self.mapper = None
        self.actors = {}
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
        self.data_dict = ReadPointsCSV().readPoints("data/events3.csv")

        points = self.data_dict["2013"]["09"]['points']
        scalars = self.data_dict["2013"]["09"]['scalar']
        # tid = data_dict["2013"]["09"]["tid"]
        self.data.SetPoints(points)
        self.data.GetPointData().SetScalars(scalars)

    def get_data_segments(self):
        if len(self.data_segments):
            return self.data_segments
        else:
            segments = []
            all_years_available = self.data_dict.keys()
            all_years_available.sort()

            for year in all_years_available:

                all_months_available = self.data_dict[year].keys()
                all_months_available.sort()

                for month in all_months_available:
                    segments.append(month+"/"+year)

            self.data_segments = segments
            return self.data_segments

    def set_data_segment(self, segment_string):
        # Data segment interpretation
        month = segment_string[:2]
        year = segment_string[3:7]

        # Update data segment
        self.data.SetPoints(self.data_dict[year][month]['points'])
        self.data.GetPointData().SetScalars(self.data_dict[year][month]['scalar'])

        # Update visualization
        self.actors['glyph_actor'].set_data(self.data)

    def init_mapper(self):
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInput(self.data)
        self.mapper.SetLookupTable(self.colorTransferFunction)

    def init_actors(self):

        # add visualization actor
        actor = vtk.vtkActor()
        actor.SetMapper(self.mapper)
        actor.GetProperty().SetPointSize(2)
        self.actors['visualization_actor'] = actor

        # add BallGlyphs with scalar bar
        ball_actor = EarthquakeBallGlyphActor(self.data)
        ball_actor.set_color_transfer_function(self.colorTransferFunction)
        self.actors['glyph_actor'] = ball_actor

        scalar_bar_actor = ball_actor.get_scalar_bar()
        self.actors['glyph_actor_scalar_bar'] = scalar_bar_actor

        # add outline
        outline_actor = EarthquakeOutlineActor(self.data)
        self.actors['outline'] = outline_actor

    def init_renderer(self):
        # Create a renderer and add the actors to it
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.2, 0.2, 0.2)

        # add the actors to renderer
        for key in self.actors.keys():
            self.renderer.AddActor(self.actors[key])

    def get_renderer(self):
        return self.renderer

    def visualize(self):
        self.init_reader()
        self.init_mapper()
        self.init_actors()
        self.init_renderer()

        # Create a text property for both cube axes
        text_prop = vtk.vtkTextProperty()
        text_prop.SetColor(1, 1, 1)
        text_prop.ShadowOn()

        # Create a vtkCubeAxesActor2D. Use the outer edges of the bounding box to
        # draw the axes. Add the actor to the renderer.
        axes = vtk.vtkCubeAxesActor2D()
        axes.SetInput(self.data)
        #axes.SetCamera(renderer.GetActiveCamera())
        axes.SetLabelFormat("%6.4g")
        axes.SetFlyModeToOuterEdges()
        axes.SetFontFactor(0.8)
        axes.SetAxisTitleTextProperty(text_prop)
        axes.SetAxisLabelTextProperty(text_prop)

        # create a text actor
        txt = vtk.vtkTextActor()
        txt.SetInput("Time: " + str(2.0))
        txt_prop = txt.GetTextProperty()
        txt_prop.SetFontFamilyToArial()
        txt_prop.SetFontSize(18)
        txt_prop.SetColor(1, 1, 1)
        txt.SetDisplayPosition(20, 20)
        self.renderer.AddActor(txt)

    def start_movie(self, main_window):
        print "EarthquakeVisualization.py: start_movie()"
        # going through every year and month and display data

        all_years_available = self.data_dict.keys()
        all_years_available.sort()

        for year in all_years_available:

            all_months_available = self.data_dict[year].keys()
            all_months_available.sort()

            for month in all_months_available:
                print "Movie is in " + year + "/" + month
                points = self.data_dict[str(year)][str(month)]['points']
                scalars = self.data_dict[str(year)][str(month)]['scalar']
                #tid = self.data_dict[str(year)][str(month)]['tid']

                self.data.SetPoints(points)
                self.data.GetPointData().SetScalars(scalars)
                self.actors['glyph_actor'].set_data(self.data)
                main_window.render_window.Render()