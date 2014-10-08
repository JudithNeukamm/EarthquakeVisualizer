from vtk import *


class EarthquakePlaneActor(vtkImageActor):
    
    def __init__(self, file_name):
        self.pic = file_name
        self.jpg_reader = None
        
        self.init_reader()
        self.init_mapper()

    def set_bounds(self, bounds):
        self.SetDisplayExtent(bounds)

    def init_reader(self):
        jpg_reader = vtk.vtkJPEGReader()
        jpg_reader.SetFileName(self.pic)
        self.jpg_reader = jpg_reader

    def init_mapper(self):
        self.GetMapper().SetInputConnection(self.jpg_reader.GetOutputPort())