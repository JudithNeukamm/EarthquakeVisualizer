from vtk import *


class EarthquakeBallGlyphActor(vtkActor):

    def __init__(self, data):
        self.source = None
        self.data = data
        self.filter = None
        self.mapper = None

        self.init_source()
        self.init_filter()
        self.init_mapper()

        self.SetMapper(self.mapper)

    def init_source(self):
        # put spheres at each point in the dataset
        ball = vtk.vtkSphereSource()
        ball.SetRadius(0.5)
        ball.SetThetaResolution(10)
        ball.SetPhiResolution(10)
        self.source = ball

    def init_filter(self):
        # filter that copies a geometric representation to every point in the dataset
        ball_glyph = vtk.vtkGlyph3D()
        ball_glyph.SetInput(self.data)
        ball_glyph.SetSourceConnection(self.source.GetOutputPort())
        ball_glyph.SetScaleModeToScaleByScalar()
        ball_glyph.SetColorModeToColorByScalar()
        ball_glyph.SetScaleFactor(3.0)
        self.filter = ball_glyph

    def init_mapper(self):
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.filter.GetOutputPort())

    def set_color_transfer_function(self, color_transfer_function):
        self.mapper.SetLookupTable(color_transfer_function)

    def set_data(self, data):
        self.data = data
        self.filter.SetInput(self.data)

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