#https://github.com/rdmilligan/SaltwashAR/tree/master/scripts
#https://github.com/Itseez/opencv_contrib/blob/master/modules/aruco/src/aruco.cpp

import cv2
import numpy as np
import sys
import itertools
import codes

#Debug values: edges, contours, patches, markers
debug=['markers']

def orderPointsCW(pts):
	'''Order set of points clockwise'''

	pts = np.array(pts, dtype='float32').reshape(len(pts),2)

	#Get the points centered on the origin
	centroid = np.sum(pts, axis=0)/len(pts)
	ptsOrig = pts - centroid

	#Get angles and sort
	angles = np.arctan2(ptsOrig[:,1], ptsOrig[:,0])
	sorted_idx = np.argsort(angles)
	return pts[sorted_idx]

def extractCandidates(img):
	'''Given an image get borders, contours and select the ones that have four sides'''

	#Pre-processing and edge detection
	img = cv2.GaussianBlur(img, (5,5), 0)
	edges = cv2.Canny(img, 100, 200)

	if 'edges' in debug:
		cv2.imshow('edges', edges)
		cv2.waitKey(0)

	#Get contours
	_, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	#Filter contours
	candidates = []
	for contour in contours:
		#Get perimeter and poligonal approximation
		perimeter = cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, 0.1*perimeter, True)
		
		#Save as candidate if quadrilateral
		if len(approx) == 4:
			candidates.append(orderPointsCW(approx))

	#Remove similar candidates
	for idx1, idx2 in itertools.combinations(range(0,len(candidates)), 2):
		try:
			diff = np.mean(np.absolute(candidates[idx1]-candidates[idx2]))
			if diff < 20:
				candidates.pop(idx2)
		except:
			pass
	return candidates

def getMarkerCode(patch):
	'''Given a image patch, get marker binary code'''

	cells = codes.cells
	cellsize = patch.shape[0]/cells

	code = np.zeros((cells,cells))

	for i in range(cells):
		for j in range(cells):
			px = i*cellsize+0.5*cellsize
			py = j*cellsize+0.5*cellsize
			px, py = round(px), round(py)
			code[i,j] = patch[px, py]/255.

	return code			

def getMarkerPatch(img, contour):
	'''Extracts marker patch given a contour'''


	#Form destination points and get perspective transformation matrix
	height, width = 100, 100
	dst = np.array([[0,0], [width-1,0], [width-1,height-1], [0, height-1]], dtype='float32')
	dst = orderPointsCW(dst)
	matrix = cv2.getPerspectiveTransform(contour, dst)

	#Perform perspective transform to get patch
	patch = cv2.warpPerspective(img, matrix, (height, width))

	#Perform Otsu's thresholding to have a binary image
	_, patch = cv2.threshold(patch, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

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

def showMarkers(img, markers):
	'''Helper function to show markers in image'''

	#Convert img to BGR
	color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

	#Draw markers with circle on the orientation point
	for marker in markers:
		pts = marker['points'].astype('int32')
		color = cv2.drawContours(color, [pts], -1, (0,0,255))
		color = cv2.circle(color, tuple(pts[marker['orientation'],:]), 5, (255,0,0), -1)
		centroid = np.sum(pts, axis=0)/len(pts)
		color = cv2.putText(color, str(marker['id']), tuple(centroid), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))

	cv2.imshow('contours', color)
	cv2.waitKey(0)

def preprocess(img):
	'''Preprocess image, adjust color to grayscale and resizes'''

	#Convert to Grayscale
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#Resize image
	f = 640. / img.shape[0]
	if (f<1):
		img = cv2.resize(img, None, fx=f, fy=f)

	return img

def detectMarkers(img):
	'''Given an image, detect candidates and identify markers, if any'''

	#Get candidates contours
	contours = extractCandidates(img)

	if 'contours' in debug:
		showContours(img, contours)	

	markers = []
	for contour in contours:
		patch = getMarkerPatch(img, contour)
		code = getMarkerCode(patch)
		id, orientation = codes.matchCode(code)
		if id != -1:
			markers.append({'id':id, 'orientation':orientation, 'points':contour})

		if 'patches' in debug:
			print id, orientation
			print code
			cv2.imshow("patch", patch)
			cv2.waitKey(0)

	if 'markers' in debug:
		showMarkers(img, markers)

	return markers
	

#main proc
img = cv2.imread(sys.argv[1])
img = preprocess(img)
markers = detectMarkers(img)
print markers



