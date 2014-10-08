from vtk import *


class EarthquakePlaneActor(vtkImageActor):
    
    def __init__(self, file_name):
        self.pic = file_name
        self.jpg_reader = None
        
        self.init_mapReader()
        
        self.GetMapper().SetInputConnection(self.jpg_reader.GetOutputPort())

        
        
    def init_mapReader(self):
        jpg_reader = vtk.vtkJPEGReader()
        jpg_reader.SetFileName(self.pic)
        self.jpg_reader = jpg_reader 