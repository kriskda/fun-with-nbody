from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import sqrt

import random


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class WindowView(object):
	
	pos_array = []
	
	def __init__(self):
		glutInit()
		glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
		glutCreateWindow("2D nbody on CPU")
		glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
		glutDisplayFunc(self.draw)
		glutTimerFunc(30, self.timer, 30)
		self._init_gl()
		
		self.interacting_bodies = InteractingBodies(self)
		
		glutMainLoop()

	def timer(self, t):
		glutTimerFunc(t, self.timer, t)
		glutPostRedisplay()		

	def _init_gl(self):
		glClearColor(1.0, 1.0, 1.0, 0.0)
		glColor3f(0.0, 0.0, 0.0)
		glPointSize(2.0)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluOrtho2D(0.0, SCREEN_WIDTH, 0.0, SCREEN_HEIGHT)

	def draw(self):
		self.interacting_bodies.run()
		
		glClear(GL_COLOR_BUFFER_BIT)
		glBegin(GL_POINTS)

		for pos_vect in self.pos_array:
			glVertex2f(pos_vect[0], pos_vect[1])

		glEnd()
		glFlush()


class InteractingBodies(object):
	
	def __init__(self, view):
		self.view = view
		self.bodies = []
		self._init_bodies(200)

	def _init_bodies(self, number):
		for i in range(number):
			x0 = random.uniform(0, SCREEN_WIDTH)
			y0 = random.uniform(0, SCREEN_HEIGHT)
			vx0 = 0.0#random.uniform(-100, 100)
			vy0 = 0.0#random.uniform(-100, 100)
			mass = 10**15
			self.bodies.append(BodyModel(i, x0, y0, vx0, vy0, mass))
		
	def run(self):
		pos_array = []

		for body in self.bodies:
			body.calculate_time_step(self.bodies)
			pos_array.append(body.pos_vect)

		self.view.pos_array = pos_array
		
		
class BodyModel(object):
	
	def __init__(self, i, x0, y0, vx0, vy0, mass):	
		self.body_index = i
		self.pos_vect = [x0, y0]
		self.vel_vect = [vx0, vy0]
		self.GM = mass*6.67385*10**-11

	def accel(self, x, v):
		ax = 0
		ay = 0

		for body in self.bodies:
			if body.body_index != self.body_index:
				dX = x[0] - body.pos_vect[0]
				dY = x[1] - body.pos_vect[1]
				rt = sqrt(dX*dX + dY*dY + 10.0)
				common_part = -self.GM/(rt*rt*rt)		

				ax = ax + common_part*dX;
				ay = ay + common_part*dY;

		return [ax, ay]
    
	def _rk4Integration(self):
		dt = 0.1
		x1 = self.pos_vect
		v1 = self.vel_vect
		a1 = self.accel(x1, v1);

		x2 = [x1[i] + 0.5 * v1[i] * dt for i in range(2)]
		v2 = [v1[i] + 0.5 * a1[i] * dt for i in range(2)]
		a2 = self.accel(x2, v2)
    	
		x3= [x1[i] + 0.5 * v2[i] * dt for i in range(2)]
		v3= [v1[i] + 0.5 * a2[i] * dt for i in range(2)]
		a3 = self.accel(x3, v3)
    	
		x4 = [x1[i] + v3[i] * dt for i in range(2)]
		v4 = [v1[i] + a3[i] * dt for i in range(2)]
		a4 = self.accel(x4, v4)
    	
		self.pos_vect = [x1[i] +  (dt / 6.0) * (v1[i] + 2 * v2[i] + 2 * v3[i] + v4[i])  for i in range(2)]
		self.vel_vect = [v1[i] + (dt / 6.0) * (a1[i] + 2 * a2[i] + 2 * a3[i] + a4[i]) for i in range(2)]

	def calculate_time_step(self, bodies):
		self.bodies = bodies
		self._rk4Integration()




if __name__ == "__main__":
	view = WindowView()



