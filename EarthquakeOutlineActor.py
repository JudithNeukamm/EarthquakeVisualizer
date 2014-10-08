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
        
        
        
        jpg_reader = vtk.vtkJPEGReader()
        jpg_reader.SetFileName('map.jpg')
        
        #ia = vtk.vtkImageActor()
        #ia.GetMapper().SetInputConnection(jpg_reader.GetOutputPort())
        
        
        picker = vtk.vtkCellPicker()
        picker.SetTolerance(0.005)

        planeWidgetX = vtk.vtkImagePlaneWidget()
        planeWidgetX.DisplayTextOn()
        planeWidgetX.SetInput(jpg_reader.GetOutput())
        planeWidgetX.SetPlaneOrientationToXAxes()
        planeWidgetX.SetSliceIndex(32)
        planeWidgetX.SetPicker(picker)
       
        prop1 = planeWidgetX.GetPlaneProperty()
        prop1.SetColor(1, 0, 0)

    def init_mapper(self):
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInput(self.filter.GetOutput())
        