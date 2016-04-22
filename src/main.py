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

        glClearColor( 0.0, 0.0, 0.0, 1.0 );
        glClearDepth( 1.0 );

        glShadeModel (GL_SMOOTH);
        glEnable(GL_NORMALIZE);

        #set projection from camera matrix
        #self.set_projection_from_camera(self.mtx)

        #loop
        glutMainLoop()

    def set_projection_from_camera(self, K):
        """  Set view from a camera calibration matrix. """

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

    def drawBackground(self, im):
        """  Draw background image using a quad. """

        #Convert OpenCV image to suitable OpenGL texture format
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        #im = cv2.flip(im, 1)

        #Load background
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        glOrtho(0, self.width, 0, self.height, -1.0, 1.0);
        glViewport(0, 0, self.width , self.height);
        glDisable(GL_TEXTURE_2D);
        glPixelZoom( 1, -1);

        glRasterPos3f(0, self.height, -1.0);
        glDrawPixels (self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE, im);

    def drawAxis(self, axisSize):

        glColor3f (1,0,0)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0) #// origin of the line
        glVertex3f(axisSize,0.0, 0.0) #// ending point of the line
        glEnd( )


        glColor3f (0,1,0)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0) #// origin of the line
        glVertex3f(0.0, axisSize, 0.0) #// ending point of the line
        glEnd( )


        glColor3f (0,0,1)
        glBegin(GL_LINES)
        glVertex3f(0.0, 0.0, 0.0) #// origin of the line
        glVertex3f(0.0, 0.0, axisSize) #// ending point of the line
        glEnd( )

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
        view_matrix = np.transpose(view_matrix)
        return view_matrix

    def drawModel(self, marker):
        """ Adjust ModelView matrix based on rotation and translation vectors. Render model."""

        #Generate and load viewMatrix
        view_matrix = self.getViewMtx(marker)
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        glLoadMatrixd(view_matrix)

        glutSolidCube(10)
        #self.drawAxis()

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


    def render(self):
        ''' Render Augmented Reality frame'''


        _, img = self.cam.read()
        img = cv2.resize(img, (self.width, self.height))
        self.drawBackground(img.copy())
        self.set_projection_from_camera(self.mtx)

        img = markers.preprocess(img)
        detmarkers = markers.detectMarkers(img)

        for marker in detmarkers:
            self.drawModel(marker)

        glutSwapBuffers()

AR = ARapp()
