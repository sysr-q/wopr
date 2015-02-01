#!/usr/bin/env python2
from __future__ import print_function
import collections
import curses
import math
import random
from drawille import Canvas, line


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
		self.dirty = True
		self.setup()

	def setup(self):
		self.scr.nodelay(1)
		self.scr.leaveok(0)

	def paint(self):
		if not self.dirty:
			return

		self.scr.erase()
		my, mx = self.scr.getmaxyx()

		self.draw(mx, my)  # -> does stuff with canvases

		self.scr.border()
		self.title()
		self.scr.insstr(0, mx-1, self.borders["tr"])  # fix broken border

	def draw_canvas(self, canvas, left=0, attr=0):
		for y, line in enumerate(canvas.frame().split("\n")):
			for x, c in enumerate(line.decode(self.enc)):
				if c == " ":
					continue
				self.scr.addstr(y, x+left, c.encode(self.enc), attr)

	def draw(self, mx, my):
		pass

	def title(self):
		self.scr.insstr(0, 2, " {} ".format(self.name))


class Sparkline(Widget):
	def __init__(self, scr, data, maxlen=1024, enc="utf-8", name="Sparkline"):
		super(Sparkline, self).__init__(scr, enc=enc, name=name)
		def mkcanvases():
			d = {
				"data": collections.deque([], maxlen=maxlen),
				"canvas": Canvas(),
				"attr": curses.color_pair(random.choice([1, 2, 3, 4, 5])),
				"dirty": True,
			}
			return d

		self.axes = Canvas()
		self.canvases = collections.defaultdict(mkcanvases)
		self.maxlen = maxlen

		for x in data:  # data=[("foo", [...]), ("bar", [...])]
			if len(x) == 3:
				name, d, attr = x
			else:
				name, d = x
				attr = None
			self.add_data(name, d, attr=attr)

		self.edge_buffer = 20  # 20px from edges
		self.data_buffer = 3   # + 3px added buffer for the data canvas
		self.rounding = 5  # round axes up to nearest 5.
		self.fill = True  # fill inbetween points with lines

	def add_data(self, name, data, maxlen=None, attr=None):
		if maxlen is None:
			maxlen = self.maxlen
		if attr is not None:
			self.canvases[name]["attr"] = attr
		self.canvases[name]["data"] = collections.deque(data, maxlen=maxlen)

	def add_point(self, name, p):
		self.canvases[name]["data"].append(p)
		self.canvases[name]["dirty"] = True

	def map(self, x, in_min, in_max, out_min, out_max):
		# Shamelessly lifted from the Arduino project.
		if in_max == 0:
			return 0
		return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

	def _render_canvas(self, name, mx, my):
		if not self.canvases[name]["dirty"]:
			# Nothing to do unless the canvas data is dirty.
			return

		# NOTE: We can only show at most (x*2) data points because of how the
		#       braille trick works.
		#       We're also accounting for the screen borders, the buffers for
		#       the axis edges, as well as buffering the data some more.
		_m = -((mx-2-(self.edge_buffer+self.data_buffer))*2)
		data = list(self.canvases[name]["data"])[_m:]

		max_point = float(max(data))
		# Round our vertical axes up to the nearest five. This just looks nicer.
		max_axes = int(math.ceil(max_point / self.rounding)) * self.rounding
		# max_points represents the "100%" mark for our y-axis. i.e. top.
		max_points = (my*4) - self.edge_buffer*2 - self.data_buffer*2

		canvas = self.canvases[name]["canvas"]
		canvas.clear()

		canvas.set(0, 0)  # TODO: why do I need this hack?

		lx, ly = -1, -1
		for i, point in enumerate(data):
			x = i-self.edge_buffer+self.data_buffer
			# 0 -> 0%, max_point -> 100%
			mapped = self.map(float(point), 0.0, max_point, 0.0, float(max_points))
			# account for edges and stuff, my*8/2 etc.
			y = (my*4) - self.edge_buffer - self.data_buffer - mapped
			canvas.set(x, y)

			if not self.fill:
				continue

			if lx == -1 and ly == -1:
				lx, ly = x, y
				continue

			# Draw a line between the new points and the last point.
			# It just makes it look better.
			for nx, ny in line(lx, ly, x, y):
				canvas.set(nx, ny)
			lx, ly = x, y

	def draw(self, mx, my):  # Just warning you, this code is absolute trash.
		if not any(map(lambda c: c["dirty"], self.canvases.values())):
			# Nothing dirty here, just skip.
			self.dirty = False
			return

		# TODO debugging trash
		#sf = "max_axes=%d max_point=%d max_points=%d fill=%s"
		#self.scr.addstr(1, 1, sf % (max_axes, max_point, max_points, self.fill))

		# Draw axes
		self.axes.clear()
		self.axes.set(0, 0)  # TODO: why do I need this hack?
		for y in range(self.edge_buffer, (my)*4 - self.edge_buffer):  # left axes
			self.axes.set(self.edge_buffer, y)
		for x in range(self.edge_buffer, (mx)*2 - self.edge_buffer):  # bottom axes
			# (my*4) is (my*8)/2 for the edge.
			self.axes.set(x, (my)*4 - self.edge_buffer)

		# Render all the canvases
		for name in self.canvases.keys():
			self._render_canvas(name, mx, my)

		# Draw all the canvases
		for name in self.canvases.keys():
			self.draw_canvas(self.canvases[name]["canvas"],
							 left=(self.data_buffer+self.edge_buffer)/2,
							 attr=self.canvases[name]["attr"])

		# Draw the axes last.
		self.draw_canvas(self.axes, attr=curses.color_pair(0))
