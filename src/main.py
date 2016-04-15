import numpy as np
import cv2

import markers

#OpenGL AR: https://www.safaribooksonline.com/library/view/programming-computer-vision/9781449341916/ch04.html


class ARapp:
	def __init__(self):

		#Load camera calibration params
		camparams = np.load('cameracalibration.npz')
		self.mtx = camparams['mtx']
		self.dist = camparams['dist']

	def getRTvecs(self, marker):
		'''Given a marker, gives rotation and translation vectors that will map the object coordinates to image coordinates'''

		objp = np.array([[0.,0.,0.],[1.,0.,0.], [1.,1.,0.],[0.,1.,0.]], dtype='float32')
		imgp = marker['points'].astype('float32')

		_, rvecs, tvecs = cv2.solvePnP(objp, imgp, self.mtx, self.dist)
		return rvecs, tvecs

	def drawAxis(self, f, marker):
		'''Given a marker draw 3D axis from pose estimation'''

		opts = [[0,0,-1],[0,1,0],[1,0,0]]
		colors = [(0,0,255),(0,255,0),(255,0,0)]

		for i in range(0,3):
			objp = np.array([[0,0,0],opts[i]], dtype='float32').reshape(2,3)

			rvecs, tvecs = self.getRTvecs(marker)
			imgp, _ = cv2.projectPoints(objp, rvecs, tvecs, self.mtx, self.dist)
			img = cv2.line(f, tuple(imgp[0].ravel()), tuple(imgp[1].ravel()), colors[i], 4)

		return f

	def showMarkers(self, img):
		img = markers.preprocess(img)
		detmarkers = markers.detectMarkers(img)

		render = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
		for marker in detmarkers:
			render = self.drawAxis(render, marker)
		return render

AR = ARapp()
cam = cv2.VideoCapture(0)

while(True):
	_, img = cam.read()
	img = AR.showMarkers(img)
	cv2.imshow('Augmented Reality', img)
	cv2.waitKey(30)
