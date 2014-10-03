from vtk import *


class EarthquakeOutlineActor(vtkActor):

    def __init__(self, data):
        self.filter = None
        self.mapper = None

        self.init_filter(data)
        self.init_mapper()

        self.SetMapper(self.mapper)
        self.GetProperty().SetDiffuseColor(0.8, 0.8, 0.8)
        self.GetProperty().SetLineWidth(2.0)

    def init_filter(self, data):
        self.filter = vtk.vtkOutlineFilter()
        self.filter.SetInput(data)

    def init_mapper(self):
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInput(self.filter.GetOutput())