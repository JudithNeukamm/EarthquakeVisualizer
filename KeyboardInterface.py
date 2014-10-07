# Define a class for the keyboard interface
class KeyboardInterface(object):
    """Keyboard interface.

    Provides a simple keyboard interface for interaction. You may
    extend this interface with keyboard shortcuts for, e.g., moving
    the slice plane(s) or manipulating the streamline seedpoints.

    """

    def __init__(self):
        self.screenshot_counter = 0
        self.render_window = None
        self.window2image_filter = None
        self.png_writer = None
        self.sliderUp = 0.3
        self.sliderDown = 0.3
        self.dNew = 0

    def keypress(self, obj, event):
        """This function captures keypress events and defines actions for
        keyboard shortcuts."""
        key = obj.GetKeySym()
        if key == "q":
            print "q pressed"

        elif key == "9":
            self.render_window.Render()
            self.window2image_filter.Modified()
            screenshot_filename = ("screenshot%02d.png" % self.screenshot_counter)
            self.png_writer.SetFileName(screenshot_filename)
            self.png_writer.Write()
            print("Saved %s" % screenshot_filename)
            self.screenshot_counter += 1

#         # decrease slice plane
#         elif key == "i" and self.dNew >= 0:
#             self.dNew = self.dNew - self.sliderDown
#             slicePlane.SetExtent(0,W,0,H,self.dNew,self.dNew)
#             self.render_window.Render()
#
#         # increase slice plane
#         elif key == "o" and self.dNew <= 15:
#             self.dNew = self.dNew + self.sliderUp
#             slicePlane.SetExtent(0,W,0,H,self.dNew,self.dNew)
#             self.render_window.Render()
#
