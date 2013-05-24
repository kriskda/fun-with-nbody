from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

class WindowView(object):
	
	pos_vect = [0.0, 0.0]
	
	def __init__(self):
		glutInit()
		glutInitWindowSize(640, 480)
		glutCreateWindow("2D nbody on CPU")
		glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
		glutDisplayFunc(self.draw)
		glutTimerFunc(30, self.timer, 30)
		self._init_gl()
		
		model = BodyModel(self, [1, 1])
		self.controller = NbodyController(model, self)
		
		glutMainLoop()

	def timer(self, t):
		glutTimerFunc(t, self.timer, t)
		glutPostRedisplay()		

	def _init_gl(self):
		glClearColor(1.0, 1.0, 1.0, 0.0)
		glColor3f(0.0, 0.0, 0.0)
		glPointSize(4.0)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluOrtho2D(0.0, 640.0, 0.0, 480.0)

	def draw(self):
		self.controller.run()
		
		glClear(GL_COLOR_BUFFER_BIT)
		glBegin(GL_POINTS)
		glVertex2f(self.pos_vect[0], self.pos_vect[1])
		glEnd()
		glFlush()
		
		
class BodyModel(object):
	
	def __init__(self, view, pos_vect):
		self.view = view
		self.pos_vect = pos_vect
		
	def simulate(self):
		self.view.pos_vect = [random.uniform(100, 200), random.uniform(100, 200)]


class NbodyController(object):
	
	def __init__(self, model, view):
		self.model = model
		
	def run(self):
		self.model.simulate()

if __name__ == "__main__":
	view = WindowView()

	
	
	
