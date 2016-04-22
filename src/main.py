import numpy as np
import cv2

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import markers

class ARapp:
    def __init__(self):

        #Load camera calibration params
        camparams = np.load('cameracalibration.npz')
        self.mtx = camparams['mtx']
        self.dist = camparams['dist']
        self.width, self.height = 640,480

        #Start VideoCapture
        self.cam = cv2.VideoCapture(0)

        #set constant matrix
        self.CV_TO_GL_mtx   = np.array([[ 1.0, 0.0, 0.0, 0.0],
                                        [ 0.0,-1.0, 0.0, 0.0],
                                        [ 0.0, 0.0,-1.0, 0.0],
                                        [ 0.0, 0.0, 0.0, 1.0]])

        #Setup window and OpenGL environment
        glutInit()
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        self.window_id = glutCreateWindow('AR app')
        glutDisplayFunc(self.render)
        glutIdleFunc(self.render)

        #set projection from camera matrix
        self.set_projection_from_camera(self.mtx)

        #loop
        glutMainLoop()

    def set_projection_from_camera(self, K):
        """  Set view from a camera calibration matrix. """

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        fx = K[0,0]
        fy = K[1,1]
        fovy = 2*np.arctan(0.5*self.height/fy)*180./np.pi
        aspect = (self.width*fy)/(self.height*fx)

        # define the near and far clipping planes
        near = 0.1
        far = 100.0

        # set perspective
        gluPerspective(fovy,aspect,near,far)
        glViewport(0,0,self.width,self.height)

    def drawBackground(self, im):
        """  Draw background image using a quad. """

        #Convert OpenCV image to suitable OpenGL texture format
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im = cv2.flip(im, -1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # bind the texture
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,glGenTextures(1))
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,self.width,self.height,0,GL_RGB,GL_UNSIGNED_BYTE,im)

        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)

        # create quad to fill the whole window
        glBegin(GL_QUADS)
        glTexCoord2f(0.0,0.0); glVertex3f(-1.0,-1.0,-1.0)
        glTexCoord2f(1.0,0.0); glVertex3f( 1.0,-1.0,-1.0)
        glTexCoord2f(1.0,1.0); glVertex3f( 1.0, 1.0,-1.0)
        glTexCoord2f(0.0,1.0); glVertex3f(-1.0, 1.0,-1.0)
        glEnd()

        # clear the texture
        glDeleteTextures(1)

    def getViewMtx(self, marker):
        '''Given a marker, gives rotation and translation vectors that will map the object coordinates to image coordinates'''

        #Get rotation and translation vectors to match imgp
        objp = np.array([[-5.,-5.,0.],[5.,-5.,0.], [5.,5.,0.],[-5.,5.,0.]], dtype='float32')
        imgp = marker['points'].astype('float32')
        _, rvecs, tvecs = cv2.solvePnP(objp, imgp, self.mtx, self.dist)

        #Get rotation matrix
        rmtx = cv2.Rodrigues(rvecs)[0]

        #Generate view matrix
        view_matrix = np.array([[rmtx[0][0],rmtx[0][1],rmtx[0][2],tvecs[0]],
                                [rmtx[1][0],rmtx[1][1],rmtx[1][2],tvecs[1]],
                                [rmtx[2][0],rmtx[2][1],rmtx[2][2],tvecs[2]],
                                [0.0       ,0.0       ,0.0       ,1.0    ]])

        view_matrix = np.matmul(self.CV_TO_GL_mtx, view_matrix)
        #view_matrix = np.transpose(view_matrix)
        return view_matrix

    def drawModel(self, marker):
        """ Adjust ModelView matrix based on rotation and translation vectors. Render model."""

        #Generate and load viewMatrix
        view_matrix = self.getViewMtx(marker)
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixd(view_matrix)

        #Draw model
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        # glEnable(GL_DEPTH_TEST)
        # glClear(GL_DEPTH_BUFFER_BIT)

        # draw red teapot
        # glMaterialfv(GL_FRONT,GL_AMBIENT,[0,0,0,0])
        # glMaterialfv(GL_FRONT,GL_DIFFUSE,[0.5,0.0,0.0,0.0])
        # glMaterialfv(GL_FRONT,GL_SPECULAR,[0.7,0.6,0.6,0.0])
        # glMaterialf(GL_FRONT,GL_SHININESS,0.25*128.0)
        #glutSolidTeapot(0.1)
        glutWireCube(1)

    def render(self):
        ''' Render Augmented Reality frame'''

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        _, img = self.cam.read()
        img = cv2.resize(img, (self.width, self.height))
        self.drawBackground(img.copy())

        img = markers.preprocess(img)
        detmarkers = markers.detectMarkers(img)

        for marker in detmarkers:
            self.drawModel(marker)

        glutSwapBuffers()

AR = ARapp()
