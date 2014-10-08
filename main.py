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

        # Visualization
        self.visualization = EarthquakeVisualization()
        self.slider_data_array = self.visualization.get_data_segments()
        self.mds_slider = None
        self.mds_label = None
        self.current_mds_value = None

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
        settings_widget.setMaximumWidth(300)
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
        # Manually Data Selection = mds
        # ---------------------------------------------------

        mds_group = QtGui.QGroupBox("Manually Data Changes")
        mds_vbox = QtGui.QVBoxLayout()
        mds_group.setLayout(mds_vbox)

        # Year Label
        mds_label = QtGui.QLabel("Selecting data by time")
        mds_vbox.addWidget(mds_label)

        # Slider to change years
        self.mds_slider = QtGui.QSlider(QtCore.Qt.Vertical, self)
        self.current_mds_value = 0
        self.mds_slider.setValue(self.current_mds_value)
        self.mds_slider.setMinimum(0)
        self.mds_slider.setMaximum(len(self.slider_data_array)-1)
        self.mds_slider.setTickInterval(1)
        self.mds_slider.setSingleStep(1)
        self.mds_slider.setTickPosition(QtGui.QSlider.TicksRight)
        mds_vbox.addWidget(self.mds_slider)

        # Current Value Label
        self.mds_label = QtGui.QLabel()
        self.on_slider_released()
        mds_vbox.addWidget(self.mds_label)

        # Slider events
        self.connect(self.mds_slider, QtCore.SIGNAL('valueChanged(int)'), self.on_slider_moved)
        self.connect(self.mds_slider, QtCore.SIGNAL('sliderReleased()'), self.on_slider_released)

        vbox.addWidget(movie_group)
        vbox.addWidget(mds_group)

        return settings_widget

    def on_slider_moved(self, value):
        data_selection = self.slider_data_array[value]
        self.mds_label.setText("Current selection: %s" % data_selection)

        self.visualization.set_data_segment(data_selection)
        self.render_window.Render()

    def on_slider_released(self):
        self.current_mds_value = self.mds_slider.value()
        data_selection = self.slider_data_array[self.current_mds_value]
        self.mds_label.setText("Current selection: %s" % data_selection)

        self.visualization.set_data_segment(data_selection)
        self.render_window.Render()

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