#!/usr/bin/python3

from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os

class PhotoBoothApp:
    def __init__(self, vs, outputPath):
        """ Store the video stream object and output path, then initialize
            the most recently read frame, thread for reading frames, and
            the thread stop event. """
        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None

        # Initialize the root window and image panel
        self.root = tki.Tk()
        self.panel = None

        # create a button, that when pressed, will take the current
        # frame and save it to file
        btn = tki.Button(self.root, text="Snapshot!", command=self.takeSnapshot)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        # start a thread that constantly pools the video sensor for
        # the most recently readh frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        # set a callback to handle whhen the window is closed
        self.root.wm_title("PyImageSearch Photobooth")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)

                # openCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, the convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageRg.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                # otherwise, wimply update the panel
            else:
                self.panel.configure(image=image)
                self.panel.image = image

        # except RuntimeError, e:
        except:
            print("[INFO] caught a RuntimeError")

    def takeSnapshot(self):
        # grab the current timestamp and use it to construct the
        # output path
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.outputPath, filename))

        # save the file
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved = {}".format(filename))

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit proces to continue
        print("[INFO] closing ...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()


