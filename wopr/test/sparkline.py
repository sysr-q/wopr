#!/usr/bin/env python2
from __future__ import print_function
import math
from wopr.widget import Sparkline
from wopr.test import main_loop


class SineSparkline(Sparkline):
	def __init__(self, *args, **kwargs):
		super(SineSparkline, self).__init__(*args, **kwargs)
		self.i = 0
		self.height = 20

	def draw(self, mx, my):
		p = math.sin(math.radians(self.i)) * self.height + self.height
		self.i += 2

		self.add_point(p if p > 0 else 0)
		super(SineSparkline, self).draw(mx, my)


if __name__ == "__main__":
	main_loop(SineSparkline, [0]*1024, name="Sine Sparkline")