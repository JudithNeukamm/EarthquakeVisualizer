import sys
import vtk
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from KeyboardInterface import KeyboardInterface
from EarthquakeVisualization import EarthquakeVisualization


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle("Scientific Visualization 2014")

        self.frame = QtGui.QFrame()
        self.box_layout = QtGui.QVBoxLayout()

        menu_bar = QtGui.QMenuBar()
        self.box_layout.setMenuBar(menu_bar)

        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.box_layout.addWidget(self.vtkWidget)

        self.visualization = EarthquakeVisualization()
        self.render_window = self.vtkWidget.GetRenderWindow()
        self.render_window.AddRenderer(self.visualization.get_renderer())
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.frame.setLayout(self.box_layout)
        self.setCentralWidget(self.frame)

        # Create a window-to-image filter and a PNG writer that can be used
        # to take screenshots
        window2image_filter = vtk.vtkWindowToImageFilter()
        window2image_filter.SetInput(self.render_window)
        png_writer = vtk.vtkPNGWriter()
        png_writer.SetInput(window2image_filter.GetOutput())

        # Set up the keyboard interface
        keyboard_interface = KeyboardInterface()
        keyboard_interface.render_window = self.render_window
        keyboard_interface.window2image_filter = window2image_filter
        keyboard_interface.png_writer = png_writer

        # Connect the keyboard interface to the interactor
        self.interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)

        # Button to play movie
        button1 = QtGui.QPushButton("Play Movie")
        self.box_layout.addWidget(button1)
        button1.clicked.connect(self.onPlayMovieButtonClicked)

        # Initialize the interactor and start the rendering loop
        self.do_renering()

        self.showMaximized()
        self.interactor.Initialize()
        self.interactor.Start()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def do_renering(self):
         self.render_window.Render()

    def onPlayMovieButtonClicked(self, btn):
        self.visualization.start_movie(self)

    def keyPressEvent(self, event):
        print "Test"
        if type(event) == QtGui.QKeyEvent:
            #here accept the event and do something
            print event.key()
            event.accept()
        else:
            event.ignore()

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())