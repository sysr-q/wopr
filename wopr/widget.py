#!/usr/bin/env python2
import collections
import curses
import random
from drawille import Canvas
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
		maxY, maxX = self.scr.getmaxyx()

		self.draw()  # -> does stuff with canvases

		self.scr.border()
		self.title()
		self.scr.insstr(0, maxX-1, self.borders["tr"])  # fix broken border

	def draw_canvas(self, canvas, attr=0):
		for y, line in enumerate(canvas.frame().split("\n")):
			self.scr.insstr(y, 0, line, attr)

	def draw(self):
		pass

	def title(self):
		self.scr.insstr(0, 2, " {} ".format(self.name))


class Sparkline(Widget):
	def __init__(self, scr, data, maxlen=1024, enc="utf-8", name="Sparkline"):
		super(Sparkline, self).__init__(scr, enc=enc, name=name)
		self.canvas = Canvas()
		self.axes = Canvas()
		self.data = collections.deque(data, maxlen=maxlen)

	def draw(self):
		maxY, maxX = self.scr.getmaxyx()

		buffer = 20
		data_buffer = 3
		# We can only show (x*2) points of data. Also account for padding etc.
		data = list(self.data)[-((maxX-2-(buffer+data_buffer))*2):]
		max_point = max(data)
		max_axes = (max_point // 10) * 10

		self.canvas.clear()
		self.axes.clear()

		## AXES ###############################################################
		self.axes.set(0, 0)
		self.scr.addstr(1, 1, str(max_axes))
		for y in range(buffer, (maxY)*4 - buffer):  # left axes
			self.axes.set(buffer, y)
		for x in range(buffer, (maxX)*2 - buffer):  # bottom axes
			# (maxY*4)-buffer is (maxY*8)/2 for the edge.
			self.axes.set(x, (maxY)*4 - buffer)

		## DATA ###############################################################
		self.canvas.set(0, 0)
		for i, point in enumerate(data):
			# (maxY*2) is the average for the widget's center point.
			self.canvas.set(i-buffer+data_buffer, (maxY*4) - buffer - data_buffer - point)

		self.draw_canvas(self.canvas, attr=curses.color_pair(2))
		self.draw_canvas(self.axes, attr=curses.color_pair(0))

	def add_point(self, y):
		self.data.append(y)

class RandomSparkline(Sparkline):
	def draw(self):
		p = self.data[-1] + random.choice([1, 1, 0, 0, -1])
		self.add_point(p if p > 0 else 0)
		super(RandomSparkline, self).draw()
