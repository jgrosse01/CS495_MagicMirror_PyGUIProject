"""
Created on 22 January 2022
Name: Mirror.py
Author: Jake Grosse
Description: A Python GUI which creates a mirror for the user to see themselves in.

Citation: The following link was used to consult few things at the end as I discovered that, of course,
          someone had thought of this exact idea and made a webcam photo booth. The project has been a
          process of revision and redesign, going from a game manual, to a Rick-Roll, now to a
          mirror. I found the CV2 library a few days ago and PIL and tk are standard.

          I looked to the internet for help with tkinter labels to properly format images from CV2 inputs
          and to see how other people handled color. I found both in one link with a very similar
          format to my own code. I will sign a sheet of paper that says that I wrote everything except
          that which is cited as not written by me. I promise you I did write most of this before looking
          online at this detailed project.
          https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/
          This link is referred to as SOLARIAN from here on out so I don't have to make the code ugly with links.
          I realize that this link has other features which I do not, but I wasn't going to write it off as my own
          nor was I going to get the deduction for citing huge portions of code. Therefore, we have a mirror and not
          a camera booth. It is referenced in two places in this file.
"""

# import GUI container/utility (tkinter)
import tkinter as tk
# import threads to use for streaming video
import threading as td
# import open computer vision library
import cv2
# import pillow image handling objects
from PIL import Image, ImageTk


# a class extending tkinter.Tk which holds a place for a webcam input
class Mirror(tk.Tk):
    def __init__(self, title, geom="1280x720"):
        # initialize superclass tk window
        tk.Tk.__init__(self)
        # change the tkinter title
        self.title(title)
        # change the tkinter geometry
        self.geometry(geom)
        # background color change
        self.configure(bg="grey")

        # delay wait time as I found was needed for an update or it would literally just freeze
        # incorporated in the update method using tk.after in relation to self
        self.wait_time_ms = 15

        # get video opened to use (zero is the primary webcam source)
        self.video = VideoRecorder(0)
        # wiki says canvas is better than frame for images
        # make a canvas to output video to, but labels
        # don't flicker when updating several times per second
        self.lbl = tk.Label(self, width=1200, height=720)
        self.lbl.pack()

        # creating a thread to run the video otherwise the window never opens
        self.video_thread = td.Thread(target=self.stream)
        # daemon thread
        self.video_thread.daemon = 1
        # start the video stream
        self.video_thread.start()

        # disallow the window from being resized so we don't have extra movement with the camera not scaling
        self.resizable(0, 0)

        self.mainloop()

    # stream the webcam input to the associated label on the "Mirror"
    def stream(self):
        # display video
        while self.video.isOpened():
            # capture frame from video
            returned_frame, frame = self.video.read()
            if returned_frame:
                # FROM SOLARION, second parameter was copy pasted, the rest was hand typed
                temp_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                vp_dims = self.video.get_geom()
                # FROM SOLARION, the use of fromarray is being cited to solve a problem
                # transpose just flips from left to right
                # Resize just doubles the viewport dimensions so that the image fills most of the screen
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(temp_image).transpose(method=Image.FLIP_LEFT_RIGHT).resize((2*vp_dims[0], 2*vp_dims[1])))

                # set label image to the selected photo (credit Ted for teaching this)
                self.lbl.configure(image=self.photo)
                self.lbl.image = self.photo
            # delay in updates so that the computer isn't fully consumed by processing individual images
            cv2.waitKey(self.wait_time_ms)


# a class responsible for capturing and handling the dimensions and release of video resources
class VideoRecorder(cv2.VideoCapture):
    def __init__(self, source):
        cv2.VideoCapture.__init__(self, source)
        # setting viewport width and height in pixels
        # commands found in documentation https://docs.opencv.org/4.x/index.html
        self.vp_width = self.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.vp_height = self.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # when the object is deleted, see if the video is active and if it is then release the video device
    def __del__(self):
        if self.isOpened():
            self.release()

    # returns a list of the viewport dimensions in pixels of the camera
    def get_geom(self):
        # cast to integers because they default to float values
        return [int(self.vp_width), int(self.vp_height)]

