#!/usr/bin/env python2
from __future__ import print_function
import curses
import locale
import time
from .widget import * #Widget, Sparkline


locale.setlocale(locale.LC_ALL, "")
code = locale.getpreferredencoding()

def main(stdscr):
	w = RandomSparkline(stdscr, [0]*1024, enc=code)
	y, x = stdscr.getmaxyx()

	while True:
		w.paint()

		c = stdscr.getch(0, 0)

		if c == ord('q'):
			break
		elif c == curses.KEY_RESIZE:
			y, x = stdscr.getmaxyx()
			continue

		stdscr.refresh()
		stdscr.move(0, 0)

		time.sleep(30000/1e6)
