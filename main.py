import sys
import vtk
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from KeyboardInterface import KeyboardInterface
from EarthquakeVisualization import EarthquakeVisualization


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)

        self.frame = QtGui.QFrame()
        self.vl = QtGui.QVBoxLayout()

        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)

        visualization = EarthquakeVisualization()
        self.ren = visualization.get_renderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        self.show()
        self.interactor.Initialize()


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())