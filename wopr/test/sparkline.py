#!/usr/bin/env python2
from __future__ import print_function
import curses
import math
from wopr.widget import Sparkline
from wopr.test import main_loop


class SineSparkline(Sparkline):
	def __init__(self, *args, **kwargs):
		super(SineSparkline, self).__init__(*args, **kwargs)
		self.i = 0
		self.height = 20

	def draw(self, mx, my):
		p1 = math.sin(math.radians(self.i)) * self.height + self.height
		p2 = math.sin(math.radians(self.i + 90)) * self.height + self.height
		p3 = math.sin(math.radians(self.i + 180)) * self.height + self.height

		self.i += 2

		self.add_point("test1", p1 if p1 > 0 else 0)
		self.add_point("test2", p2 if p2 > 0 else 0)
		self.add_point("test3", p3 if p3 > 0 else 0)
		super(SineSparkline, self).draw(mx, my)


if __name__ == "__main__":
	d = [
		("test1", [0]*1024),
		("test2", [0]*1024),
		("test2", [0]*1024),
	]
	main_loop(SineSparkline, d, name="Three-phase Sparkline")
