# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
from time import sleep
import wx
import os
import sys
import subprocess

class HelloFrame(wx.Frame):
	"""
	A Frame that says Hello World
	"""
	def eye_aspect_ratio(eye):

		# compute the euclidean distances between the two sets of
		# vertical eye landmarks (x, y)-coordinates
		A = dist.euclidean(eye[1], eye[5])
		B = dist.euclidean(eye[2], eye[4])
	 
		# compute the euclidean distance between the horizontal
		# eye landmark (x, y)-coordinates
		C = dist.euclidean(eye[0], eye[3])
	 
		# compute the eye aspect ratio
		ear = (A + B) / (2.0 * C)
	 
		# return the eye aspect ratio
		return ear




	def myFunction(self, queue):

		EYE_AR_THRESH = 0.3
		EYE_AR_CONSEC_FRAMES = 3
		 
		# initialize the frame counters and the total number of blinks
		COUNTER = 0
		TOTAL = 0

		# initialize dlib's face detector (HOG-based) and then create
		# the facial landmark predictor
		print("[INFO] loading facial landmark predictor...")
		detector = dlib.get_frontal_face_detector()
		predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

		# grab the indexes of the facial landmarks for the left and
		# right eye, respectively
		(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
		(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

		# start the video stream thread
		print("[INFO] starting video stream thread...")

		#vs = FileVideoStream(args["video"]).start()
		fileStream = True
		vs = VideoStream(src=0).start()
		# vs = VideoStream(usePiCamera=True).start()
		fileStream = False
		time.sleep(1.0)

		# loop over frames from the video stream
		while True:
			# if this is a file video stream, then we need to check if
			# there any more frames left in the buffer to process
			if fileStream and not vs.more():
				break
		 
			# grab the frame from the threaded video file stream, resize
			# it, and convert it to grayscale
			# channels)
			frame = vs.read()
			frame = imutils.resize(frame, width=450)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		 
			# detect faces in the grayscale frame
			rects = detector(gray, 0)

			# loop over the face detections
			for rect in rects:
				# determine the facial landmarks for the face region, then
				# convert the facial landmark (x, y)-coordinates to a NumPy
				# array
				shape = predictor(gray, rect)
				shape = face_utils.shape_to_np(shape)
		 
				# extract the left and right eye coordinates, then use the
				# coordinates to compute the eye aspect ratio for both eyes
				leftEye = shape[lStart:lEnd]
				rightEye = shape[rStart:rEnd]
				leftEAR = eye_aspect_ratio(leftEye)
				rightEAR = eye_aspect_ratio(rightEye)
		 
				# average the eye aspect ratio together for both eyes
				ear = (leftEAR + rightEAR) / 2.0

						# compute the convex hull for the left and right eye, then
				# visualize each of the eyes
				leftEyeHull = cv2.convexHull(leftEye)
				rightEyeHull = cv2.convexHull(rightEye)
				cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
				cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

						# check to see if the eye aspect ratio is below the blink
				# threshold, and if so, increment the blink frame counter
				if ear < EYE_AR_THRESH:
					COUNTER += 1
		 
				# otherwise, the eye aspect ratio is not below the blink
				# threshold
				else:
					# if the eyes were closed for a sufficient number of
					# then increment the total number of blinks
					if COUNTER >= EYE_AR_CONSEC_FRAMES:
						TOTAL += 1
		 
					# reset the eye frame counter
					COUNTER = 0

							# draw the total number of blinks on the frame along with
				# the computed eye aspect ratio for the frame
				cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

				#print("Eye blinking count: {}".format(TOTAL))
				queue.put(TOTAL)
					 
			# show the frame
			#cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
		 
			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break

			
		 
		# do a bit of cleanup
		cv2.destroyAllWindows()
		vs.stop()




	def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
		super(HelloFrame, self).__init__(*args, **kw)

        # create a panel in the frame
		pnl = wx.Panel(self)

        # and put some text with a larger bold font on it
		st = wx.StaticText(pnl, label="Hello World!", pos=(25,25))
		font = st.GetFont()
		font.PointSize += 10
		font = font.Bold()
		st.SetFont(font)

        # create a menu bar
		self.makeMenuBar()
		self.CreateStatusBar()
		self.SetStatusText("Welcome to wxPython!")

		vbox = wx.BoxSizer(wx.VERTICAL)
		self.btn = wx.Button(pnl, -1, "Click me!")
		self.btn.Bind(wx.EVT_BUTTON, self.onClicked)


	def sampleFunction(q, x):
		q.put(x*x)



	def makeMenuBar(self):
		fileMenu = wx.Menu()
		helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
			"Help string shown in status bar for this menu item")
		fileMenu.AppendSeparator()
		exitItem = fileMenu.Append(wx.ID_EXIT)

		helpMenu = wx.Menu()
		aboutItem = helpMenu.Append(wx.ID_ABOUT)
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu, "&File")
		menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
		self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
		self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
		self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
		self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


	def OnExit(self, event):
		self.Close(True)

	def onClicked(self, event):
		btn = event.GetEventObject().GetLabel()
		print("Button clicked: ",btn)
		from multiprocessing import Process, Queue
		q = Queue()
		p = Process(target=sampleFunction, args=(q, 2))
		p.start()
		print(q.get())
		p.join()

	def OnHello(self, event):
		wx.MessageBox("Hey")


	def OnAbout(self, event):
		wx.MessageBox("This is a wxPython Hello World sample",
					"About Hello World 2",
					wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = HelloFrame(None, title='blinko')
    frm.Show()
    app.MainLoop()