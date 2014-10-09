from vtk import *


class EarthquakePlaneActor(vtkActor):
    
    def __init__(self, file_name, bounds):
        self.reader = None
        self.mapper = None
        self.texture = None
        
        self.init_reader(file_name)
        self.init_mapper(bounds)
        self.init_texture()

    def init_reader(self, file_name):
        jpg_reader = vtk.vtkJPEGReader()
        jpg_reader.SetFileName(file_name)
        self.reader = jpg_reader

    def init_texture(self):
        texture = vtk.vtkTexture()
        texture.SetInput(self.reader.GetOutput())
        texture.SetInputConnection(self.reader.GetOutputPort())
        texture.InterpolateOn()
        self.texture = texture
        self.SetTexture(self.texture)

    def init_mapper(self, bounds):
        plane = vtkPlaneSource()
        plane.SetOrigin(bounds[0], bounds[2], bounds[4])  # Xmin, Ymin, Zmin
        plane.SetPoint1(bounds[0], bounds[3], bounds[4])  # point x,y,z defining the first axis of the plane
        plane.SetPoint2(bounds[1], bounds[2], bounds[4])  # point x,y,z defining the second axis of the plane

        plane_mapper = vtk.vtkPolyDataMapper()
        plane_mapper.SetInputConnection(plane.GetOutputPort())
        self.mapper = plane_mapper
        self.SetMapper(self.mapper)