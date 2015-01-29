#!/usr/bin/env python2
import collections
import random
from drawille import Canvas
import q

class Widget(object):
	name = "Widget (Base)"

	def __init__(self, scr, enc="utf-8"):
		self.canvas = Canvas()
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
		self.setup()

	def setup(self):
		self.scr.nodelay(1)
		self.scr.leaveok(0)

	def paint(self):
		self.scr.erase()
		maxY, maxX = self.scr.getmaxyx()

		self.draw()  # -> does stuff with canvas
		for y, line in enumerate(self.canvas.frame().split("\n")):
			self.scr.insstr(y, 0, line)
		self.scr.border()
		self.title()

	def draw(self):
		pass

	def title(self):
		self.scr.insstr(0, 2, " {} ".format(self.name))


class Sparkline(Widget):
	def __init__(self, scr, data, maxlen=1024, enc="utf-8"):
		super(Sparkline, self).__init__(scr, enc=enc)
		self.data = collections.deque(data, maxlen=maxlen)

	def draw(self):
		maxY, maxX = self.scr.getmaxyx()
		data = list(self.data)[-((maxX-2)*2):]  # only get the data we can plot

		self.canvas.clear()
		self.canvas.set(0, 0)
		for i, point in enumerate(data):
			# point is a y location
			self.canvas.set(i, ((maxY*4) / 2) + point)

	def add_point(self, y):
		self.data.append(y)

class RandomSparkline(Sparkline):
	def __init__(self, scr, data, maxlen=1024, enc="utf-8"):
		super(RandomSparkline, self).__init__(scr, data, maxlen=maxlen, enc=enc)

	def draw(self):
		self.add_point(self.data[-1] + random.choice([1, 0, 0, -1]))
		super(RandomSparkline, self).draw()
