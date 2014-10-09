from vtk import *


class EarthquakeOutlineActor(vtkActor):

    def __init__(self, bound_tuple):
        self.mapper = None
        self.source = None

        self.init_source(bound_tuple)
        self.init_mapper()

        self.GetProperty().SetDiffuseColor(0.701, 0.701, 0.701)  # Aluminium
        self.GetProperty().SetLineWidth(2.0)

    def init_source(self, bound_tuple):
        source = vtk.vtkOutlineSource()

        x_min = bound_tuple[0]
        x_max = bound_tuple[1]
        y_min = bound_tuple[2]
        y_max = bound_tuple[3]
        z_min = bound_tuple[4]
        z_max = bound_tuple[5]
        source.SetBounds(x_min, x_max, y_min, y_max, z_min, z_max)

        self.source = source

    def init_mapper(self):
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInput(self.source.GetOutput())
        self.SetMapper(self.mapper)