import sys
import vtk
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from KeyboardInterface import KeyboardInterface
from EarthquakeVisualization import EarthquakeVisualization


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle("Scientific Visualization 2014")

        self.frame = QtGui.QFrame()
        self.box_layout = QtGui.QHBoxLayout()

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

        # Settings Widget
        self.settings_widget = self.init_settings_widget()
        self.box_layout.addWidget(self.settings_widget)

        # Initialize the interactor and start the rendering loop
        self.render_window.Render()

        self.showMaximized()
        self.interactor.Initialize()
        self.interactor.Start()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def init_settings_widget(self):
        settings_widget = QtGui.QWidget()
        settings_widget.setMaximumWidth(200)
        vbox = QtGui.QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignTop)
        settings_widget.setLayout(vbox)

        # Movie Group
        movie_group = QtGui.QGroupBox("Automatic Data Visualization")
        movie_vbox = QtGui.QVBoxLayout()
        movie_group.setLayout(movie_vbox)

        # Button to play movie
        button1 = QtGui.QPushButton("Play Movie")
        movie_vbox.addWidget(button1)
        button1.clicked.connect(self.onPlayMovieButtonClicked)

        # ---------------------------------------------------
        # Manually Data Changes
        # ---------------------------------------------------

        year_group = QtGui.QGroupBox("Manually Data Changes")
        year_vbox = QtGui.QVBoxLayout()
        year_group.setLayout(year_vbox)

        # Year Label
        year_label = QtGui.QLabel("Year")
        year_vbox.addWidget(year_label)

        # Slider to change years
        year_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        current_year = 2014
        year_slider.setValue(current_year)
        year_slider.setMinimum(2011)
        year_slider.setMaximum(2014)
        year_slider.setTickInterval(1)
        year_slider.setSingleStep(1)
        year_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        year_vbox.addWidget(year_slider)
        #year_slider.connect(year_slider, QtCore.SIGNAL('sliderReleased()'), current_year)

        # Month Label
        month_label = QtGui.QLabel("Month")
        year_vbox.addWidget(month_label)

        # Slider
        month_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        month_slider.setMinimum(01)
        month_slider.setMaximum(12)
        month_slider.setTickInterval(1)
        month_slider.setSingleStep(1)
        month_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        year_vbox.addWidget(month_slider)

        vbox.addWidget(movie_group)
        vbox.addWidget(year_group)

        return settings_widget

    def onPlayMovieButtonClicked(self, btn):
        self.visualization.start_movie(self)

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