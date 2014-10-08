from vtk import *


class EarthquakeOutlineActor(vtkActor):

    def __init__(self, boundTuple):
        self.mapper = None
        self.source = None
        
        self.xmin = boundTuple[0]
        self.xmax = boundTuple[1]
        self.ymin = boundTuple[2]
        self.ymax = boundTuple[3]
        self.zmin = boundTuple[4]
        self.zmax = boundTuple[5]

        self.init_source()
        self.init_mapper()

        self.GetProperty().SetDiffuseColor(1, 0, 0)
        #self.GetProperty().SetDiffuseColor(0.8, 0.8, 0.8)
        self.GetProperty().SetLineWidth(2.0)

    def init_source(self):
        self.source = vtk.vtkOutlineSource()
        self.source.SetBounds(self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax)

    def init_mapper(self):
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInput(self.source.GetOutput())
        self.SetMapper(self.mapper)