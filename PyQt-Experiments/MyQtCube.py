"""
Simple VTK scene in a Qt QFrame
"""

import sys
import vtk
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)

        self.frame = QtGui.QFrame()

        self.vl = QtGui.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Generate polygon data for a cube
        self.cube = vtk.vtkCubeSource()

        # Create a mapper and an actor for the cube data
        self.cube_mapper = vtk.vtkPolyDataMapper()
        self.cube_mapper.SetInput(self.cube.GetOutput())
        self.cube_actor = vtk.vtkActor()
        self.cube_actor.SetMapper(self.cube_mapper)
        self.cube_actor.GetProperty().SetColor(0.0, 1.0, 0.0)  # make the cube red

        # Create a renderer and add the cube actor to it
        self.ren.SetBackground(0.0, 0.0, 0.0)  # make the background black
        self.ren.AddActor(self.cube_actor)

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
        self.show()
        self.interactor.Initialize()


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())