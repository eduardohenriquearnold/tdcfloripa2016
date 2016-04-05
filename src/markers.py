#https://github.com/rdmilligan/SaltwashAR/tree/master/scripts
#https://github.com/Itseez/opencv_contrib/blob/master/modules/aruco/src/aruco.cpp

import cv2
import numpy as np
import sys

def orderPointsCW(pts):
	'''Order set of points clock-wise'''

	pts = np.array(pts, dtype='float32').reshape(len(pts),2)

	#Get the points centered on the origin
	centroid = np.sum(pts, axis=0)/len(pts)
	ptsOrig = pts - centroid

	#Get angles and sort
	angles = -np.arctan2(ptsOrig[:,1], ptsOrig[:,0])
	sorted_idx = np.argsort(angles)
	return pts[sorted_idx]

def extractCandidates(img):
	'''Given an image get borders, contours and select the ones that have four sides'''

	#Pre-processing and edge detection
	img = cv2.GaussianBlur(img, (5,5), 0)
	edges = cv2.Canny(img, 100, 200)

	#Get contours
	_, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	#Filter contours
	candidates = []
	for contour in contours:
		#Get perimeter and poligonal approximation
		perimeter = cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, 0.01*perimeter, True)
		
		#Save as candidate if quadrilateral
		if len(approx) == 4:
			candidates.append(orderPointsCW(approx))

	return candidates

def getMarkerCode(patch):
	'''Given a image patch, get marker binary code'''

	threshold = 150
	pass

def identifyCodeWithinDict(code):
	'''Given a marker code identify its ID and orientation'''

	pass

def getMarkerPatch(img, contour):
	'''Extracts marker patch given a contour'''


	#Form destination points and get perspective transformation matrix
	height, width = 100, 100
	dst = np.array([[0,0], [width-1,0], [width-1,height-1], [0, height-1]], dtype='float32')
	dst = orderPointsCW(dst)
	matrix = cv2.getPerspectiveTransform(contour, dst)

	#Perform perspective transform to get patch
	patch = cv2.warpPerspective(img, matrix, (height, width))
	return patch

def showContours(img, contours):
	'''Helper function to show contours in image'''

	#Convert img to BGR
	color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

	#Draw contours and show image
	contours = [c.astype('int32') for c in contours]
	color = cv2.drawContours(color, contours, -1, (0,0,255))

	cv2.imshow('contours', color)
	cv2.waitKey(0)

def detectMarkers(img):
	'''Given an image, detect candidates and identify markers, if any'''

	#Convert to Grayscale
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#Resize image
	f = 640. / img.shape[0]
	if (f<1):
		img = cv2.resize(img, None, fx=f, fy=f)

	#Get candidates contours
	contours = extractCandidates(img)
	showContours(img, contours)	
	for contour in contours:
		patch = getMarkerPatch(img, contour)
		cv2.imshow("patch", patch)
		cv2.waitKey(0)

#		code = getMarkerCode(patch)
#		id, orientation = identifyCodeWithinDict(code)
	
	
	

#main proc
img = cv2.imread(sys.argv[1])
detectMarkers(img)



