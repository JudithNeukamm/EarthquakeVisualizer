from vtk import *


class EarthquakeBallGlyphActor(vtkActor):

    def __init__(self, data):
        self.source = None
        self.filter = None
        self.mapper = None

        self.init_source()
        self.init_filter(data)
        self.init_mapper()

        self.SetMapper(self.mapper)

    def init_source(self):
        # put spheres at each point in the dataset
        ball = vtk.vtkSphereSource()
        ball.SetRadius(0.5)
        ball.SetThetaResolution(10)
        ball.SetPhiResolution(10)
        self.source = ball

    def init_filter(self, data):
        # filter that copies a geometric representation to every point in the dataset
        ballGlyph = vtk.vtkGlyph3D()
        ballGlyph.SetInput(data)
        ballGlyph.SetSourceConnection(self.source.GetOutputPort())
        ballGlyph.SetScaleModeToScaleByScalar()
        ballGlyph.SetColorModeToColorByScalar()
        ballGlyph.SetScaleFactor(3.0)
        self.filter = ballGlyph

    def init_mapper(self):
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.filter.GetOutputPort())

    def set_color_transfer_function(self, color_transfer_function):
        self.mapper.SetLookupTable(color_transfer_function)

    def get_scalar_bar(self):
         # create scalar bar
        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetLookupTable(self.mapper.GetLookupTable())

        # set properties ...
        scalar_bar.SetTitle("Strength")
        scalar_bar.GetLabelTextProperty().SetColor(0, 0, 1)
        scalar_bar.GetTitleTextProperty().SetColor(0, 0, 1)

        # ...and size
        scalar_bar.SetWidth(.12)
        scalar_bar.SetHeight(.95)

        # ... and position
        spc = scalar_bar.GetPositionCoordinate()
        spc.SetCoordinateSystemToNormalizedViewport()
        spc.SetValue(0.05, 0.05)

        return scalar_bar

    def start_movie(self):
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

                self.filter.SetInput(self.data)
                # render_window.Render() has to be called in main