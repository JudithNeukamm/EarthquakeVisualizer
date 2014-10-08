from vtk import *


class EarthquakeOutlineActor(vtkActor):

    def __init__(self, xmin=0, xmax=0, ymin=0, ymax=0, zmin=0, zmax=0):
        self.mapper = None
        self.source = None
        
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        
        self.init_mapper()

        self.SetMapper(self.mapper)
        self.GetProperty().SetDiffuseColor(0.8, 0.8, 0.8)
        self.GetProperty().SetLineWidth(2.0)
 

    def init_source(self):
        self.source = vtk.vtkOutlineSource()
        self.source.SetBonds(self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax)
 

    def init_mapper(self):
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInput(self.source)
        