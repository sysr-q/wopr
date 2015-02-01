#!/usr/bin/env python2
from __future__ import print_function
import collections
import curses
import math
import random
from drawille import Canvas, line
import q

class Widget(object):
	def __init__(self, scr, enc="utf-8", name="Widget"):
		self.borders = {
			"tl": u"\u250C".encode(enc),
			"bl": u"\u2514".encode(enc),
			"tr": u"\u2510".encode(enc),
			"br": u"\u2518".encode(enc),
			"lr": u"\u2502".encode(enc),
			"tb": u"\u2500".encode(enc),
		}

		self.scr = scr
		self.enc = enc
		self.name = name
		self.setup()

	def setup(self):
		self.scr.nodelay(1)
		self.scr.leaveok(0)

	def paint(self):
		self.scr.erase()
		my, mx = self.scr.getmaxyx()

		self.draw(mx, my)  # -> does stuff with canvases

		self.scr.border()
		self.title()
		self.scr.insstr(0, mx-1, self.borders["tr"])  # fix broken border

	def draw_canvas(self, canvas, attr=0):
		for y, line in enumerate(canvas.frame().split("\n")):
			self.scr.insstr(y, 0, line, attr)

	def draw(self, mx, my):
		pass

	def title(self):
		self.scr.insstr(0, 2, " {} ".format(self.name))


class Sparkline(Widget):
	def __init__(self, scr, data, maxlen=1024, enc="utf-8", name="Sparkline"):
		super(Sparkline, self).__init__(scr, enc=enc, name=name)
		self.canvas = Canvas()
		self.axes = Canvas()
		self.data = collections.deque(data, maxlen=maxlen)
		self.edge_buffer = 20  # 20px from edges
		self.data_buffer = 3   # + 3px added buffer for the data canvas
		self.rounding = 5  # round axes up to nearest 5.
		self.fill = True  # fill inbetween points with lines

	def map(self, x, in_min, in_max, out_min, out_max):
		# Shamelessly lifted from the Arduino project.
		if in_max == 0:
			return 0
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

	def draw(self, mx, my):  # Just warning you, this code is absolute trash.
		# NOTE: We can only show at most (x*2) data points because of how the
		#       braille trick works.
		#       We're also accounting for the screen borders, the buffers for
		#       the axis edges, as well as buffering the data some more.
		data = list(self.data)[-((mx-2-(self.edge_buffer+self.data_buffer))*2):]

		max_point = max(data)
		# Round our vertical axes up to the nearest five. This just looks nicer.
		max_axes = int(math.ceil(max_point / float(self.rounding))) * self.rounding
		# max_points represents the "100%" mark for our y-axis. i.e. top.
		max_points = (my*4) - self.edge_buffer*2 - self.data_buffer*2

		self.canvas.clear()
		self.axes.clear()

		## Draw axes
		self.axes.set(0, 0)  # TODO: why do I need this hack?
		self.scr.addstr(1, 1, "max_axes=%d max_point=%d max_points=%d" % (max_axes, max_point, max_points))
		for y in range(self.edge_buffer, (my)*4 - self.edge_buffer):  # left axes
			self.axes.set(self.edge_buffer, y)
		for x in range(self.edge_buffer, (mx)*2 - self.edge_buffer):  # bottom axes
			# (my*4) is (my*8)/2 for the edge.
			self.axes.set(x, (my)*4 - self.edge_buffer)

		## Draw data on "main" canvas.
		self.canvas.set(0, 0)  # TODO
		lx, ly = -1, -1
		for i, point in enumerate(data):
			x = i-self.edge_buffer+self.data_buffer
			# 0 -> 0%, max_point -> 100%
			mapped = int(self.map(float(point), 0.0, float(max_point), 0.0, float(max_points)))
			# account for edges and stuff, my*8/2 etc.
			y = (my*4) - self.edge_buffer - self.data_buffer - mapped
			self.canvas.set(x, y)

			if not self.fill:
				continue

			if lx == -1 and ly == -1:
				lx, ly = x, y
				continue

			# Draw a line between the new points and the last point.
			# It just makes it look better.
			for nx, ny in line(lx, ly, x, y):
				self.canvas.set(nx, ny)
			lx, ly = x, y

		self.draw_canvas(self.canvas, attr=curses.color_pair(2))
		self.draw_canvas(self.axes, attr=curses.color_pair(0))

	def add_point(self, y):
		self.data.append(y)

class RandomSparkline(Sparkline):
	def __init__(self, *args, **kwargs):
		super(RandomSparkline, self).__init__(*args, **kwargs)
		self.i = 0
		self.height = 20

	def draw(self, mx, my):
		p = math.sin(math.radians(self.i)) * self.height + self.height
		self.i += 2

		self.add_point(p if p > 0 else 0)
		super(RandomSparkline, self).draw(mx, my)
