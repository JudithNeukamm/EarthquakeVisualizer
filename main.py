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

        self.root_layout = QtGui.QVBoxLayout()

        self.box_layout = QtGui.QHBoxLayout()
        self.root_layout.addLayout(self.box_layout)

        #menu_bar = QtGui.QMenuBar()
        #self.box_layout.setMenuBar(menu_bar)

        self.frame = QtGui.QFrame()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.box_layout.addWidget(self.vtkWidget)

        # Visualization
        self.visualization = EarthquakeVisualization()
        self.slider_data_array = self.visualization.get_data_segments()
        self.mds_slider = None
        self.mds_label = None
        self.current_mds_value = None
        self.strength_min_box = None
        self.strength_max_box = None
        self.opacity_slider = None
        self.opacity_value_label = None

        self.render_window = self.vtkWidget.GetRenderWindow()
        self.render_window.AddRenderer(self.visualization.get_renderer())
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.frame.setLayout(self.root_layout)
        self.setCentralWidget(self.frame)

        # Settings Widget
        self.settings_widget = self.init_settings_widget()
        self.box_layout.addWidget(self.settings_widget)

        # Bottom Widget
        self.bottom_widget = self.init_bottom_widget()
        self.root_layout.addWidget(self.bottom_widget)

        # Initialize the interactor and start the rendering loop
        self.render_window.Render()

        self.showMaximized()
        self.interactor.Initialize()
        self.interactor.Start()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def init_bottom_widget(self):
        bottom_widget = QtGui.QWidget()
        bottom_widget.setMaximumHeight(300)
        vbox = QtGui.QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignTop)
        bottom_widget.setLayout(vbox)

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
        self.mds_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
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

        vbox.addWidget(mds_group)

        return bottom_widget

    def init_settings_widget(self):
        settings_widget = QtGui.QWidget()
        settings_widget.setMaximumWidth(300)
        vbox = QtGui.QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignTop)
        settings_widget.setLayout(vbox)

        # ---------------------------------------------------
        # Movie Group
        # ---------------------------------------------------

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
        self.mds_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
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


        # ---------------------------------------------------
        # Strength Group
        # ---------------------------------------------------
        strength_group = QtGui.QGroupBox("Filter earthquakes a min/max strength value")
        strength_vbox = QtGui.QVBoxLayout()
        strength_group.setLayout(strength_vbox)

        spinbox_layout = QtGui.QHBoxLayout()
        min, max = self.visualization.get_strength_range()

        self.strength_min_box = QtGui.QDoubleSpinBox(self)
        self.strength_min_box.setRange(0.00, 10.00)
        self.strength_min_box.setValue(min)
        spinbox_layout.addWidget(self.strength_min_box)

        self.strength_max_box = QtGui.QDoubleSpinBox(self)
        self.strength_max_box.setRange(0.00, 10.00)
        self.strength_max_box.setValue(max)
        spinbox_layout.addWidget(self.strength_max_box)

        strength_apply_btn = QtGui.QPushButton("Apply strength range")
        strength_apply_btn.clicked.connect(self.on_strength_filter_applied)

        strength_vbox.addLayout(spinbox_layout)
        strength_vbox.addWidget(strength_apply_btn)

        # ---------------------------------------------------
        # Visualization Adjustment Group
        # ---------------------------------------------------
        vis_group = QtGui.QGroupBox("Visualization Adjustments")
        vis_vbox = QtGui.QVBoxLayout()
        vis_group.setLayout(vis_vbox)

         # Opacity Label
        opacity_label = QtGui.QLabel("Opacity of map")
        vis_vbox.addWidget(opacity_label)

        # Slider to change years
        self.opacity_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.opacity_slider.setValue(100*self.visualization.get_map_opacity())
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setTickPosition(QtGui.QSlider.TicksBelow)
        vis_vbox.addWidget(self.opacity_slider)

        # Current Value Label
        self.opacity_value_label = QtGui.QLabel()
        self.on_opacity_changed(100*self.visualization.get_map_opacity())
        vis_vbox.addWidget(self.opacity_value_label)

        # Slider events
        self.connect(self.opacity_slider, QtCore.SIGNAL('valueChanged(int)'), self.on_opacity_changed)
        self.connect(self.opacity_slider, QtCore.SIGNAL('sliderReleased()'), self.on_opacity_slider_released)

        # Order of groups
        vbox.addWidget(vis_group)
        vbox.addWidget(mds_group)
        vbox.addWidget(strength_group)
        vbox.addWidget(movie_group)

        return settings_widget

    # value: int position in the data_segment array
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

    def on_opacity_changed(self, value):
        self.opacity_value_label.setText("Current opacity: %s" % int(value) + '%')
        opacityFloat = float(value)/100
        self.visualization.set_map_opacity(opacityFloat)

    def on_opacity_slider_released(self):
        self.render_window.Render()

    def onPlayMovieButtonClicked(self, btn):
        self.visualization.start_movie(self)

    def on_strength_filter_applied(self):
        min = self.strength_min_box.value()
        max = self.strength_max_box.value()
        print "Set strength filter to " + str(min) + "/" + str(max)
        self.visualization.set_strength_range(min, max)

        # update data slider as well because data might not be available anymore
        self.slider_data_array = self.visualization.get_data_segments()
        self.mds_slider.setMaximum(len(self.slider_data_array)-1)

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